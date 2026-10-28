# Triunfo

Fine-tuning de um LLM pequeno para gerar chamadas de ferramentas a partir de pedidos em linguagem natural.

O projeto investiga três comportamentos: escolher a ferramenta correta, preencher seus argumentos e reconhecer pedidos que as ferramentas disponíveis não atendem.

## Estado atual

Preparação dos dados executada no Colab, a partir dos 11.300 exemplos da revisão `6bda777c88d21e5a204703c1ee45597a8fa4f734` do ToolACE. O recorte tem 5.586 exemplos: 4.469 de treino, 559 de validação e 558 de teste, com semente 42. Ainda não há modelo ajustado ou resultados de avaliação de modelos.

O [notebook de preparação](notebooks/01_data_inspection.ipynb) fixa a revisão e reúne a lógica das células utilizadas. O [registro da inspeção](reports/data_inspection.json) documenta as checagens e limitações. O [manifesto do recorte](reports/dataset_manifest.json) registra a divisão e os hashes dos arquivos observados no Colab. A execução integral da versão consolidada do notebook ainda precisa ser repetida e comparada a esses hashes.

## Recorte preparado

São 4.297 exemplos de chamadas únicas reconhecidas pelo leitor e 1.289 respostas fora dos colchetes. Esta segunda categoria descreve o formato; não significa que todos esses exemplos sejam recusas. A inspeção de uma amostra encontrou tanto ferramentas incompatíveis quanto pedidos de dados faltantes.

Três entradas duplicadas com a mesma resposta foram unificadas, preservando os índices de origem. Registros com pedidos normalizados iguais ou conjuntos idênticos de descrições de ferramentas foram mantidos na mesma divisão. As checagens dessas chaves passaram no Colab. Ferramentas individuais podem aparecer em diferentes divisões; não se trata de um teste de APIs inéditas nem de uma auditoria completa de semelhança semântica.

A leitura das chamadas e a presença dos argumentos obrigatórios foram verificadas no nível superior. Tipos, objetos aninhados, semântica e execução das ferramentas não foram validados por essas checagens. O tamanho em tokens será medido na configuração do modelo, antes de definir o limite de contexto.

## Experimento

- Dados: [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE), com conversas sintéticas supervisionadas e descrições de ferramentas. A ficha declara Apache 2.0.
- Modelo candidato: [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), com licença Apache 2.0.
- Método previsto: ajuste supervisionado com LoRA ou QLoRA.
- Comparação: modelo original e modelo ajustado, usando os mesmos exemplos de avaliação.
- Métricas previstas: acerto da ferramenta, acerto dos argumentos, validade do formato e chamadas indevidas.

A configuração final do treinamento e da avaliação será registrada após medir os tokens e executar o piloto. Os conjuntos de validação e teste preparados devem permanecer reservados durante essas decisões.

## Organização

Os arquivos serão acrescentados conforme cada etapa for executada:

| Pasta | Conteúdo |
| --- | --- |
| `notebooks/` | Inspeção, treinamento e avaliação executados no Colab/Kaggle |
| `src/triunfo/` | Preparação dos dados, avaliação e integração das funções de demonstração |
| `configs/` | Configurações dos experimentos |
| `tests/` | Verificações de preparação dos dados e avaliação |
| `reports/` | Métricas, gráficos e análise dos erros |

## Rastreabilidade

Cada experimento deverá registrar revisão da base e do modelo, IDs das divisões, semente, configuração, ambiente, versão do código e resultados observados. Mudanças no protocolo serão documentadas junto à análise dos resultados.

Treinamento e inferência serão realizados no Colab/Kaggle. Os dados baixados e os pesos ficam fora do Git. A publicação do adaptador no Hugging Face será vinculada ao código e ao experimento correspondentes.

## Limites

O ToolACE fornece exemplos de chamadas e respostas simuladas; não fornece integrações prontas com os serviços mencionados. A primeira demonstração usará funções de teste com resultados controlados.

O treinamento inicial considera dados em inglês. Desempenho em português precisará de avaliação própria.
