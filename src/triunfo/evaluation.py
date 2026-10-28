"""Leitura estrita de chamadas; não executa ferramentas nem valida semântica."""

import ast
import json


def parse_single_call(text, tools):
    """Retorna uma chamada nomeada com valores literais ou None.

    Texto livre, chamadas múltiplas e sintaxes não suportadas retornam None.
    Isso não classifica texto livre como uma recusa correta.
    """
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        return None
    interior = text[1:-1].strip()
    for tool in sorted(tools, key=lambda item: len(item["name"]), reverse=True):
        name = tool["name"]
        if not interior.startswith(name + "("):
            continue
        try:
            node = ast.parse("function" + interior[len(name):], mode="eval").body
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "function"
            ):
                return None
            if node.args or any(argument.arg is None for argument in node.keywords):
                return None
            arguments = {
                argument.arg: ast.literal_eval(argument.value)
                for argument in node.keywords
            }
            if len(arguments) != len(node.keywords):
                return None
            json.dumps(arguments, allow_nan=False)
            return {"name": name, "arguments": arguments}
        except (SyntaxError, ValueError, TypeError, RecursionError):
            return None
    return None


def score_call(prediction, reference, tools):
    """Compara à referência; igualdade não comprova correção no mundo real.

    Ignora a ordem das chaves. Mantém comparação JSON estrita de valores,
    inclusive distinções entre números, textos e booleanos.
    """
    expected = parse_single_call(reference, tools)
    if expected is None:
        raise ValueError("Referência fora do protocolo de chamada única.")
    observed = parse_single_call(prediction, tools)
    tool_correct = observed is not None and observed["name"] == expected["name"]
    call_exact = tool_correct and json.dumps(
        observed["arguments"], sort_keys=True, ensure_ascii=False, allow_nan=False
    ) == json.dumps(
        expected["arguments"], sort_keys=True, ensure_ascii=False, allow_nan=False
    )
    return {
        "parseable_call": observed is not None,
        "tool_correct": tool_correct,
        "call_exact": call_exact,
    }
