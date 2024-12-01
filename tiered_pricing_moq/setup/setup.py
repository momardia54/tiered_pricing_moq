import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def setup_custom_fields():
    """Create the custom fields for tiered pricing in the Item and Item Price doctypes and ensure they're in the form."""
    
    # Custom fields for Item doctype
    item_custom_fields = [
        {
            "fieldname": "custom_is_tiered",
            "label": "Enable Tiered Pricing",
            "fieldtype": "Check",
            "insert_after": "description",  # Insert after description field (adjust if needed)
            "default": 0,
            "reqd": 1,
            "in_list_view": 1,
            "description": "Check if tiered pricing is enabled for this item.",
        },
        {
            "fieldname": "custom_tier_size",
            "label": "Tier Size",
            "fieldtype": "Int",
            "insert_after": "custom_is_tiered",
            "default": 50,
            "reqd": 1,
            "in_list_view": 1,
            "description": "The size of each tier (in UOM).",
        },
        {
            "fieldname": "custom_reduction_per_tier",
            "label": "Reduction per Tier (%)",
            "fieldtype": "Float",
            "insert_after": "custom_tier_size",
            "default": 8,
            "reqd": 1,
            "in_list_view": 1,
            "description": "The percentage reduction per tier.",
        }
    ]
    
    # Loop through all the fields and create them if they don't exist
    for field in item_custom_fields:
        field_name = field["fieldname"]
        field_label = field["label"]
        
        # Check if the field already exists
        if not frappe.db.exists("Custom Field", {"fieldname": field_name, "dt": "Item"}):
            # Create the custom field
            create_custom_field("Item", field)
            frappe.msgprint(f"{field_label} has been added to the Item doctype.")

        # Add the field to the form layout for Item
        ensure_field_in_form("Item", field_name, field_label, field)

    # Custom field for Item Price doctype
    item_price_custom_fields = [
        {
            "fieldname": "custom_flat_rate_price",
            "label": "Base Flat Rate Price",
            "fieldtype": "Currency",  # Changed to Currency type
            "insert_after": "price_list_rate",  # Adjust based on where it should appear
            "default": 0,
            "reqd": 1,
            "in_list_view": 1,
            "description": "Base flat rate price for tiered pricing.",
        }
    ]
    
    # Loop through all the fields for Item Price and create them if they don't exist
    for field in item_price_custom_fields:
        field_name = field["fieldname"]
        field_label = field["label"]
        
        # Check if the field already exists
        if not frappe.db.exists("Custom Field", {"fieldname": field_name, "dt": "Item Price"}):
            # Create the custom field
            create_custom_field("Item Price", field)
            frappe.msgprint(f"{field_label} has been added to the Item Price doctype.")

        # Add the field to the form layout for Item Price
        ensure_field_in_form("Item Price", field_name, field_label, field)


def ensure_field_in_form(doctype, fieldname, label, field_properties):
    """Ensure the custom field is part of the doctype form layout."""
    try:
        # Fetch the Customize Form document
        customize_form = frappe.get_doc("Customize Form", {"doc_type": doctype})
        
        # Check if the field is already present in the form
        if not any(f.fieldname == fieldname for f in customize_form.fields):
            customize_form.append("fields", {
                "fieldname": fieldname,
                "label": label,
                "fieldtype": field_properties["fieldtype"],  # Use the field type from the creation
                "insert_after": field_properties.get("insert_after", "price_list_rate"),  # Default to price_list_rate
                "reqd": field_properties["reqd"],
            })
            customize_form.save()
            frappe.msgprint(f"{label} has been added to the {doctype} form layout.")
    except Exception as e:
        frappe.msgprint(f"Error adding {label} to the {doctype} form: {str(e)}")
