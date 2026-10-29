# Relatórios do Triunfo

## Resultado final

- `test558_summary.json`: resultado nos 558 exemplos reservados; métricas de chamada usam 444 pares.
- `base_test558.json` e `finetuned_test558.json`: previsões individuais, referências, IDs, formatos, tempos e métricas.
- `test_integrity.json`: conferência do ZIP, protocolo, métricas e preservação dos resultados após interrupção.
- `test_progress.json`: estado final da execução, agora concluída.

## Validação e análise

- `comparison_validation430_summary.json`: comparação nas 430 chamadas únicas de validação.
- `comparison_validation430_review.json`: revisão das dez regressões estritas de validação.
- `textual_validation129_summary.json`: observações do leitor nos 129 exemplos em outro formato; não é nota semântica.
- `textual_validation_review12_assessed.json`: parecer qualitativo dos 12 exemplos definidos antes da geração; sem segundo avaliador ou estimativa global de acerto.
- Os JSONs `base_*` e `finetuned_*` correspondentes preservam as previsões completas.

## Dados e treinamento

- `dataset_manifest.json` e `reproduction_check.json`: origem, política de divisão, hashes e reprodução da preparação.
- `colab_environment.json`, `tokenizer_profile.json`, `model_load.json` e `lora_setup.json`: ambiente e configuração observados.
- `training_epoch1_recovery.json`: treino do adaptador avaliado e preservado no Drive.
- `training_epoch1.json` e `training_epoch1_loss.json`: primeira execução, cujos pesos temporários não foram preservados; não é uma segunda época do adaptador final.
- Arquivos de piloto e comparação em 32 casos documentam decisões anteriores; o número de destaque do projeto vem do teste final.

O teste e o leitor mantêm comparação JSON estrita. Não editar referências ou excluir falhas depois de observar os resultados. Os dados brutos e os pesos não ficam nesta pasta.
