import re

def detect_and_preserve_pii(input_text: str) -> str:
    """
    Detecta e preserva PII substituindo por identificadores únicos.
    """
    pii_patterns = {
        "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
        "CNPJ": r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",
        "Telefone": r"\b(\+?\d{1,3})?\s?\(?\d{2,3}\)?\s?\d{4,5}-?\d{4}\b",
        "E-mail": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "Endereço": r"\b(rua|avenida|praça|travessa|alameda)\s.*?\d+\b",
        "Gênero": r"\b(masculino|feminino|não-binário|outro)\b",
        "Raça": r"\b(branco|preto|pardo|amarelo|indígena)\b",
    }

    for label, pattern in pii_patterns.items():
        input_text = re.sub(pattern, f"[{label} PRESERVADO]", input_text)

    return input_text

def check_bank_name(input_text: str) -> str:
    """
    Verifica se a pergunta menciona um banco que não seja o Itaú e insere o nome dos bancos permitidos.
    """
    allowed_banks = ["Itaú"]
    bank_patterns = {
        "Bradesco": r"\bBradesco\b",
        "Santander": r"\bSantander\b",
        "Banco do Brasil": r"\bBanco do Brasil\b",
        "Caixa": r"\bCaixa\b",
        "Nubank": r"\bNubank\b",
        "Inter": r"\bInter\b",
        "BTG Pactual": r"\bBTG Pactual\b",
    }

    for bank, pattern in bank_patterns.items():
        if re.search(pattern, input_text, re.IGNORECASE):
            if bank not in allowed_banks:
                allowed_banks_str = ", ".join(allowed_banks)
                return f"Não consigo te ajudar se o assunto não for relacionado aos seguintes bancos: {allowed_banks_str}."

    return input_text
