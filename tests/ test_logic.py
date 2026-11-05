from logic import calculate_price


def test_calculate_price_default():
    result = calculate_price(qty=1000, pages=4, price_per_sheet=10.0)
    assert result == 26250.0


def test_calculate_price_small_qty():
    result = calculate_price(qty=100, pages=4, price_per_sheet=10.0)
    assert result == 2625.0


def test_calculate_price_rounding():
    result = calculate_price(qty=333, pages=4, price_per_sheet=4.5)
    assert result == 3932.61


def test_calculate_price_zero_qty():
    result = calculate_price(qty=0, pages=4, price_per_sheet=10.0)
    assert result == 0.0


def test_calculate_price_float_qty():
    result = calculate_price(qty=10.5, pages=4, price_per_sheet=10.0)
    assert result == 275.62


def test_calculate_price_large_qty():
    result = calculate_price(qty=100000, pages=4, price_per_sheet=10.0)
    assert result == 2625000.0
