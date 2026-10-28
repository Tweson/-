def calculate_price(qty, pages, price_per_sheet):
    sheets = (qty * pages) / 2
    sheets = sheets * 1.05
    cost = sheets * price_per_sheet
    total = cost * 1.25
    return round(total, 2)