{
    "name": "Website Payment Acquirer Bank Account",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Integrates payment modes with bank accounts in sales.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": [
        "web",
        "sale",
        "account",
        "payment_acquirer_payment_mode",  # trey
    ],
    "data": ["views/payment_view.xml"],
    "installable": True,
    "application": False,
}
