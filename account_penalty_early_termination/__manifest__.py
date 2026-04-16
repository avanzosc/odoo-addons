# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Penalty Early Termination",
    "summary": "Early Termination Penalties for Subscriptions and Agreements",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": [
        "subscription_penalty",
        "agreement_penalty",
        "agreement_sale_creation",
        "agreement_livelink",
    ],
    "data": [
        "views/subscription_penalty_views.xml",
        "views/sale_subscription_views.xml",
        "views/account_penalty_views.xml",
    ],
    "installable": True,
}
