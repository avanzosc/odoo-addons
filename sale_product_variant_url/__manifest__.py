{
    "name": "Product Variant URL - Sale Glue",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "summary": "Show Product URL in Sale Order Reports if both modules are installed",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "sale",
        "product_variant_url",
    ],
    "data": [
        "views/sale_report_template.xml"
    ],
    "installable": True,
    "auto_install": True,
}
