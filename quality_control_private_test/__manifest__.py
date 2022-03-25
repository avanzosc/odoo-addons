# Copyright (c) 2022 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Quality Control Private Test",
    "version": "14.0.1.0.0",
    "depends": [
        "base",
        "quality_control_oca",
        "product",
    ],
    "author":  "AvanzOSC",
    "license": "AGPL-3",
    "summary": """Quality Control Private Test""",
    "website": "http://www.avanzosc.es",
    "data": [
        "views/quality_control_view.xml",
        "views/product_template_view.xml",
        #"security/ir.model.access.csv",
        ],
    "installable": True,
    "auto_install": False,
}
