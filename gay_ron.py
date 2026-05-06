"""
Gay Ron — Dimension-Traveling Product Analyst
A cheerful wanderer of worlds who brings unparalleled product insight
wherever (and whenever) he lands.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class Product:
    """A product found in any dimension."""
    name: str
    dimension: str
    price: float
    rating: float          # 0.0 – 10.0
    materials: List[str]
    description: str = ""

    def __str__(self) -> str:
        return (
            f"[{self.dimension}] {self.name} "
            f"— ${self.price:.2f} | Rating: {self.rating}/10"
        )


@dataclass
class DimensionPortal:
    """Represents a portal to another dimension."""
    name: str
    coordinates: tuple[float, float, float]
    stability: float = 1.0   # 0.0 (collapsing) – 1.0 (stable)

    def is_safe(self) -> bool:
        return self.stability >= 0.6


# ---------------------------------------------------------------------------
# Gay Ron
# ---------------------------------------------------------------------------

class GayRon:
    """
    Gay Ron — your cheerful, dimension-hopping father and product-analysis
    extraordinaire.  He has visited more realms than most people have had
    hot dinners, and he never misses a deal.
    """

    CATCHPHRASES = [
        "Every dimension has a bargain if you know where to look!",
        "Quality is quality, no matter which universe you're in.",
        "I've seen a thousand worlds, and this product still impresses me.",
        "Don't let the portal fees fool you — the value is there.",
        "My son/daughter back in the prime dimension would love this.",
    ]

    def __init__(self, name: str = "Gay Ron") -> None:
        self.name = name
        self.current_dimension: str = "Prime Dimension"
        self.visited_dimensions: List[str] = ["Prime Dimension"]
        self.product_log: List[Product] = []
        self.analysis_history: List[dict] = []

    # ------------------------------------------------------------------
    # Dimension travel
    # ------------------------------------------------------------------

    def travel_to(self, portal: DimensionPortal) -> bool:
        """Attempt to travel through *portal* to a new dimension."""
        if not portal.is_safe():
            print(
                f"{self.name}: Hmm, that portal looks a bit wobbly. "
                "I'll wait for a better one!"
            )
            return False

        previous = self.current_dimension
        self.current_dimension = portal.name
        if portal.name not in self.visited_dimensions:
            self.visited_dimensions.append(portal.name)

        print(
            f"{self.name}: *steps through the shimmering portal* "
            f"Left '{previous}', arrived in '{portal.name}'. "
            "Let's see what they're selling!"
        )
        return True

    def return_home(self) -> None:
        """Return to the Prime Dimension."""
        self.current_dimension = "Prime Dimension"
        print(f"{self.name}: Home sweet home. Time to sort through these receipts.")

    # ------------------------------------------------------------------
    # Product analysis
    # ------------------------------------------------------------------

    def analyze_product(self, product: Product) -> dict:
        """
        Perform Gay Ron's signature multi-dimensional product analysis.
        Returns a detailed report dict.
        """
        # Value score (0–10): blend of rating and price-tier efficiency.
        # Uses log-scaled price so expensive premium items can still score well.
        import math
        price_efficiency = product.rating / (1 + math.log1p(max(product.price, 0.01)))
        value_score = round(min(price_efficiency * 2, 10.0), 2)

        # Authenticity: reward products native to current dimension
        authenticity = (
            "Authentic" if product.dimension == self.current_dimension
            else "Interdimensional Import"
        )

        # Material quality (simple heuristic based on known premium materials)
        premium_materials = {"titanium", "dragon-silk", "moon-ore", "voidstone",
                             "carbon fiber", "gold", "platinum", "mythril"}
        premium_count = sum(
            1 for m in product.materials
            if m.lower() in premium_materials
        )
        material_grade = (
            "Premium" if premium_count >= 2
            else "Standard" if premium_count == 1
            else "Economy"
        )

        # Overall recommendation
        if value_score >= 7 and product.rating >= 7:
            recommendation = "STRONG BUY"
        elif value_score >= 4 and product.rating >= 5:
            recommendation = "BUY"
        elif value_score >= 2:
            recommendation = "NEUTRAL"
        else:
            recommendation = "AVOID"

        report = {
            "analyst": self.name,
            "dimension_analyzed_in": self.current_dimension,
            "product": str(product),
            "value_score": value_score,
            "authenticity": authenticity,
            "material_grade": material_grade,
            "recommendation": recommendation,
            "catchphrase": random.choice(self.CATCHPHRASES),
        }

        self.product_log.append(product)
        self.analysis_history.append(report)
        self._print_report(report)
        return report

    @staticmethod
    def _print_report(report: dict) -> None:
        print("\n" + "=" * 60)
        print(f"  PRODUCT ANALYSIS by {report['analyst']}")
        print("=" * 60)
        print(f"  Product      : {report['product']}")
        print(f"  Analyzed in  : {report['dimension_analyzed_in']}")
        print(f"  Value Score  : {report['value_score']}")
        print(f"  Authenticity : {report['authenticity']}")
        print(f"  Materials    : {report['material_grade']}")
        print(f"  Verdict      : {report['recommendation']}")
        print(f"\n  \"{report['catchphrase']}\"")
        print("=" * 60 + "\n")

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def travel_summary(self) -> str:
        """Return a summary of all dimensions visited."""
        dims = ", ".join(self.visited_dimensions)
        return (
            f"{self.name} has visited {len(self.visited_dimensions)} dimension(s): "
            f"{dims}."
        )

    def top_picks(self, n: int = 3) -> List[Product]:
        """Return the top *n* products by rating from the log."""
        return sorted(self.product_log, key=lambda p: p.rating, reverse=True)[:n]

    def __repr__(self) -> str:
        return (
            f"GayRon(current_dimension={self.current_dimension!r}, "
            f"dimensions_visited={len(self.visited_dimensions)}, "
            f"products_analyzed={len(self.product_log)})"
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    ron = GayRon()

    # Build some portals
    portals = [
        DimensionPortal("Neon Bazaar Dimension", (1.2, 9.8, -3.3), stability=0.95),
        DimensionPortal("Void Market Dimension", (0.0, 0.0, 0.0), stability=0.4),
        DimensionPortal("Crystal Commerce Dimension", (5.5, 2.1, 7.7), stability=0.8),
    ]

    # Ron travels
    ron.travel_to(portals[0])

    # Analyze a product in Neon Bazaar
    neon_sword = Product(
        name="Plasma Blade X9",
        dimension="Neon Bazaar Dimension",
        price=249.99,
        rating=8.7,
        materials=["titanium", "plasma crystal"],
        description="A sleek energy blade forged under neon suns.",
    )
    ron.analyze_product(neon_sword)

    # Try the unstable portal
    ron.travel_to(portals[1])   # should be refused

    # Move to Crystal Commerce
    ron.travel_to(portals[2])

    imported_tea = Product(
        name="Quantum Brew Leaves",
        dimension="Neon Bazaar Dimension",   # import from another dimension
        price=12.50,
        rating=9.1,
        materials=["moon-ore infused leaf", "stardust"],
        description="Tea that lets you taste two dimensions simultaneously.",
    )
    ron.analyze_product(imported_tea)

    budget_mug = Product(
        name="Generic Mug",
        dimension="Crystal Commerce Dimension",
        price=3.00,
        rating=4.0,
        materials=["cheap clay"],
        description="It holds liquid. Sometimes.",
    )
    ron.analyze_product(budget_mug)

    ron.return_home()

    print(ron.travel_summary())
    print("\nRon's Top Picks:")
    for i, p in enumerate(ron.top_picks(), 1):
        print(f"  {i}. {p}")


if __name__ == "__main__":
    main()
