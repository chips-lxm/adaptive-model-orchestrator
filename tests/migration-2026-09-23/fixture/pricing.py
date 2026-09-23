def quote(quantity, delivery="standard"):
    if type(quantity) is not int or quantity < 0:
        raise ValueError("quantity")
    if not isinstance(delivery, str):
        raise ValueError("delivery")
    delivery = str.__str__(delivery)
    if delivery not in ("standard", "express"):
        raise ValueError("delivery")
    return quantity * 125 + (500 if delivery == "express" else 0)
