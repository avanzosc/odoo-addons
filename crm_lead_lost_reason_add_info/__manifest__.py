{
    "name": "CRM Lead Lost Reason Additional Information",
    "version": "14.0.1.0.0",
    "summary": "Enhances CRM leads with detailed information on lost opportunities.",
    "description": "Adds fields to CRM leads to capture detailed information when a lead is marked as lost.",
    "category": "Sales/CRM",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "views/crm_lead_views.xml",
        "wizards/crm_lead_lost_reason_wizard_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
