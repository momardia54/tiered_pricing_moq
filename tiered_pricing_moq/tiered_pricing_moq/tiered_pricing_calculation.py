import frappe
from frappe import _

# Server Script: Before Save for Quotation
def apply_tiered_pricing(doc, method):
    for item in doc.items:
        # Fetch item data from the Item doctype
        item_data = frappe.db.get_value(
            "Item",
            item.item_code,
            ["custom_is_tiered", "custom_tier_size", "custom_reduction_per_tier"],
            as_dict=True
        )

        # Skip if tiered pricing is not enabled
        if not item_data.custom_is_tiered:
            continue
        
        # Fetch the flat rate price from the Item Price doctype
        flat_rate_price = frappe.db.get_value(
            "Item Price",
            {"item_code": item.item_code, "selling": 1},  # Adjust query for buying if needed
            "custom_flat_rate_price"
        ) or 0  # Default to 0 if no flat rate price is defined

        # Fetch custom field values
        tier_size = item_data.custom_tier_size or 50  # Default tier size is 50
        reduction_rate = item_data.custom_reduction_per_tier or 8  # Default reduction is 8%
        base_price = item.rate  # Use the item rate as the base price

        # Ensure reduction rate is a decimal
        discount_rate = reduction_rate / 100.0
        max_discount_rate = 0.4  # Maximum allowed discount (40%)

        # Calculate capped price
        capped_price = base_price * (1 - max_discount_rate)

        # Calculate total amount based on the tiered pricing logic
        pages = item.qty or 0  # Number of units
        total_amount = 0  # Total cumulative amount

        if flat_rate_price > 0 and pages > 0:
            # Apply flat rate to the first 10 UOM only if flat_rate_price is defined
            if pages <= 10:
                total_amount = flat_rate_price  # Apply flat rate for all pages if <= 10
            else:
                total_amount += flat_rate_price  # Apply flat rate for the first 10 pages
                pages -= 10  # Deduct the flat-rate-covered pages

        # Calculate pricing for remaining UOM beyond the first 10
        remaining_pages = max(0, pages)

        tier_number = 1
        while remaining_pages > 0:
            # Calculate pages in the current tier
            pages_in_tier = min(tier_size, remaining_pages)

            # Calculate the discounted tier price
            tier_price = base_price * ((1 - discount_rate) ** tier_number)

            # Cap the tier price to the maximum allowed discount
            tier_price = max(tier_price, capped_price)

            # Add the price for the current tier
            total_amount += tier_price * pages_in_tier

            # Move to the next tier
            remaining_pages -= pages_in_tier
            tier_number += 1

        # Update the item's rate and amount fields
        item.rate = total_amount / (item.qty or 1)  # Avoid division by zero
        item.amount = total_amount
