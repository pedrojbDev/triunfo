# Triunfo

Fine-tuning de um Qwen2.5 de 1,5 bilhão de parâmetros para transformar pedidos em linguagem natural em chamadas de ferramentas.

O desafio é escolher a função disponível, respeitar seu formato e extrair os argumentos do pedido. O Triunfo compara o mesmo modelo antes e depois de um ajuste com LoRA, com dados e protocolo versionados.

## Resultado no teste reservado

| Métrica — 444 exemplos de chamada única | Qwen original | Triunfo LoRA |
| --- | ---: | ---: |
| Chamada interpretável pelo leitor | 254/444 — 57,21% | 416/444 — 93,69% |
| Ferramenta correta | 251/444 — 56,53% | 412/444 — 92,79% |
| Ferramenta e argumentos iguais à referência | 173/444 — 38,96% | 280/444 — 63,06% |

**Ganho de 24,10 pontos percentuais em correspondência exata**, com 128 casos corrigidos e 21 regressões. Na validação de 430 chamadas, a mesma métrica passou de 36,28% para 63,49%.

O teste contém 558 exemplos: 444 chamadas e 114 respostas em outro formato. Os dois modelos geraram respostas para todos os exemplos, mas a tabela mede somente as chamadas. As contagens de chamadas nos exemplos textuais não são taxas de recusa correta. A revisão qualitativa da validação encontrou falhas relevantes nesse comportamento.

[Resumo do teste](reports/test558_summary.json) · [Protocolo fixado antes do teste](configs/final_test_protocol.json) · [Conferência dos resultados](reports/test_integrity.json)

## Experimento

| Item | Configuração |
| --- | --- |
| Modelo original | [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) |
| Revisão do modelo | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| Dados | [Team-ACE/ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE), exemplos sintéticos supervisionados |
| Revisão dos dados | `6bda777c88d21e5a204703c1ee45597a8fa4f734` |
| Recorte | 5.586 exemplos: 4.469 treino / 559 validação / 558 teste |
| Método | LoRA, rank 16, alpha 32, dropout 0,05; projeções q/k/v/o |
| Parâmetros treináveis | 4.358.144 — 0,2815% do modelo com adaptadores |
| Treino | Uma época, 559 atualizações, batch físico 1 e acumulação de 8 |
| Otimização | AdamW, lr 0,0001, 28 passos de aquecimento e decaimento linear |
| Supervisão | Apenas resposta do assistente e encerramento do chat |
| Contexto | Limite de 2.048 tokens; máximo observado no treino: 1.711; sem cortes |
| Hardware | Tesla T4; pico de memória alocada: 6,02 GiB |
| Precisão | Base float16, adaptadores float32, precisão mista; sem quantização |

A execução preservada levou aproximadamente 35 minutos. A configuração já coube na T4 sem quantização; a decisão foi tomada após um piloto com o exemplo de treino mais longo. Não houve busca de hiperparâmetros pelo resultado de teste.

## Dados e avaliação

A preparação seleciona conversas de uma rodada com descrições de ferramentas legíveis: 4.297 exemplos de chamada única e 1.289 respostas fora dos colchetes. Essa segunda categoria descreve formato, não um rótulo semântico de recusa.

Três duplicatas exatas foram unificadas. Pedidos normalizados iguais ou conjuntos idênticos de descrições de ferramentas foram mantidos na mesma divisão, com semente 42. Os três JSONL foram reproduzidos com os mesmos hashes. Ferramentas individuais podem aparecer em divisões diferentes; não é um teste de APIs inéditas nem uma garantia contra todas as paráfrases.

O avaliador lê argumentos literais sem executar funções. A correspondência exata ignora a ordem das chaves e mantém os valores JSON estritos, inclusive a diferença entre `120` e `120.0`. Não comprova equivalência funcional, correção no mundo real ou validação completa do schema.

[Protocolo de avaliação](docs/evaluation.md) · [Preparação e hashes](reports/dataset_manifest.json) · [Análise de erros](docs/results.md)

## Reproduzir e consultar

Treinamento e inferência foram executados no Colab. As etapas com modelos devem ser executadas em Colab/Kaggle com GPU; os testes do avaliador usam somente a biblioteca padrão do Python.

1. [Preparar os dados](notebooks/01_data_inspection.ipynb): fixa a revisão, aplica o recorte e exporta as divisões.
2. [Treinar com LoRA](notebooks/03_lora_training.ipynb): restaura o ZIP, prepara o modelo e os tokens e salva checkpoints no Drive.
3. [Consultar a execução completa](notebooks/Triunfo.ipynb): reúne treinamento, comparações e o protocolo do teste com as saídas observadas. É um registro de execução; não use “Executar tudo” em uma sessão que já tem artefatos.
4. [Publicar o adaptador](notebooks/04_publish_huggingface.ipynb): preparação, autenticação e envio; não exige GPU nem carrega o modelo.

As versões observadas estão em [requirements-colab.txt](requirements-colab.txt) e [colab_environment.json](reports/colab_environment.json). Não há imagem de ambiente empacotada; novas versões do Colab podem exigir adaptação documentada. Não reinstale o PyTorch com CUDA sem verificar compatibilidade.

Para verificar o avaliador, sem baixar modelos:

```bash
python -m unittest discover -s tests -v
```

O código de avaliação fica em [src/triunfo/evaluation.py](src/triunfo/evaluation.py). Os pesos ficam fora do Git. O adaptador está publicado em [pedrojb04/triunfo](https://huggingface.co/pedrojb04/triunfo). A [ficha do modelo](huggingface/README.md) e o [registro de publicação](reports/huggingface_publication.json) acompanham os resultados. Os arquivos remotos foram conferidos por hash, com os mesmos pesos do teste final.

## Limitações observadas

- Os dados são sintéticos e há referências com datas ou convenções que não podem ser determinadas apenas pelo pedido.
- A métrica estrita pode rejeitar respostas funcionalmente equivalentes. O modelo também comete erros reais: omissão de argumentos, ferramenta inadequada e valores inventados.
- A revisão de 12 exemplos textuais de validação encontrou chave de API fictícia e confusão entre argumentos obrigatórios e opcionais. Não há demonstração de melhora geral em recusas nem uma nota semântica para os 114 textos do teste.
- O formato suportado é uma chamada por resposta. Chamadas paralelas, múltiplas rodadas e português não foram avaliados como tarefas próprias.
- As APIs descritas no ToolACE não foram integradas nem executadas. O repositório não contém um agente que opera serviços reais ou uma demonstração de produção.

## Rastreabilidade e licença

Revisões, hashes, configurações, previsões e resultados ficam em `configs/` e `reports/`. O teste foi interrompido por cota de GPU; a retomada preservou os 558 resultados do original e os primeiros 147 do ajustado. Os 411 restantes foram concluídos com o mesmo protocolo.

Uma primeira execução de treino perdeu os pesos armazenados na máquina temporária. A repetição com a mesma configuração passou a salvar no Drive; ambos os registros permanecem identificados. O adaptador avaliado é o da execução `lora_epoch1_recovery`.

Código sob [Apache 2.0](LICENSE). O Qwen2.5-1.5B-Instruct e o ToolACE declaram Apache 2.0 em suas fichas. Consulte as fontes originais antes de redistribuir material derivado.
