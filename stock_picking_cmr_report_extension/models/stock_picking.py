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
        res = super().onchange_partner_id()
        for picking in self:
            if picking.partner_id:
                picking.cmr_tractor_id = picking.partner_id.tractor_id.id
                picking.cmr_semi_trailer_id = picking.partner_id.semi_trailer_id.id
        return res

    @api.onchange("cmr_tractor_id")
    def _onchange_cmr_tractor_id(self):
        for picking in self:
            if picking.cmr_tractor_id:
                picking.cmr_tractor_license_plate = picking.cmr_tractor_id.license_plate
                picking.crm_driver_id = picking.cmr_tractor_id.driver_id.id

    @api.onchange("cmr_semi_trailer_id")
    def _onchange_cmr_semi_trailer_id(self):
        for picking in self:
            if picking.cmr_semi_trailer_id:
                picking.cmr_semi_trailer_license_plate = (
                    picking.cmr_semi_trailer_id.license_plate
                )

    @api.onchange("crm_driver_id")
    def _onchange_crm_driver_id(self):
        for picking in self:
            if picking.crm_driver_id:
                picking.cmr_loader_id = picking.crm_driver_id.parent_id.id
