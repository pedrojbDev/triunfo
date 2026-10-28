# Protocolo inicial de avaliação

A comparação usa a mesma revisão do modelo, instrução, seleção de exemplos e política de geração antes e depois do ajuste. O teste permanece reservado.

## Chamadas únicas

- `parseable_call`: uma chamada de ferramenta disponível, entre colchetes, com argumentos nomeados e literais interpretáveis pelo leitor.
- `tool_correct`: chamada interpretável com o mesmo nome de ferramenta da referência.
- `call_exact`: ferramenta correta e argumentos iguais ao gabarito após serialização JSON com chaves ordenadas. A ordem dos argumentos é ignorada; valores são comparados estritamente. Booleanos e números não são intercambiáveis.

Referências não interpretáveis provocam erro explícito; não são omitidas silenciosamente. Chamadas múltiplas, texto livre e outras sintaxes não são chamadas válidas nesse protocolo de chamada única. O leitor não executa ferramentas nem valida tipos ou objetos contra todos os esquemas.

Estas métricas não comprovam atendimento semântico ao pedido. O piloto8621 inclui uma data absoluta ausente do contexto do pedido; essa limitação deve acompanhar a análise de correspondência exata. Não ajustar o gabarito ou remover o exemplo para melhorar o resultado.

## Respostas fora dos colchetes

O campo de formato não constitui anotação semântica de recusa ou esclarecimento. Não interpretar ausência de chamada reconhecida como uma recusa correta. A avaliação desse grupo precisa ser relatada separadamente, com limites e análise de erros.

## Piloto

O primeiro caso foi escolhido pela ordem do arquivo de validação, condicionado ao formato de chamada única. Não constitui uma estimativa agregada. A primeira latência inclui aquecimento e não representa a latência típica.

## Testes do avaliador

Execute `python3 -m unittest discover -s tests -v`. Os testes cobrem a chamada inválida observada, nomes com espaços, ordem dos argumentos, valores extras, booleanos, referências não suportadas e rejeição de múltiplas chamadas ou expressões. Não carregam modelos.
