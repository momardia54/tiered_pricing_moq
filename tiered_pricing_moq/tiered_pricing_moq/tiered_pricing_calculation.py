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
        if not item_data or not item_data.custom_is_tiered:
            continue

        # Fetch the flat rate price from the Item Price doctype
        flat_rate_price = frappe.db.get_value(
            "Item Price",
            {"item_code": item.item_code, "selling": 1},  # Adjust query for buying if needed
            "custom_flat_rate_price"
        ) or 0

        # Fetch custom field values
        tier_size = item_data.custom_tier_size
        reduction_rate = item_data.custom_reduction_per_tier

        # Fetch the base price
        base_price = frappe.db.get_value(
            "Item Price",
            {"item_code": item.item_code, "selling": 1},
            "price_list_rate"
        )

        if not base_price:
            frappe.throw(_("Base price not found for item {0}.").format(item.item_code))

        # Ensure reduction rate is a decimal
        discount_rate = reduction_rate / 100.0
        max_discount_rate = 0.4  # Maximum allowed discount (40%)

        # Calculate capped price
        capped_price = base_price * (1 - max_discount_rate)

        # Calculate total amount based on the tiered pricing logic
        pages = item.qty
        item_total = 0

        if flat_rate_price > 0 and pages > 0:
            if pages <= 10:
                item_total = flat_rate_price
                pages = 0
            else:
                item_total += flat_rate_price
                pages -= 10

        # Calculate pricing for remaining UOM beyond the first 10
        remaining_pages = max(0, pages)

        tier_number = 0
        while remaining_pages > 0:
            pages_in_tier = min(tier_size, remaining_pages)
            tier_price = base_price * (1 - (discount_rate * tier_number))
            tier_price = max(tier_price, capped_price)
            item_total += tier_price * pages_in_tier
            remaining_pages -= pages_in_tier
            tier_number += 1

        # Set the rate and rely on ERPNext for amount calculation
        item.rate = round(item_total / (item.qty or 1))

    # Trigger recalculation of taxes and totals
    doc.run_method("calculate_taxes_and_totals")
