# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "SEPE - Expedientes y Acciones Formativas",
    "summary": "Expedientes de financiación, acciones formativas y eventos vinculados",
    "version": "18.0.1.0.0",
    "category": "Events",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "author": "Avanzosc",
    "depends": ["event"],
    "data": [
        "security/ir.model.access.csv",
        "data/sepe.training.specialty.csv",
        "views/training_funding_views.xml",
        "views/training_action_views.xml",
        "views/event_event_views.xml",
        "views/sepe_specialty_views.xml",
        "views/grant_program.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
