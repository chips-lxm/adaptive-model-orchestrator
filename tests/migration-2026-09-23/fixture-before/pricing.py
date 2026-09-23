def quote(quantity, delivery="standard"):
    if not isinstance(quantity, int) or quantity < 0:
        raise ValueError("quantity")
    if delivery not in ("standard", "express"):
        raise ValueError("delivery")
    return quantity * 125 + (500 if delivery == "express" else 0)
