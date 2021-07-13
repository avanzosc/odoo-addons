# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Product Multi Company Tax",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Products & Pricelists",
    "depends": [
        "account",
        "product",
        "purchase",
        "l10n_es",
        "base_multi_company",
        "product_multi_company"
    ],
    "data": [
        "data/product_tax_cron.xml"
    ],
    "installable": True,
    "auto_install": True,
}
