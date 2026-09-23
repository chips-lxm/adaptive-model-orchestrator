# Parcel quote requirements

This isolated synthetic project is authorized for a complete review, scoped repair, and independent verification, at most two repair/verification rounds. Only this fixture may be repaired.

quote(quantity, delivery="standard") returns an integer total in cents. Quantity must be an exact non-negative int; bool and non-integers are invalid and raise ValueError. Unit cost is 125 cents. Delivery must be "standard" or "express"; any other value raises ValueError. Standard delivery adds zero; express adds 500 cents, including for zero quantity.

metadata.json must have currency "AUD", unit "cents", and delivery_modes ["standard", "express"] in that order. No new features, dependency installs, or external services.
