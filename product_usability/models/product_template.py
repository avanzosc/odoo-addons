# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api
from datetime import timedelta
from odoo.tools.float_utils import float_round


class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_product_pricelist = fields.Many2one(
        search="_search_product_pricelist")
    comsumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months", digits="Product Unit of Measure",
        compute="_compute_comsumed_last_twelve_months")
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_months_with_stock")

    def _compute_comsumed_last_twelve_months(self):
        stock_move_obj = self.env["stock.move"]
        date_from = fields.Datetime.to_string(
            fields.datetime.now() - timedelta(days=365))
        for template in self:
            domain = [
                ("state", "=", "done"),
                ("date", ">", date_from),
                ("location_dest_id", "!=", False),
                ("location_dest_id.usage", "not in",
                 ("view", "internal", "supplier")),
                ("product_id.product_tmpl_id", "=", template.id)]
            move_lines = stock_move_obj.read_group(
                domain, ['product_id', 'product_uom_qty'], ['product_id'])
            move_data = dict(
                [(data['product_id'][0], data['product_uom_qty'])
                    for data in move_lines])
            template.comsumed_last_twelve_months = float_round(
                move_data.get(template.id, 0),
                precision_rounding=template.uom_id.rounding)

    def _compute_months_with_stock(self):
        for template in self:
            months_with_stock = 0
            if template.incoming_qty:
                months_with_stock = (
                    (template.qty_available + template.incoming_qty -
                     template.outgoing_qty) / (template.incoming_qty / 12))
            template.months_with_stock = months_with_stock

    @api.model
    def _search_product_pricelist(self, operator, value):
        result = self.env["ir.property"].search_multi(
            "property_product_pricelist", "product.template", operator, value)
        return result

