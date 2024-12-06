import frappe
from frappe import _

def validate_moq(doc, method):
    for item in doc.items:
    # Fetch the Minimum Order Quantity and UOM from the Item Master
    item_details = frappe.db.get_value("Item", item.item_code, ["custom_moq", "stock_uom"], as_dict=True)
    
    if item_details:
        min_qty = item_details.custom_moq
        uom = item_details.stock_uom or "units"  # Default UOM if stock_uom is empty
        
        # Check if the item's quantity is below the minimum
        if min_qty <= item.qty:
            frappe.throw(f"The minimum order quantity for {item.item_code} is {min_qty} {uom}. Please adjust the quantity.")
