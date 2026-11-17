
from ai_recipes import generate_recipes

test_inventory = [
    (1, "Chicken breast", "Freezer", 2, "lbs", "Meat", None, None),
    (2, "Spinach", "Fridge", 1, "package", "Vegetables", None, None),
    (3, "Rice", "Pantry", 2, "cups", "Grains", None, None),
    (4, "Eggs", "Fridge", 12, "items", "Dairy", None, None),
]

recipes = generate_recipes(test_inventory)

print(recipes)
