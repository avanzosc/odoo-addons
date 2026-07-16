# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ContactRiskXlsx(models.AbstractModel):
    _name = "report.contact_risk_xlsx"
    _inherit = "report.contact_risk_xlsx_opt"
    _description = "Contact Risk Report"
