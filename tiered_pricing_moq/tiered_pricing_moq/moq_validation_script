import frappe
from frappe import _

def validate_moq(doc, method):
    """
    Validate if all items in the document have a quantity >= MOQ.
    This function validates documents that have an 'items' child table.
    """
    # Ensure the 'items' attribute is a valid list
    if not hasattr(doc, "items") or not isinstance(doc.items, list):
        return  # Exit if 'items' does not exist or is not a list

    # Iterate through the items and validate MOQ
    for item in doc.items:
        # Fetch the item's custom MOQ value
        custom_moq = frappe.db.get_value("Item", item.get("item_code"), "custom_moq")

        # Check if the quantity is less than the MOQ
        if custom_moq and item.get("qty", 0) < custom_moq:
            frappe.throw(
                _("Item {0} has a quantity ({1}) less than the MOQ ({2}).").format(
                    item.get("item_code"), item.get("qty"), custom_moq
                )
            )
