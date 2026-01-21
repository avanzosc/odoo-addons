# Copyright 2025 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Agreement Penalty Type",
    "version": "14.0.1.0.0",
    "category": "Agreement",
    "license": "AGPL-3",
    "summary": "Link penalty types to agreements with custom pricing",
    "author": "AvanzOSC",
    "website": "https://www.avanzosc.es",
    "depends": [
        "agreement",          
        "account_penalties", 
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/agreement_view.xml",
    ],
    "installable": True,
}
