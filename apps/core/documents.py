import re


def digits_only(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def normalize_tax_id(value: str) -> str:
    normalized = digits_only(value)
    if len(normalized) not in {11, 14}:
        raise ValueError("CPF ou CNPJ deve conter 11 ou 14 dígitos.")
    return normalized
