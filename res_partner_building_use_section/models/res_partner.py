# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        string=_("Building use"),
        comodel_name="building.use",
        copy=False,
    )
    building_section_ids = fields.One2many(
        string=_("Building Section/Area"),
        comodel_name="building.section",
        inverse_name="partner_id",
        copy=False,
    )
    service_start_date = fields.Date(
        string=_("Service Start Date"),
        copy=False,
    )
    service_end_date = fields.Date(
        string=_("Service End Date"),
        copy=False,
    )

    maintainer_id = fields.Many2one(_("Maintainer"), comodel_name="res.partner")
    installer_id = fields.Many2one(_("Installer"), comodel_name="res.partner")
    administrator_id = fields.Many2one(_("Administrator"), comodel_name="res.partner")

    normativas_ids = fields.Many2many(
        "survey.question.normative",
        string=_("Normativas"),
        compute="_compute_normativas_ids",
    )

    @api.depends("service_start_date")
    def _compute_normativas_ids(self):
        for partner in self:
            partner.normativas_ids = self.env["survey.question.normative"].search(
                [
                    ("start_year", "<=", partner.service_start_date.year),
                    ("end_year", ">=", partner.service_start_date.year),
                ]
            )