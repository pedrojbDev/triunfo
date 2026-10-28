# Teste final

O protocolo foi fixado após a avaliação de validação e antes de gerar as respostas do teste. A configuração exata e o SHA256 do adaptador estão em configs/final_test_protocol.json.

Avaliar os dois modelos nos 558 exemplos reservados, sem reaproveitar previsões de validação. A métrica primária é correspondência estrita de chamada e argumentos nos 444 exemplos de chamada única; formato e ferramenta são métricas secundárias. As 114 respostas textuais recebem gerações e observações descritivas, sem nota semântica automática. Não combinar os dois grupos em uma acurácia global.

O modelo original usa os mesmos pesos congelados com os adaptadores desativados. O modelo ajustado usa o adaptador persistido após 559 atualizações. Prompt, tokenizer, revisão, geração e avaliador permanecem iguais. Não executar APIs reais.

A revisão qualitativa de 12 exemplos textuais da validação mostrou resultados mistos, incluindo chave fictícia, confusão entre opcional e obrigatório e pedido de parâmetros de uma ferramenta inadequada. Não declarar melhora geral em recusas ou prontidão para automação autônoma.

Não alterar a configuração após ver o resultado de teste. Se o projeto ganhar uma nova versão depois, declarar que este conjunto já foi consultado e não tratar uma comparação posterior nele como novo teste cego.
