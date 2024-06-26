{
    "name": "Product Classification Fields",
    "version": "1.0",
    "category": "Product",
    "summary": "Adds classification fields to product template",
    "description": """
        This module adds the following fields to the product template:
        - Series
        - Model
        - Application
        - Family
        - Packaging Type
    """,
    "depends": ["product"],
    "data": ["views/product_template_views.xml"],
    "installable": True,
    "application": False,
}
