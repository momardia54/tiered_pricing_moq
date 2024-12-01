app_name = "tiered_pricing_moq"
app_title = "Tiered pricing moq"
app_publisher = "Momar Dia	"
app_description = "Apply tiered pricing and mo q"
app_email = "momar@boostwaydigital.com"
app_license = "agpl-3.0"

# Apps
# ------------------

doc_events = {
    "Quotation": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    },
    "Sales Order": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    },
    "Purchase Order": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    },
    "Blanket Order": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    },
    "Delivery Note": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    },
    "Purchase Receipt": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq"
    }
}
