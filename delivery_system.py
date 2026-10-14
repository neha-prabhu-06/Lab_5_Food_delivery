"""Food delivery order queue manager."""

import json
from datetime import datetime

DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]

# Global state used by the simple lab script.
STATE = {
    "orders": {},
    "next_id": 1,
    "menu": {},
}


def create_order(customer, items, order_history=None):
    """Create a validated order and return its generated order ID."""
    if order_history is None:
        order_history = []

    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name cannot be empty")

    if not isinstance(items, list) or not items:
        raise ValueError("An order must contain at least one item")

    total = 0

    for item in items:
        if not isinstance(item, str) or item not in STATE["menu"]:
            raise ValueError(f"Unknown menu item: {item}")
        total += STATE["menu"][item]

    order_id = STATE["next_id"]
    STATE["orders"][order_id] = {
        "customer": customer.strip(),
        "items": items.copy(),
        "total": total,
        "status": "placed"
    }

    order_history.append(order_id)
    STATE["next_id"] += 1

    return order_history[-1]


def update_order_status(order_id, status):
    """Update an existing order to a valid delivery status."""
    if order_id not in STATE["orders"]:
        raise ValueError(f"Order ID {order_id} does not exist")

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid order status: {status}")

    STATE["orders"][order_id]["status"] = status


def validate_menu(menu_data):
    """Validate menu data loaded from JSON."""
    if not isinstance(menu_data, dict) or not menu_data:
        raise ValueError("Menu configuration must be a non-empty JSON object")

    for name, price in menu_data.items():
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(price, (int, float))
            or isinstance(price, bool)
            or price < 0
        ):
            raise ValueError(
                "Menu items must have non-empty names and "
                "non-negative numeric prices"
            )


def read_menu_config(file="menu.json"):
    """Load the menu from JSON, or use the default menu if loading fails."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            loaded_menu = json.load(f)

        validate_menu(loaded_menu)

        STATE["menu"] = loaded_menu

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Could not load menu: {e}. Using default menu.")
        STATE["menu"] = DEFAULT_MENU.copy()


def daily_revenue():
    """Return total revenue from delivered orders."""
    revenue = 0

    for order in STATE["orders"].values():
        if order["status"] == "delivered":
            revenue += order["total"]

    return revenue


def backup_orders(file="orders.json"):
    """Back up current orders to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(STATE["orders"], f, indent=4)


def is_positive_integer_string(value):
    """Return True when value is a positive integer stored as a string."""
    return isinstance(value, str) and value.isdigit() and int(value) > 0


def validate_order_items(items):
    """Validate restored order items against the loaded menu."""
    if not isinstance(items, list) or not items:
        raise ValueError("Order must contain at least one item")

    for item in items:
        if not isinstance(item, str) or item not in STATE["menu"]:
            raise ValueError(f"Invalid restored menu item: {item}")


def validate_order_record(order_id, order):
    """Validate one order loaded from a JSON backup."""
    if not is_positive_integer_string(order_id):
        raise ValueError(f"Invalid order ID: {order_id}")

    if not isinstance(order, dict):
        raise ValueError(f"Invalid order data for ID {order_id}")

    customer = order.get("customer")
    items = order.get("items")
    total = order.get("total")
    status = order.get("status")

    if not isinstance(customer, str) or not customer.strip():
        raise ValueError(f"Invalid customer for ID {order_id}")

    validate_order_items(items)

    if (
        not isinstance(total, (int, float))
        or isinstance(total, bool)
        or total < 0
    ):
        raise ValueError(f"Invalid total for ID {order_id}")

    expected_total = sum(STATE["menu"][item] for item in items)
    if total != expected_total:
        raise ValueError(f"Incorrect total for ID {order_id}")

    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status for ID {order_id}")


def restore_orders(file="orders.json"):
    """Restore orders from a validated JSON backup."""
    with open(file, "r", encoding="utf-8") as f:
        saved_orders = json.load(f)

    if not isinstance(saved_orders, dict):
        raise ValueError("Invalid order backup format")

    restored_orders = {}

    for order_id, order in saved_orders.items():
        validate_order_record(order_id, order)
        restored_orders[int(order_id)] = order

    STATE["orders"] = restored_orders
    STATE["next_id"] = max(STATE["orders"].keys(), default=0) + 1


def print_queue():
    """Print the current order queue."""
    print("Order queue at", datetime.now())

    for order_id, order in STATE["orders"].items():
        print(
            order_id,
            order["customer"],
            order["status"],
            order["total"]
        )


def main():
    """Run a small demonstration of the order queue workflow."""
    read_menu_config()

    a = create_order("Asha", ["pizza", "coke"])
    b = create_order("Ravi", ["burger", "fries"])
    c = create_order("Meera", ["coke"])

    update_order_status(a, "delivered")
    update_order_status(b, "cooking")
    update_order_status(c, "delivered")

    # Test invalid order status
    try:
        update_order_status(b, "teleported")
    except ValueError as e:
        print(e)

    # Test nonexistent order ID
    try:
        update_order_status(42, "delivered")
    except ValueError as e:
        print(e)

    print("Revenue today:", daily_revenue())

    backup_orders()
    restore_orders()

    print_queue()


if __name__ == "__main__":
    main()
