# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    main_parent_id = fields.Many2one(
        string="Main Partner", comodel_name="res.partner",
        compute="_compute_group_parent_info", store=True, copy=False
    )
    main_state_id = fields.Many2one(
        string="Main Province", comodel_name="res.country.state",
        compute="_compute_group_parent_info", store=True, copy=False
    )

    @api.depends("state_id", "parent_id", "parent_id.state_id")
    def _compute_group_parent_info(self):
        for partner in self:
            main_parent_id = False
            main_state_id = False
            if partner.id and not partner.parent_id:
                main_parent_id = partner.id
                if partner.state_id:
                    main_state_id = partner.state_id.id
            if partner.parent_id:
                main_parent_id = partner.parent_id.id
                if partner.parent_id.state_id:
                    main_state_id = partner.parent_id.state_id.id
            partner.main_parent_id = main_parent_id
            partner.main_state_id = main_state_id
