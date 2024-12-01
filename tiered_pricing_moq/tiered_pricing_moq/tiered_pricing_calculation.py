# Server Script: Before Save for Quotation
def apply_tiered_pricing(doc, method):
    for item in doc.items:
        # Check if tiered pricing is enabled for this item
        item_data = frappe.db.get_value(
            "Item", item.item_code,
            ["custom_is_tiered", "custom_tier_size", "custom_reduction_per_tier", "custom_flat_rate_price"],
            as_dict=True
        )
        
        if not item_data or not item_data.custom_is_tiered:
            # Skip if tiered pricing is not enabled
            continue
        
        # Fetch custom field values
        tier_size = item_data.custom_tier_size or 50  # Default tier size is 50
        reduction_rate = item_data.custom_reduction_per_tier or 8  # Default reduction is 8%
        flat_rate_price = item_data.custom_flat_rate_price or 0  # Flat rate price for the first tier
        base_price = item.rate  # Use the item rate as the base price

        # Ensure reduction rate is a decimal
        discount_rate = reduction_rate / 100.0
        max_discount_rate = 0.4  # Maximum allowed discount (40%)

        # Calculate capped price
        capped_price = base_price * (1 - max_discount_rate)

        # Calculate total amount based on the tiered pricing logic
        pages = item.qty or 0  # Number of units
        total_amount = 0  # Total cumulative amount

        if pages <= 10 and flat_rate_price > 0:
            # Flat rate for quantities less than or equal to 10 if applicable
            total_amount = flat_rate_price
        else:
            # Flat rate for the first 10 UOM (if applicable)
            if flat_rate_price > 0:
                total_amount += flat_rate_price
                pages -= 10

            # Remaining UOM beyond the first 10
            remaining_pages = max(0, pages)

            # Iterate through tiers
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
