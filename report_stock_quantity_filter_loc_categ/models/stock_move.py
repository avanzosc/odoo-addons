# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    not_show_category_in_inventory_reports = fields.Boolean(
        string="NOT show category in inventory reports",
        compute="_compute_not_show_category_in_inventory_reports",
        copy=False, store=True)
    not_show_location_in_inventory_reports = fields.Boolean(
        string="NOT show location in inventory reports",
        compute="_compute_not_show_location_in_inventory_reports",
        copy=False, store=True)

    @api.depends("product_id", "product_id.categ_id",
                 "product_id.categ_id.not_show_in_inventory_reports")
    def _compute_not_show_category_in_inventory_reports(self):
        for move in self:
            not_show_category_in_inventory_reports = False
            if move.product_id and move.product_id.categ_id:
                not_show_category_in_inventory_reports = (
                    move.product_id.categ_id.not_show_in_inventory_reports)
            move.not_show_category_in_inventory_reports = (
                not_show_category_in_inventory_reports)

    @api.depends("location_id.not_show_in_inventory_reports",
                 "location_dest_id.not_show_in_inventory_reports")
    def _compute_not_show_location_in_inventory_reports(self):
        for move in self:
            not_show_location_in_inventory_reports = False
            if (move.location_id and
                    move.location_id.not_show_in_inventory_reports):
                not_show_location_in_inventory_reports = True
            if (move.location_dest_id and
                    move.location_dest_id.not_show_in_inventory_reports):
                not_show_location_in_inventory_reports = True
            move.not_show_location_in_inventory_reports = (
                not_show_location_in_inventory_reports)
