---
language:
- en
license: apache-2.0
library_name: peft
pipeline_tag: text-generation
base_model: Qwen/Qwen2.5-1.5B-Instruct
base_model_relation: adapter
datasets:
- Team-ACE/ToolACE
tags:
- lora
- tool-calling
- supervised-fine-tuning
- qwen2
---

# Triunfo

Adaptador LoRA para **Qwen2.5-1.5B-Instruct**, treinado para gerar uma chamada de ferramenta a partir de um pedido e de descrições de funções. O formato é `[tool_name(argument=value)]`, com argumentos em sintaxe literal Python. Os nomes podem incluir espaços ou pontos.

Este repositório contém adaptadores e tokenizer, não uma cópia completa dos pesos originais. Código, dados preparados e avaliação: [pedrojbDev/triunfo](https://github.com/pedrojbDev/triunfo).

## Resultado no teste reservado

| Métrica — 444 chamadas únicas | Modelo original | LoRA |
| --- | ---: | ---: |
| Chamada interpretável pelo leitor | 254/444 — 57,21% | 416/444 — 93,69% |
| Ferramenta correta | 251/444 — 56,53% | 412/444 — 92,79% |
| Ferramenta e argumentos iguais à referência | 173/444 — 38,96% | 280/444 — 63,06% |

Ganho de **24,10 pontos percentuais** em correspondência exata; 128 exemplos corrigidos e 21 regressões. O protocolo foi fixado antes do teste, sem novo treinamento ou escolha de checkpoint pelo resultado de teste. O modelo original foi avaliado com os mesmos pesos congelados e adaptadores desativados.

O teste tem 558 exemplos: 444 chamadas e 114 respostas em outro formato. Os 114 receberam gerações e observações, sem nota semântica automática. Não interpretar 63,06% como desempenho de todos os formatos. Na validação de 430 chamadas, a correspondência exata passou de 36,28% para 63,49%.

A métrica compara valores JSON estritos, ignorando a ordem das chaves. Ela distingue `120` de `120.0`, não executa ferramentas e não mede equivalência funcional ou verdade dos valores. Não se trata de um resultado BFCL.

## Treinamento

- Modelo: `Qwen/Qwen2.5-1.5B-Instruct`, revisão `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.
- Dados: ToolACE, revisão `6bda777c88d21e5a204703c1ee45597a8fa4f734`; conversas sintéticas supervisionadas.
- Recorte: 5.586 exemplos, divididos em 4.469 treino / 559 validação / 558 teste, semente 42.
- Agrupamento: mesmo pedido normalizado ou mesmo conjunto de descrições de ferramentas ficam no mesmo split. Ferramentas individuais e paráfrases podem reaparecer entre splits; não é avaliação de APIs inéditas.
- LoRA: rank 16, alpha 32, dropout 0,05 em `q_proj`, `k_proj`, `v_proj`, `o_proj`; 4.358.144 parâmetros treináveis.
- Uma época, 559 atualizações, batch físico 1, acumulação 8, AdamW, lr 0,0001, 28 passos de aquecimento e redução linear.
- Supervisão somente na resposta e encerramento do chat; contexto de 2.048 tokens sem cortar exemplos do treino, cujo máximo foi 1.711.
- T4, precisão mista float16, adaptadores float32, sem quantização; pico alocado de 6,02 GiB e aproximadamente 35 minutos na execução preservada.

Arquivos `experiment_config.json` e `evaluation_results.json` registram os parâmetros e resultados. O SHA256 dos pesos avaliados está no primeiro arquivo. O `adapter_config.json` da publicação fixa a revisão do modelo original.

## Carregar no Colab/Kaggle com GPU

O ambiente utilizado foi Python 3.13.16, PyTorch 2.11.0+cu130, Transformers 5.20.2, PEFT 0.21.2 e Accelerate 1.15.0. As versões são um registro do experimento; não constituem uma imagem portátil empacotada.

```python
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

repo = "pedrojb04/triunfo"
tokenizer = AutoTokenizer.from_pretrained(repo)
base = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct",
    revision="989aa7980e4cf806f80c7fef2b1adb7bc71aa306",
    dtype=torch.float16,
    device_map={"": 0},
    trust_remote_code=False,
    attn_implementation="sdpa",
)
model = PeftModel.from_pretrained(base, repo, is_trainable=False)
model.eval()

instruction = 'You are a tool-use assistant. Use only the available tools. When calling a tool, return exactly one call inside square brackets: [tool_name(argument=value)]. Copy the tool name exactly, including spaces or dots. Use Python literal syntax for argument values. If no available tool can fulfill the request, explain why. If required information is missing, ask for it. Do not invent missing information or tool results.'
tools = [{
    "name": "calculate_discount_amount",
    "description": "Calculate the discount amount for a price and percentage.",
    "parameters": {
        "type": "dict",
        "properties": {
            "price": {"type": "float"},
            "discount_percentage": {"type": "float"},
        },
        "required": ["price", "discount_percentage"],
    },
}]
messages = [
    {"role": "system", "content": instruction + "\n\nAvailable tools:\n" + json.dumps(tools, ensure_ascii=False, sort_keys=True)},
    {"role": "user", "content": "A jacket costs $120 with a 25% discount. Calculate the discount amount."},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False).to("cuda")
with torch.inference_mode():
    output = model.generate(
        **inputs, do_sample=False, num_beams=1, max_new_tokens=768,
        temperature=1.0, top_p=1.0, top_k=50, use_cache=True,
        eos_token_id=model.generation_config.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )
print(tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

O exemplo mostra como montar a entrada; não é uma nova execução medida neste documento. Não executar a saída com `eval` ou `exec`. O leitor do projeto aceita somente a estrutura literal e não aciona APIs.

## Limitações e uso pretendido

Protótipo de pesquisa e portfólio para estudar ajuste e avaliação de chamadas únicas em inglês. Não é um agente com integrações reais, um sistema validado em português ou uma garantia de parâmetros corretos.

A revisão qualitativa de 12 textos de validação encontrou resultados mistos: há esclarecimentos adequados, mas também uma chamada com chave fictícia, confusão entre argumentos opcionais e obrigatórios e uso indevido de ferramentas. A queda de chamadas reconhecidas nos textos (20 para 13 na validação; 31 para 15 no teste) não prova melhora de recusa. Não há nota semântica para todos esses textos.

Os dados sintéticos podem conter datas subespecificadas e referências ambíguas. A correspondência exata pode rejeitar respostas equivalentes e também aceitar valores inadequados copiados da referência. Nenhuma API descrita nos dados foi executada.

## Licença e atribuição

Adaptador e código sob Apache 2.0. Modelo original: Qwen/Qwen2.5-1.5B-Instruct; dados: Team-ACE/ToolACE, ambos com Apache 2.0 declarada nas respectivas fichas. Consultar as fontes originais e o arquivo LICENSE.
