app_name = "tiered_pricing_moq"
app_title = "Tiered Pricing MOQ"
app_publisher = "Momar Dia"
app_description = "Apply tiered pricing and MOQ"
app_email = "momar@boostwaydigital.com"
app_license = "AGPL-3.0"

# Hooks for after installation
# ----------------------------
after_install = "tiered_pricing_moq.setup.setup.setup_custom_fields"

# Document Events
# ----------------------------
doc_events = {
    # MOQ validation hooks and tiered pricing calculation
    "Quotation": {
        "before_save": [
            "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq",
            "tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing",
        ]
    },
    "Sales Order": {
        "before_save": [
            "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq",
            "tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing",
        ]
    },
    "Purchase Order": {
        "before_save": "tiered_pricing_moq.moq_validation_script.validate_moq",
    },
    "Blanket Order": {
        "before_save": "tiered_pricing_moq.moq_validation_script.validate_moq",
    },
    "Delivery Note": {
        "before_save": [
            "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq",
            "tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing",
        ]
    },
    "Purchase Receipt": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.moq_validation_script.validate_moq",
    },
    "Sales Invoice": {
        "before_save": "tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing",
    },
    "Sales Receipt": {
        "before_save": "tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing",
    },
}
