import frappe
from frappe import _

# Server Script: Before Save for Quotation
def apply_tiered_pricing(doc, method):
    # Initialize total values
    total_amount = 0
    total_qty = 0

    for item in doc.items:
        # Fetch item data from the Item doctype
        item_data = frappe.db.get_value(
            "Item",
            item.item_code,
            ["custom_is_tiered", "custom_tier_size", "custom_reduction_per_tier"],
            as_dict=True
        )

        # Skip if tiered pricing is not enabled
        if not item_data or not item_data.custom_is_tiered:
            total_amount += item.amount  # Include unchanged item amount
            total_qty += item.qty
            continue

        # Fetch the flat rate price from the Item Price doctype
        flat_rate_price = frappe.db.get_value(
            "Item Price",
            {"item_code": item.item_code, "selling": 1},  # Adjust query for buying if needed
            "custom_flat_rate_price"
        ) or 0  # Default to 0 if no flat rate price is defined

        # Fetch custom field values
        tier_size = item_data.custom_tier_size
        reduction_rate = item_data.custom_reduction_per_tier
        base_price = item.rate  # Use the original rate for calculations

        # Ensure reduction rate is a decimal
        discount_rate = reduction_rate / 100.0
        max_discount_rate = 0.4  # Maximum allowed discount (40%)

        # Calculate capped price
        capped_price = base_price * (1 - max_discount_rate)

        # Calculate total amount based on the tiered pricing logic
        pages = item.qty  # Number of units
        item_total = 0  # Item's cumulative amount

        if flat_rate_price > 0 and pages > 0:
            # Apply flat rate to the first 10 UOM only if flat_rate_price is defined
            if pages <= 10:
                item_total = flat_rate_price  # Apply flat rate for all pages if <= 10
                pages = 0
            else:
                item_total += flat_rate_price  # Apply flat rate for the first 10 pages
                pages -= 10  # Deduct the flat-rate-covered pages

        # Calculate pricing for remaining UOM beyond the first 10
        remaining_pages = max(0, pages)

        tier_number = 1
        while remaining_pages > 0:
            # Calculate pages in the current tier
            pages_in_tier = min(tier_size, remaining_pages)

            # Calculate the discounted tier price
            tier_price = base_price * (1 - (discount_rate * tier_number))

            # Cap the tier price to the maximum allowed discount
            tier_price = max(tier_price, capped_price)

            # Add the price for the current tier
            item_total += tier_price * pages_in_tier

            # Move to the next tier
            remaining_pages -= pages_in_tier
            tier_number += 1

        # Update the item's amount field only
        item.amount = item_total

        # Add the updated item's amount and quantity to the totals
        total_amount += item.amount
        total_qty += item.qty

    # Update the parent document's total and other relevant fields
    doc.total = total_amount
    doc.net_total = total_amount
    doc.total_qty = total_qty

    # Trigger recalculation of taxes and grand total
    doc.run_method("calculate_taxes_and_totals")
