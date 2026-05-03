"""
MgRonald's - Farm-to-table fast food with signature special ingredients.
All items made fresh with locally sourced ingredients.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Ingredient:
    name: str
    source: str          # farm or supplier name
    is_local: bool = True
    is_fresh: bool = True

    def __str__(self) -> str:
        freshness = "fresh" if self.is_fresh else "pre-made"
        origin = f"local ({self.source})" if self.is_local else self.source
        return f"{self.name} — {freshness}, from {origin}"


@dataclass
class MenuItem:
    name: str
    description: str
    price: float
    ingredients: List[Ingredient]
    has_special_ingredient: bool = False
    special_ingredient_name: str = ""

    def is_farm_to_table(self) -> bool:
        return all(i.is_local for i in self.ingredients)

    def is_all_fresh(self) -> bool:
        return all(i.is_fresh for i in self.ingredients)

    def display(self) -> str:
        lines = [
            f"  {self.name}  ${self.price:.2f}",
            f"    {self.description}",
        ]
        if self.has_special_ingredient:
            lines.append(f"    ✦ Contains our secret special ingredient: {self.special_ingredient_name}")
        if self.is_farm_to_table():
            lines.append("    🌿 Farm-to-table")
        if self.is_all_fresh():
            lines.append("    🥬 Made fresh daily")
        lines.append("    Ingredients:")
        for ing in self.ingredients:
            lines.append(f"      - {ing}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Farm & supplier definitions
# ---------------------------------------------------------------------------

HAPPY_ACRES = "Happy Acres Farm"
SUNRISE_DAIRY = "Sunrise Dairy Co."
RIVERBED_GREENS = "Riverbed Greens"
MOUNTAIN_MILLS = "Mountain Mills"
LOCAL_SPICE_CO = "Local Spice Co."
BUZZ_BOTANICAL = "Buzz Botanical Gardens"

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU: List[MenuItem] = [
    MenuItem(
        name="The MgRonald Burger",
        description="Double smash patty, heirloom tomato, wild-foraged lettuce, "
                    "house pickles, and our signature Buzz Sauce.",
        price=9.99,
        has_special_ingredient=True,
        special_ingredient_name="Buzz Sauce (espresso-infused aioli with adaptogenic mushrooms)",
        ingredients=[
            Ingredient("grass-fed beef patty (2×)", HAPPY_ACRES),
            Ingredient("heirloom tomato", RIVERBED_GREENS),
            Ingredient("wild-foraged butter lettuce", RIVERBED_GREENS),
            Ingredient("house-fermented pickles", HAPPY_ACRES),
            Ingredient("brioche bun", MOUNTAIN_MILLS),
            Ingredient("Buzz Sauce", BUZZ_BOTANICAL),
        ],
    ),
    MenuItem(
        name="Farm Fries",
        description="Hand-cut russet potatoes, fried in sunflower oil, "
                    "dusted with our house seasoning blend.",
        price=3.99,
        ingredients=[
            Ingredient("russet potatoes", HAPPY_ACRES),
            Ingredient("sunflower oil", LOCAL_SPICE_CO),
            Ingredient("house seasoning blend", LOCAL_SPICE_CO),
        ],
    ),
    MenuItem(
        name="Green Garden Wrap",
        description="Charred corn, roasted peppers, kale, avocado crema, "
                    "quinoa, and jalapeño honey drizzle in a whole-wheat tortilla.",
        price=8.49,
        ingredients=[
            Ingredient("whole-wheat tortilla", MOUNTAIN_MILLS),
            Ingredient("sweet corn", HAPPY_ACRES),
            Ingredient("roasted bell peppers", RIVERBED_GREENS),
            Ingredient("kale", RIVERBED_GREENS),
            Ingredient("avocado", RIVERBED_GREENS),
            Ingredient("quinoa", MOUNTAIN_MILLS),
            Ingredient("jalapeño honey", LOCAL_SPICE_CO),
        ],
    ),
    MenuItem(
        name="Wake-Up Shake",
        description="Thick milkshake blended with cold-brew concentrate and "
                    "lion's mane mushroom extract. The legal kind of buzz.",
        price=5.99,
        has_special_ingredient=True,
        special_ingredient_name="Lion's Mane mushroom extract + cold-brew concentrate",
        ingredients=[
            Ingredient("whole milk", SUNRISE_DAIRY),
            Ingredient("vanilla ice cream", SUNRISE_DAIRY),
            Ingredient("cold-brew concentrate", BUZZ_BOTANICAL),
            Ingredient("lion's mane mushroom extract", BUZZ_BOTANICAL),
        ],
    ),
    MenuItem(
        name="Crispy Herb Chicken Sandwich",
        description="Free-range chicken breast, herb buttermilk brine, "
                    "coleslaw, and comeback sauce on a toasted potato bun.",
        price=10.49,
        ingredients=[
            Ingredient("free-range chicken breast", HAPPY_ACRES),
            Ingredient("buttermilk", SUNRISE_DAIRY),
            Ingredient("cabbage slaw", RIVERBED_GREENS),
            Ingredient("comeback sauce", LOCAL_SPICE_CO),
            Ingredient("potato bun", MOUNTAIN_MILLS),
        ],
    ),
    MenuItem(
        name="Seasonal Soft Serve",
        description="Rotating single-origin soft serve made with whatever "
                    "the farm has in abundance this week.",
        price=2.99,
        ingredients=[
            Ingredient("seasonal fruit purée", HAPPY_ACRES),
            Ingredient("whole milk", SUNRISE_DAIRY),
            Ingredient("cane sugar", LOCAL_SPICE_CO),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Order system
# ---------------------------------------------------------------------------

@dataclass
class Order:
    items: List[MenuItem] = field(default_factory=list)

    def add(self, item: MenuItem) -> None:
        self.items.append(item)

    def total(self) -> float:
        return sum(item.price for item in self.items)

    def receipt(self) -> str:
        lines = ["=" * 40, "        MgRonald's", "  Farm-to-table • Made Fresh Daily", "=" * 40]
        for item in self.items:
            lines.append(f"  {item.name:<28} ${item.price:>5.2f}")
        lines.append("-" * 40)
        lines.append(f"  {'TOTAL':<28} ${self.total():>5.2f}")
        lines.append("=" * 40)
        lines.append("  Thanks for eating fresh! 🌿")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def print_menu() -> None:
    print("\n" + "=" * 50)
    print("           🍔  MgRonald's Menu  🍔")
    print("    Farm-to-table fast food, made fresh daily")
    print("=" * 50)
    for item in MENU:
        print()
        print(item.display())
    print("\n" + "=" * 50)


if __name__ == "__main__":
    print_menu()

    order = Order()
    order.add(MENU[0])   # MgRonald Burger
    order.add(MENU[1])   # Farm Fries
    order.add(MENU[3])   # Wake-Up Shake

    print("\n")
    print(order.receipt())
