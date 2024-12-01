app_name = "tiered_pricing_moq"
app_title = "Tiered pricing moq"
app_publisher = "Momar Dia	"
app_description = "Apply tiered pricing and mo q"
app_email = "momar@boostwaydigital.com"
app_license = "agpl-3.0"

# Apps
# ------------------

# create the required fields in the database and add them to the form
after_install = "tiered_pricing_moq.setup.setup.setup_custom_fields"


# MQO validation hooks ______________________________________________________________________________________________________________
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
#_____________________________________________________________________________________________________________________________________





# tiered pricing calcutions for all sales processes
doc_events = {
    "Quotation": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing_logic"
    },
    "Sales Order": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing_logic"
    },
    "Sales Invoice": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing_logic"
    },
    "Delivery Note": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing_logic"
    },
    "Sales Receipt": {
        "before_save": "tiered_pricing_moq.tiered_pricing_moq.tiered_pricing_calculation.apply_tiered_pricing_logic"
    }
}




