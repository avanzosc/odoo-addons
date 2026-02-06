# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Subscription Penalty",
    "summary": "Penalty Tracking to Subscriptions",
    "version": "14.0.1.0.0",
    "category": "Subscription",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["sale_subscription", "account_penalty"],
    "data": [
        "security/ir.model.access.csv",
        "views/subscription_penalty_views.xml",
        "views/sale_subscription_views.xml",
    ],
    "installable": True,
}
