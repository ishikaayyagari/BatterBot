# Formatting of ingredients

OMIT_UNITS = {"piece", "pieces", "unit", "units", "count"}

def format_ingredient(amount, unit):
    if unit is None:
        return str(amount)

    if unit.lower() in OMIT_UNITS:
        return str(amount)

    return f"{amount} {unit}"
