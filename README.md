# Triunfo

Fine-tuning de um LLM pequeno para gerar chamadas de ferramentas a partir de pedidos em linguagem natural.

O projeto investiga três comportamentos: escolher a ferramenta correta, preencher seus argumentos e reconhecer pedidos que as ferramentas disponíveis não atendem.

## Estado atual

Preparação do projeto e inspeção inicial dos dados. Ainda não há modelo ajustado ou resultados experimentais.

## Experimento

- Dados: [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE), com conversas sintéticas supervisionadas e descrições de ferramentas. A ficha declara Apache 2.0.
- Modelo candidato: [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), com licença Apache 2.0.
- Método previsto: ajuste supervisionado com LoRA ou QLoRA.
- Comparação: modelo original e modelo ajustado, usando os mesmos exemplos de avaliação.
- Métricas previstas: acerto da ferramenta, acerto dos argumentos, validade do formato e chamadas indevidas.

A revisão dos dados, as divisões de treino/validação/teste e a configuração final serão registradas após a inspeção. As conversas e os esquemas semelhantes de ferramentas precisam ser considerados nessa separação.

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
