import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def setup_custom_fields():
    """Create the custom fields for tiered pricing and MOQ in the Item doctype and ensure they're in the form."""
    
    # Existing custom field for MOQ (minimum order quantity)
    custom_fields = [
        {
            "fieldname": "custom_moq",
            "label": "Minimum Order Quantity",
            "fieldtype": "Int",
            "insert_after": "stock_uom",  # Adjust based on where it should appear
            "default": 1,
            "reqd": 1,
            "in_list_view": 1,
            "description": "Minimum Order Quantity for Items",
        },
        # New custom fields for tiered pricing
        {
            "fieldname": "custom_is_tiered",
            "label": "Enable Tiered Pricing",
            "fieldtype": "Check",
            "insert_after": "custom_moq",  # Insert after MOQ field
            "default": 0,
            "reqd": 0,
            "in_list_view": 1,
            "description": "Check if tiered pricing is enabled for this item",
        },
        {
            "fieldname": "custom_tier_size",
            "label": "Tier Size",
            "fieldtype": "Int",
            "insert_after": "custom_is_tiered",
            "default": 50,
            "reqd": 0,
            "in_list_view": 1,
            "description": "The size of each tier (in UOM).",
        },
        {
            "fieldname": "custom_reduction_per_tier",
            "label": "Reduction per Tier (%)",
            "fieldtype": "Float",
            "insert_after": "custom_tier_size",
            "default": 8,
            "reqd": 0,
            "in_list_view": 1,
            "description": "The percentage reduction per tier.",
        }
    ]
    
    # Loop through all the fields and create them if they don't exist
    for field in custom_fields:
        field_name = field["fieldname"]
        field_label = field["label"]
        
        # Check if the field already exists
        if not frappe.db.exists("Custom Field", {"fieldname": field_name, "dt": "Item"}):
            # Create the custom field
            create_custom_field("Item", field)
            frappe.msgprint(f"{field_label} has been added to the Item doctype.")

        # Add the field to the form layout
        ensure_field_in_form(field_name, field_label)


def ensure_field_in_form(fieldname, label):
    """Ensure the custom field is part of the Item form layout."""
    customize_form = frappe.get_doc("Customize Form", {"doc_type": "Item"})
    
    # Check if the field is already present in the form
    if not any(f.fieldname == fieldname for f in customize_form.fields):
        customize_form.append("fields", {
            "fieldname": fieldname,
            "label": label,
            "fieldtype": "Data",  # Use the fieldtype from the creation above
            "insert_after": "stock_uom",  # Adjust based on where it should appear
            "reqd": 0,
        })
        customize_form.save()
        frappe.msgprint(f"{label} has been added to the Item form layout.")
