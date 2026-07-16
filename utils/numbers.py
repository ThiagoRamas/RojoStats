def formatear_numero(numero: int) -> str:
    return f"{numero:,}".replace(",", ".")


def formatear_variacion(numero: int) -> str:
    if numero > 0:
        return f"+{formatear_numero(numero)}"

    return formatear_numero(numero)