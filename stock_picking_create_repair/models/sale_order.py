# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_repair = fields.Boolean(
        string="Is repair", related="type_id.is_repair",
        store=True, copy=False)
    repair_ids = fields.One2many(
        string="Repairs", comodel_name="repair.order",
        inverse_name="sale_order_id", copy=False)
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", copy=False,
        store=True)
    count_in_picking_repairs = fields.Integer(
        string="# Repair in pickings",
        compute="_compute_count_in_picking_repairs")
    count_out_picking_repairs = fields.Integer(
        string="# Repair out pickings",
        compute="_compute_count_out_picking_repairs")
    repairs_amount_untaxed = fields.Monetary(
        string='Repairs untaxed amount', copy=False)

    @api.depends("repair_ids")
    def _compute_repairs_count(self):
        for sale in self:
            sale.repairs_count = len(sale.repair_ids)

    def _compute_count_in_picking_repairs(self):
        for sale in self:
            pickings = sale._search_pickings_repair(
                self.type_id.picking_type_repair_in_id)
            sale.count_in_picking_repairs = len(pickings)

    def _compute_count_out_picking_repairs(self):
        for sale in self:
            pickings = sale._search_pickings_repair(
                self.type_id.picking_type_repair_out_id)
            sale.count_out_picking_repairs = len(pickings)

    def action_in_picking_repairs_from_sale(self):
        self.ensure_one()
        pickings = self._search_pickings_repair(
            self.type_id.picking_type_repair_in_id)
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", pickings.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_out_picking_repairs_from_sale(self):
        self.ensure_one()
        pickings = self._search_pickings_repair(
            self.type_id.picking_type_repair_out_id)
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", pickings.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_repairs_from_sale(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.repair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def create_invoice_repairs_control(self):
        self.ensure_one()
        if self.is_repair and self.repair_ids:
            repairs = self.repair_ids.filtered(
                lambda x: x.state not in ('done', 'cancel'))
            if repairs:
                raise UserError(
                    _("Can't invoice yet, because there are unfinished "
                      "repairs."))
        action = self.env.ref("sale.action_view_sale_advance_payment_inv")
        action_dict = action.read()[0] if action else {}
        return action_dict

    def _search_pickings_repair(self, picking_type):
        cond = [('picking_type_id', '=', picking_type.id),
                ('location_id', '=', picking_type.default_location_src_id.id),
                ('location_dest_id', '=',
                 picking_type.default_location_dest_id.id),
                ('partner_id', '=', self.partner_id.id),
                ('sale_order_id', '=', self.id),
                ('company_id', '=', self.company_id.id),
                ('is_repair', '=', True)]
        pickings = self.env['stock.picking'].search(cond)
        return pickings

    def action_create_in_picking_repair_from_sale_order(self):
        self._control_data_ok_for_repair()
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            if lines:
                picking = sale.create_in_picking_repair()
            for line in lines:
                line.create_stock_move_for_in_picking_repair(picking)

    def _control_data_ok_for_repair(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            if lines and not sale.is_repair:
                raise UserError(
                    _("There are lines with products to be repaired, and the "
                      "type of sale is not repair."))
            if not lines and sale.is_repair:
                raise UserError(
                    _("The type of sale is repair, and there is no line in "
                      "the sales order with product to be repaired."))
            lines = sale.order_line.filtered(
                lambda x: x.is_repair and not x.product_to_repair_id)
            for line in lines:
                raise UserError(
                    _("You must enter the product to be repaired for "
                      "product: {}").format(line.product_id.name))

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            for line in lines:
                line.initial_price_unit = line.price_unit
        return result

    def create_in_picking_repair(self):
        vals = self._catch_data_for_create_in_picking_repair()
        picking = self.env["stock.picking"].create(vals)
        return picking

    def _catch_data_for_create_in_picking_repair(self):
        picking_type = self.type_id.picking_type_repair_in_id
        vals = {"picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id,
                "location_dest_id": picking_type.default_location_dest_id.id,
                "partner_id": self.partner_id.id,
                "origin": self.name,
                "sale_order_id": self.id,
                "company_id": self.company_id.id,
                "is_repair": True}
        return vals
