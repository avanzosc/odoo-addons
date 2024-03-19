# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    file_number = fields.Char(
        string="File Number",
        copy=False,
    )
    building_use_id = fields.Many2one("building.use", string="Building Use")
    is_industrial = fields.Boolean(string="Industrial")
    certification_text = fields.Text(string="Certification Text")
