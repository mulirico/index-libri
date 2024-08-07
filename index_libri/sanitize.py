import re


def sanitize(string_entrada: str) -> str:
    sanitized_str = string_entrada.strip().lower()
    sanitized_str = ' '.join(sanitized_str.split())
    sanitized_str = re.sub(r'[!@#$%&?]', '', sanitized_str)

    return sanitized_str
