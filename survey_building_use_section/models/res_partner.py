# Copyright 2024 Unai Beristain - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    file_number = fields.Char(
        copy=False,
    )
    building_use_id = fields.Many2one(
        comodel_name="building.use",
        string="Building Use",
    )
    certification_text = fields.Text()
    emi = fields.Char(string="EMI")
    epi = fields.Char(string="EPI")
    normativas_ids = fields.Many2many(
        comodel_name="survey.question.normative",
        string="Normativas",
        compute="_compute_normativas_ids",
    )

    @api.depends("service_start_date")
    def _compute_normativas_ids(self):
        normative_obj = self.env["survey.question.normative"]
        for partner in self:
            partner.normativas_ids = normative_obj.search(
                [
                    ("start_year", "<=", partner.service_start_date.year),
                    ("end_year", ">=", partner.service_start_date.year),
                ]
            )
