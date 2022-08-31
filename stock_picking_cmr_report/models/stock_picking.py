# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cmr_way_out_id = fields.Many2one(
        string="Way out", comodel_name="res.city", copy=False)
    cmr_destination_id = fields.Many2one(
        string="Destination", comodel_name="res.city", copy=False)
    cmr_loader_id = fields.Many2one(
        string="loader", comodel_name="res.partner", copy=False)
    crm_transportation_id = fields.Many2one(
        string="Transportations", comodel_name="res.partner", copy=False)
    cmr_tractor_license_plate = fields.Char(
        string="Tractor license plate", copy=False)
    cmr_semi_trailer_license_plate = fields.Char(
        string="Semi-trailer license plate", copy=False)
    crm_driver_id = fields.Many2one(
        string="Driver", comodel_name="res.partner", copy=False)
    site_date_info = fields.Char(
        string="Site and date info", compute="_compute_site_date_info")

    def _compute_site_date_info(self):
        my_date = fields.Date.context_today(self)
        for picking in self:
            city = (picking.cmr_way_out_id.name if picking.cmr_way_out_id else
                    "")
            print ('***** my_date: ' + str(my_date))
            if my_date.month == 1:
                month = _("January")
            if my_date.month == 2:
                month = _("February")
            if my_date.month == 3:
                month = _("March")
            if my_date.month == 4:
                month = _("April")
            if my_date.month == 5:
                month = _("May")
            if my_date.month == 6:
                month = _("June")
            if my_date.month == 7:
                month = _("July")
            if my_date.month == 8:
                month = _("August")
            if my_date.month == 9:
                month = _("September")
            if my_date.month == 10:
                month = _("October")
            if my_date.month == 11:
                month = _("November")
            if my_date.month == 12:
                month = _("December")
            picking.site_date_info = "{}, {} of {} of {}".format(
                city, my_date.day, month, my_date.year)
