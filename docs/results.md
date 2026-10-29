# Resultados e interpretação

O adaptador foi escolhido antes do teste: LoRA rank 16 em q/k/v/o, uma época, mesma instrução e geração greedy. O protocolo do teste foi preservado antes de abrir os exemplos reservados. Nenhum novo treino foi feito para melhorar o resultado nesse conjunto.

| Divisão — chamadas únicas | Original exato | LoRA exato | Diferença |
| --- | ---: | ---: | ---: |
| Validação, 430 exemplos | 156 — 36,28% | 273 — 63,49% | +27,21 p.p. |
| Teste, 444 exemplos | 173 — 38,96% | 280 — 63,06% | +24,10 p.p. |

No teste, 128 exemplos passaram de incorretos para corretos segundo a referência e 21 fizeram o caminho inverso: ganho líquido de 107. A melhora se manteve fora da validação, mas não é uniforme em todos os casos.

## O que melhorou

Na validação, foram corrigidas chamadas com valores de texto sem aspas, respostas com explicações fora do formato exigido e pedidos que antes eram respondidos sem acionar a ferramenta disponível. Alguns casos passaram a preencher corretamente estruturas aninhadas.

O leitor não verifica execução ou semântica. Parte do ganho estrito pode refletir normalização de formato: no recorte preliminar, um ganho veio apenas de inteiros passarem a decimais. Os relatórios mantêm o critério original e não removem esses casos depois de ver os resultados.

## O que permaneceu problemático

A revisão das regressões de validação encontrou omissão de `category="workforce"`, uso de `Tesla` em vez do ticker `TSLA`, perguntas por campos opcionais e representação de 5% como `0.05` onde o schema exige `5`.

Há referências ambíguas: ano ausente no pedido, convenções de sinal e inversão de aeroportos em uma distância potencialmente simétrica. Não mudar o rótulo nem excluir o caso para melhorar a métrica. A lista de regressões e as notas estão em `reports/comparison_validation430_review.json`.

## Respostas textuais

Os dois modelos foram executados nos 129 exemplos textuais da validação e nos 114 do teste. A presença de uma chamada única conhecida foi registrada como observação, sem chamá-la de erro ou acerto automaticamente.

A revisão qualitativa de 12 casos de validação, amostrados com semente 42 antes das gerações, encontrou resultados mistos. Entre as falhas do ajustado estão uma chamada com `p="your_api_key"` sem uma chave fornecida, confusão entre obrigatório e opcional e pedido de parâmetros de uma ferramenta que não atende à tarefa. Há também esclarecimentos adequados e mais específicos.

Essa revisão é descritiva, sem segundo avaliador; não produz uma taxa de acerto populacional. A contagem de chamadas nos textos caiu de 20 para 13 na validação e de 31 para 15 no teste, mas isso não demonstra melhora semântica em recusas.

## O que o projeto demonstra

Ajuste supervisionado de um modelo pequeno, comparação pareada com pesos originais congelados, divisão reprodutível, protocolo fixado antes do teste e recuperação após interrupção de sessão. Não demonstra execução segura de APIs reais, autonomia, desempenho em português ou transferência para ferramentas inéditas.
