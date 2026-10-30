
def check_budget(items, budget):
    """
    Check whether costume materials fit the user's budget.
    """
    total = sum(float(item["price"]) for item in items)

    return {
        "total_cost": round(total, 2),
        "remaining": round(budget - total, 2),
        "within_budget": total <= budget
    }


def match_wardrobe(required_items, owned_items):
    """
    Identify which costume items the user already owns.
    """
    owned = {item.strip().lower() for item in owned_items}

    available = []
    missing = []

    for item in required_items:
        if item.strip().lower() in owned:
            available.append(item)
        else:
            missing.append(item)

    return {
        "available": available,
        "missing": missing
    }
