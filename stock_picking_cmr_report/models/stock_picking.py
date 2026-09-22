# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from calendar import month_name

from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cmr_way_out_id = fields.Many2one(
        string="Way out", comodel_name="res.city", copy=False
    )
    cmr_destination_id = fields.Many2one(
        string="Destination", comodel_name="res.city", copy=False
    )
    cmr_loader_id = fields.Many2one(
        string="loader", comodel_name="res.partner", copy=False
    )
    crm_transportation_id = fields.Many2one(
        string="Transportations", comodel_name="res.partner", copy=False
    )
    cmr_tractor_license_plate = fields.Char(string="Tractor license plate", copy=False)
    cmr_semi_trailer_license_plate = fields.Char(
        string="Semi-trailer license plate", copy=False
    )
    crm_driver_id = fields.Many2one(
        string="Driver", comodel_name="res.partner", copy=False
    )
    site_date_info = fields.Char(
        string="Site and date info", compute="_compute_site_date_info"
    )
    cmr_second_driver_id = fields.Many2one(
        string="Second Driver", comodel_name="res.partner", copy=False
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        parent_onchange = getattr(super(), "onchange_partner_id", None)
        res = {}
        if parent_onchange:
            res = parent_onchange()
        if self.partner_id:
            self.crm_driver_id = self.partner_id.driver_id.id
        return res

    @api.depends("cmr_way_out_id")
    def _compute_site_date_info(self):
        my_date = fields.Date.context_today(self)
        for picking in self:
            city = picking.cmr_way_out_id.name if picking.cmr_way_out_id else ""
            month = _(month_name[my_date.month])
            picking.site_date_info = (
                f"{city}, {my_date.day} of {month} of {my_date.year}"
            )
