# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cmr_tractor_id = fields.Many2one(
        string="Tractor",
        comodel_name="fleet.vehicle",
        copy=False,
    )
    cmr_semi_trailer_id = fields.Many2one(
        string="Semi-Trailer",
        comodel_name="fleet.vehicle",
        copy=False,
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super(StockPicking, self).onchange_partner_id()
        if self.partner_id:
            self.cmr_tractor_id = self.partner_id.tractor_id.id
            self.cmr_semi_trailer_id = self.partner_id.semi_trailer_id.id

    @api.onchange("cmr_tractor_id")
    def onchange_cmr_tractor_id(self):
        if self.cmr_tractor_id:
            self.cmr_tractor_license_plate = self.cmr_tractor_id.license_plate
            self.crm_driver_id = self.cmr_tractor_id.driver_id.id

    @api.onchange("cmr_semi_trailer_id")
    def onchange_cmr_semi_trailer_id(self):
        if self.cmr_semi_trailer_id:
            self.cmr_semi_trailer_license_plate = self.cmr_semi_trailer_id.license_plate

    @api.onchange("crm_driver_id")
    def onchange_crm_driver_id(self):
        if self.crm_driver_id:
            self.cmr_loader_id = self.crm_driver_id.parent_id.id
