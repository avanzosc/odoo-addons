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
    cmr_loader_vat = fields.Char(string="Loader VAT", copy=False)
    cmr_loader_address = fields.Text(string="Loader Address")
    cmr_transportation_id = fields.Many2one(
        string="Transportations", comodel_name="res.partner", copy=False
    )
    cmr_transportation_vat = fields.Char(string="Transportation VAT", copy=False)
    cmr_tractor_license_plate = fields.Char(string="Tractor license plate", copy=False)
    cmr_semi_trailer_license_plate = fields.Char(
        string="Semi-trailer license plate", copy=False
    )
    cmr_driver_id = fields.Many2one(
        string="Driver", comodel_name="res.partner", copy=False
    )
    site_date_info = fields.Char(
        string="Site and date info", compute="_compute_site_date_info"
    )
    cmr_second_driver_id = fields.Many2one(
        string="Second Driver", comodel_name="res.partner", copy=False
    )
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
    cmr_special_traffic_authorization = fields.Boolean(
        string="Special Traffic Authorization",
        default=False,
        copy=False,
    )
    cmr_observations = fields.Text(
        string="Observations",
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        parent_onchange = getattr(super(), "onchange_partner_id", None)
        res = {}
        if parent_onchange:
            res = parent_onchange()
        if self.partner_id:
            self.cmr_driver_id = self.partner_id.driver_id.id
            self.cmr_tractor_id = self.partner_id.tractor_id.id
            self.cmr_semi_trailer_id = self.partner_id.semi_trailer_id.id
        return res

    @api.onchange("cmr_loader_id")
    def onchange_cmr_loader_id(self):
        self.cmr_loader_vat = self.cmr_loader_id.vat or ""
        self.cmr_loader_address = self.cmr_loader_id.contact_address or ""

    @api.onchange("cmr_transportation_id")
    def onchange_cmr_transportation_id(self):
        self.cmr_transportation_vat = self.cmr_transportation_id.vat or ""

    @api.onchange("cmr_tractor_id")
    def _onchange_cmr_tractor_id(self):
        for picking in self:
            if picking.cmr_tractor_id:
                picking.cmr_tractor_license_plate = picking.cmr_tractor_id.license_plate
                picking.cmr_driver_id = picking.cmr_tractor_id.driver_id.id

    @api.onchange("cmr_semi_trailer_id")
    def _onchange_cmr_semi_trailer_id(self):
        for picking in self:
            if picking.cmr_semi_trailer_id:
                picking.cmr_semi_trailer_license_plate = (
                    picking.cmr_semi_trailer_id.license_plate
                )

    @api.onchange("cmr_tractor_id", "cmr_semi_trailer_id")
    def _onchange_cmr_tractor_semi_trailer(self):
        for picking in self:
            picking.cmr_special_traffic_authorization = any(
                (
                    picking.cmr_tractor_id.special_traffic_authorization,
                    picking.cmr_semi_trailer_id.special_traffic_authorization,
                )
            )

    @api.onchange("cmr_driver_id")
    def _onchange_cmr_driver_id(self):
        for picking in self:
            if picking.cmr_driver_id:
                picking.cmr_loader_id = picking.cmr_driver_id.parent_id.id

    @api.depends("cmr_way_out_id")
    def _compute_site_date_info(self):
        my_date = fields.Date.context_today(self)
        for picking in self:
            city = picking.cmr_way_out_id.name if picking.cmr_way_out_id else ""
            month = _(month_name[my_date.month])
            picking.site_date_info = (
                f"{city}, {my_date.day} of {month} of {my_date.year}"
            )
