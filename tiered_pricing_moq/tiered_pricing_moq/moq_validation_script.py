import frappe
from frappe import _

def validate_moq(doc, method):
    """
    Validates if the quantity of each item in a transaction meets the minimum order quantity (custom_moq).
    """
    for item in doc.items:
        # Fetch the custom_moq and stock_uom from the Item doctype
        item_details = frappe.db.get_value(
            "Item",
            item.item_code,
            ["custom_moq", "stock_uom"],
            as_dict=True
        )
        
        if item_details:
            # Extract the minimum order quantity and UOM
            min_qty = item_details.get("custom_moq")
            uom = item_details.get("stock_uom") or "units"  # Default to 'units' if UOM is not set
            
            # Check if the quantity is below the minimum order quantity
            if min_qty and item.qty < float(min_qty):
                frappe.throw(
                    _("The minimum order quantity for item {0} is {1} {2}. Please adjust the quantity.")
                    .format(item.item_code, min_qty, uom)
                )
