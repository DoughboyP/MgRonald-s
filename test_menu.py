import pytest
from menu import Ingredient, MenuItem, Order, MENU


# ---------------------------------------------------------------------------
# Ingredient tests
# ---------------------------------------------------------------------------

def test_ingredient_str_local_fresh():
    ing = Ingredient("tomato", "Happy Acres Farm")
    assert "fresh" in str(ing)
    assert "local" in str(ing)
    assert "Happy Acres Farm" in str(ing)


def test_ingredient_str_not_fresh():
    ing = Ingredient("frozen patty", "Generic Supplier", is_local=False, is_fresh=False)
    assert "pre-made" in str(ing)
    assert "local" not in str(ing)


# ---------------------------------------------------------------------------
# MenuItem tests
# ---------------------------------------------------------------------------

def _make_item(local: bool = True, fresh: bool = True, special: bool = False) -> MenuItem:
    return MenuItem(
        name="Test Item",
        description="A test item",
        price=5.00,
        has_special_ingredient=special,
        special_ingredient_name="Magic Dust" if special else "",
        ingredients=[
            Ingredient("ingredient A", "Farm A", is_local=local, is_fresh=fresh),
            Ingredient("ingredient B", "Farm B", is_local=local, is_fresh=fresh),
        ],
    )


def test_farm_to_table_true_when_all_local():
    assert _make_item(local=True).is_farm_to_table() is True


def test_farm_to_table_false_when_any_nonlocal():
    item = MenuItem(
        name="Mixed",
        description="",
        price=1.0,
        ingredients=[
            Ingredient("local veg", "Local Farm", is_local=True),
            Ingredient("imported spice", "Overseas Co.", is_local=False),
        ],
    )
    assert item.is_farm_to_table() is False


def test_all_fresh_true():
    assert _make_item(fresh=True).is_all_fresh() is True


def test_all_fresh_false_when_any_stale():
    item = MenuItem(
        name="Stale",
        description="",
        price=1.0,
        ingredients=[
            Ingredient("fresh herb", "Farm A", is_fresh=True),
            Ingredient("pre-made sauce", "Factory", is_fresh=False),
        ],
    )
    assert item.is_all_fresh() is False


def test_display_includes_farm_to_table_badge():
    item = _make_item(local=True, fresh=True)
    assert "Farm-to-table" in item.display()


def test_display_includes_fresh_badge():
    item = _make_item(fresh=True)
    assert "Made fresh daily" in item.display()


def test_display_includes_special_ingredient():
    item = _make_item(special=True)
    output = item.display()
    assert "Magic Dust" in output
    assert "special ingredient" in output


def test_display_no_special_ingredient_badge_when_false():
    item = _make_item(special=False)
    assert "special ingredient" not in item.display()


def test_display_shows_price():
    item = _make_item()
    assert "5.00" in item.display()


# ---------------------------------------------------------------------------
# MENU sanity checks
# ---------------------------------------------------------------------------

def test_menu_not_empty():
    assert len(MENU) > 0


def test_all_menu_items_have_ingredients():
    for item in MENU:
        assert len(item.ingredients) > 0, f"{item.name} has no ingredients"


def test_all_menu_items_farm_to_table():
    for item in MENU:
        assert item.is_farm_to_table(), f"{item.name} is not farm-to-table"


def test_all_menu_items_fresh():
    for item in MENU:
        assert item.is_all_fresh(), f"{item.name} has non-fresh ingredients"


def test_special_items_have_special_ingredient_name():
    for item in MENU:
        if item.has_special_ingredient:
            assert item.special_ingredient_name, (
                f"{item.name} is flagged special but has no special_ingredient_name"
            )


# ---------------------------------------------------------------------------
# Order tests
# ---------------------------------------------------------------------------

def test_order_total_empty():
    order = Order()
    assert order.total() == 0.0


def test_order_total_with_items():
    order = Order()
    order.add(_make_item())   # 5.00
    order.add(_make_item())   # 5.00
    assert order.total() == pytest.approx(10.00)


def test_order_receipt_contains_total():
    order = Order()
    order.add(_make_item())
    receipt = order.receipt()
    assert "TOTAL" in receipt
    assert "5.00" in receipt


def test_order_receipt_contains_item_name():
    order = Order()
    order.add(_make_item())
    assert "Test Item" in order.receipt()


def test_order_receipt_branding():
    order = Order()
    receipt = order.receipt()
    assert "MgRonald" in receipt
