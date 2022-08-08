# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_repair = fields.Boolean(
        string="Is repair", related="product_id.is_repair",
        store=True, copy=False)
    product_to_repair_id = fields.Many2one(
        string="Product to repair", comodel_name="product.product", copy=False)
    initial_price_unit = fields.Float(
        string="Initial price unit", digits='Product Price', default=0.0,
        copy=False)
    repair_amount_untaxed = fields.Monetary(
        string='Repair untaxed amount', copy=False)
    repair_price_in_sale_budget = fields.Float(
        string="Repairs price in sale budget", digits='Product Price',
        default=0.0, copy=False)

    @api.onchange('product_id')
    def product_id_change(self):
        warning = {}
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.product_id.is_repair:
            lit_message = _("You must enter the product to repair")
            if "warning" not in result:
                warning['title'] = _("Warning for %s", self.product_id.name)
                warning['message'] = lit_message
                result = {'warning': warning}
            else:
                warning = result.get("warning")
                my_message = "{} \n {}".format(
                    warning.get("message"), lit_message)
                result["warning"]["message"] = my_message
        return result

    def create_stock_move_for_in_picking_repair(self, picking):
        vals = self._catch_data_for_create_move_in_picking_repair(picking)
        self.env['stock.move'].create(vals)

    def _catch_data_for_create_move_in_picking_repair(self, picking):
        vals = {"name": self.product_to_repair_id.name,
                "product_id": self.product_to_repair_id.id,
                "partner_id": self.order_id.partner_id.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "picking_id": picking.id,
                "sale_line_id": self.id,
                "company_id": self.order_id.company_id.id,
                "picking_type_id": picking.picking_type_id.id,
                "origin": self.order_id.name,
                "description_picking": self.product_to_repair_id.name,
                "propagate_cancel": True,
                "warehouse_id": picking.picking_type_id.warehouse_id.id,
                "product_uom_qty": self.product_uom_qty,
                "product_uom": self.product_to_repair_id.uom_po_id.id}
        return vals
