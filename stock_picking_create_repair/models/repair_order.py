# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class RepairOrder(models.Model):
    _inherit = "repair.order"

    created_from_move_line_id = fields.Many2one(
        string="Created from detailed operation", copy=False,
        comodel_name="stock.move.line")
    created_from_picking_id = fields.Many2one(
        string="Created from incoming picking", comodel_name="stock.picking",
        related="created_from_move_line_id.picking_id", store=True, copy=False)
    purchase_order_id = fields.Many2one(
        string="Purchase order", comodel_name="purchase.order", copy=False)
    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=False)
    sale_line_id = fields.Many2one(
        string="Sale line", comodel_name="sale.order.line",
        related="created_from_move_line_id.sale_line_id", store=True,
        copy=False)
    from_repair_picking_out_id = fields.Many2one(
        string="From repair picking out", comodel_name="stock.picking",
        copy=False)
    price_in_sale_budget = fields.Float(
        string="Price in sale budget", digits='Product Price', default=0.0,
        copy=False)

    def action_repair_end(self):
        result = super(RepairOrder, self).action_repair_end()
        for repair in self.filtered(
            lambda x: not x.from_repair_picking_out_id and
                x.sale_order_id):
            repair._create_out_picking_repair()
            repair._amount_untaxed_to_sale_order()
        return result

    def action_repair_done(self):
        return super(RepairOrder,self.with_context(
            move_no_to_done=True)).action_repair_done()

    def _create_out_picking_repair(self):
        cond = [('sale_order_id', '=', self.sale_order_id.id),
                ('from_repair_picking_out_id', '!=', False)]
        repair = self.env['repair.order'].search(cond)
        if repair:
            picking = repair.from_repair_picking_out_id
        else:
            vals = self._catch_data_for_create_out_picking_repair()
            picking = picking = self.env["stock.picking"].create(vals)
        vals = {'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id}
        self.move_id.write(vals)
        self.move_id.move_line_ids.write(vals)
        self.from_repair_picking_out_id = picking.id

    def _amount_untaxed_to_sale_order(self):
        cond = [('sale_order_id', '=', self.sale_order_id.id)]
        all_repairs = self.env['repair.order'].search(cond)
        if all_repairs:
            realized_repairs = all_repairs.filtered(
                lambda x: x.state == 'done')
            if len(all_repairs) == len(realized_repairs):
                self.sale_order_id.repairs_amount_untaxed = (
                    sum(all_repairs.mapped('amount_untaxed')))
        cond = [('created_repair_id', '=', self.id)]
        move_lines = self.env['stock.move.line'].search(cond)
        if move_lines:
            move_lines = move_lines.filtered(lambda x: x.move_id)
            for move_line in move_lines:
                if move_line.move_id and move_line.move_id.sale_line_id:
                    sale_line = move_line.move_id.sale_line_id
                    qty_done = sale_line.qty_delivered
                    repair_amount_untaxed = sale_line.repair_amount_untaxed
                    repair_amount_untaxed += self.amount_untaxed
                    qty_done += self.product_qty
                    sale_line.write(
                        {'qty_delivered_manual': qty_done,
                         'qty_delivered': qty_done,
                         'repair_amount_untaxed': repair_amount_untaxed})
                    sale_line.price_unit = (sale_line.repair_amount_untaxed /
                                            sale_line.qty_delivered)

    def _catch_data_for_create_out_picking_repair(self):
        picking_type = self.sale_order_id.type_id.picking_type_repair_out_id
        vals = {"picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id,
                "location_dest_id": picking_type.default_location_dest_id.id,
                "partner_id": self.sale_order_id.partner_id.id,
                "origin": self.sale_order_id.name,
                "sale_order_id": self.sale_order_id.id,
                "company_id": self.sale_order_id.company_id.id,
                "is_repair": True}
        return vals

    def write(self, values):
        result = super(RepairOrder, self).write(values)
        if "price_in_sale_budget" in values:
            self._put_price_bugdet_in_sale_order_line()
        return result

    def _put_price_bugdet_in_sale_order_line(self):
        for repair in self.filtered(lambda x: x.sale_order_id and
                                    x.sale_order_id.state == "draft" and
                                    x.created_from_picking_id and
                                    x.created_from_move_line_id):
            cond = [
                ("sale_order_id", '=', repair.sale_order_id.id),
                ("created_from_picking_id", '=',
                 repair.created_from_picking_id.id),
                ("product_id", '=', repair.product_id.id)]
            for_product_repairs = self.env['repair.order'].search(cond)
            if for_product_repairs:
                price_in_sale_budget = sum(
                    for_product_repairs.mapped('price_in_sale_budget'))
                sale_line = (
                    repair.created_from_move_line_id.move_id.sale_line_id)
                price_unit = price_in_sale_budget / sale_line.product_uom_qty
                sale_line.write(
                    {"price_unit": price_unit,
                     "repair_price_in_sale_budget": price_in_sale_budget})

    def control_action_repair_start(self):
        repairs = self.filtered(lambda r: r.state in ["confirmed", "ready"])
        for repair in repairs:
            repair.action_repair_start()

    def control_action_repair_end(self):
        repairs = self.filtered(lambda r: r.state == "under_repair")
        for repair in repairs:
            repair.action_repair_end()

    def control_action_validate(self):
        repairs = self.filtered(lambda r: r.state == "draft")
        for repair in repairs:
            repair.action_validate()
