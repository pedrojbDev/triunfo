# Reprodução e arquivos persistentes

## Sem modelos no computador local

Os testes em `tests/` exercitam apenas o leitor e as métricas, com a biblioteca padrão do Python. O ambiente local não precisa de PyTorch, Transformers ou pesos. Treino e inferência do experimento usam uma T4 no Colab.

## Dados

`notebooks/01_data_inspection.ipynb` contém a preparação do recorte. A revisão do ToolACE e os hashes estão em `reports/dataset_manifest.json`. A reprodução com biblioteca padrão gerou os mesmos três hashes; ver `reports/reproduction_check.json`.

O ZIP preparado contém `train.jsonl`, `validation.jsonl`, `test.jsonl` e `manifest.json`. O treinamento usa somente o treino. O tokenizer foi medido no treino antes da escolha do contexto. O teste foi preservado até o protocolo final.

## Treinamento

`notebooks/03_lora_training.ipynb` reúne as etapas necessárias numa sessão nova: montar Drive, restaurar dados, conferir ambiente, carregar modelo e LoRA, preparar labels e treinar. O notebook é uma consolidação das células executadas; a sequência consolidada não foi retreinada depois da organização. Os resultados publicados vêm da execução acompanhada, não de uma execução inventada do notebook reorganizado.

As versões foram observadas com Python 3.13.16, PyTorch 2.11.0+cu130, Transformers 5.20.2, PEFT 0.21.2, Accelerate 1.15.0 e Datasets 4.8.5. O torchao 0.10.0 da imagem precisou ser removido; quantização não foi utilizada. `requirements-colab.txt` registra as bibliotecas adicionais, sem substituir o PyTorch da imagem.

Os checkpoints e o adaptador ficam no Drive em `Triunfo/runs/lora_epoch1_recovery`. Não sobrescrever uma execução concluída para reproduzir outra; usar outra pasta e manter sua identidade nos registros.

## Avaliação executada

`notebooks/Triunfo.ipynb` preserva o fluxo de avaliação. As etapas compartilham o estado da sessão e algumas só devem ser executadas uma vez. É um registro explicável de execução, não um comando genérico que recria todos os resultados com “Executar tudo”.

A retomada de sessão carrega o adaptador já treinado com `PeftModel.from_pretrained`; a inicialização de LoRA novo não recupera pesos treinados. A geração salva cada caso no Drive e confere protocolo e pesos antes de retomar.

O teste final inclui 558 pares. As métricas de chamada usam 444 pares; os outros 114 têm observações descritivas. Os arquivos completos estão em `reports/base_test558.json` e `reports/finetuned_test558.json`.

A inferência greedy reduz a variação de amostragem, mas não garante identidade bit a bit entre GPUs, versões e implementações numéricas diferentes. Não há imagem de ambiente nem garantia de acesso contínuo a GPU gratuita.
