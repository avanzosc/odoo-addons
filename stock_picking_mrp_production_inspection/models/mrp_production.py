# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _compute_num_related_sale_orders(self):
        for production in self:
            production.num_related_sale_orders = len(
                production.related_sale_order_ids)

    def _compute_num_related_out_pickings(self):
        for production in self:
            production.num_related_out_pickings = len(
                production.related_out_picking_ids)

    related_sale_order_ids = fields.Many2many(
        comodel_name="sale.order",
        relation="rel_related_production_sale",
        column1="production_id", column2="sale_id",
        string="Sale orders", copy=False)
    related_out_picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        relation="rel_related_production_out_picking",
        column1="production_id", column2="picking_id",
        string="Out pickings", copy=False)
    num_related_sale_orders = fields.Integer(
        string="Num. Related sale orders",
        compute="_compute_num_related_sale_orders")
    num_related_out_pickings = fields.Integer(
        string="Num. Related out pickings",
        compute="_compute_num_related_out_pickings")

    @api.multi
    def action_inspect_to_out_picking(self):
        self.ensure_one()
        related_sale_orders = self.env["sale.order"]
        related_out_pickings = self.env["stock.picking"]
        inspections = self.env["qc.inspection"]
        production_obj = self.env["mrp.production"]      
        production = production_obj
        if self.origin and self.product.attributes:
            production = self
        else:
            cond = [("origin", "=", self.name)]
            production = production_obj.search(cond, limit=1)
        if (not production or not
            production.move_created_ids2 or not
            production.move_created_ids2[0].restrict_lot_id):
            return  
        cond = [("name", "=", production.origin)]
        production_origin = production_obj.search(cond, limit=1)        
        cond = [
            ("product_id", "=", production.move_created_ids2[0].product_id.id),
            ("lot_id", "=", production.move_created_ids2[0].restrict_lot_id.id)]
        quants= self.env["stock.quant"].search(cond)
        for quant in quants:
            for history in quant.history_ids. filtered(lambda x: x.origin and x.origin != production.name):
                cond = [("name", "=", history.origin)]
                sale = self.env["sale.order"].search(cond)
                if sale:
                    cond = [("origin", "=", sale.name)]
                    picking = self.env["stock.picking"].search(cond, limit=1)
                    if picking and picking.picking_type_id.code == "outgoing":
                        if sale not in related_sale_orders:
                            related_sale_orders += sale
                        if picking not in related_out_pickings:
                            related_out_pickings += picking
        if related_sale_orders:
            production.related_sale_order_ids = [
                (6, 0, related_sale_orders.ids)]
        if related_out_pickings:
            production.related_out_picking_ids = [
                (6,0, related_out_pickings.ids)]
            
        if production_origin.move_lines2:
            lots = production_origin.move_lines2.mapped("restrict_lot_id")
            for lot in lots:
                for inspection in lot.qc_inspections:
                    if inspection not in inspections:
                        inspections += inspection
                        
        if related_sale_orders or related_out_pickings:
            cond = [("name", "=", production.origin)]
            production_origin = production_obj.search(cond, limit=1)
            if production_origin:
                if related_sale_orders:
                    production_origin.related_sale_order_ids = [
                        (6, 0, related_sale_orders.ids)]
                if related_out_pickings:
                    production_origin.related_out_picking_ids = [
                        (6,0, related_out_pickings.ids)]
        if related_out_pickings and inspections:
            related_out_pickings.write(
                {"mrp_related_inspections_ids": [(
                    6, 0, inspections.ids)]})

    @api.multi
    def button_view_related_sale_orders(self):
        self.ensure_one()
        if self.related_sale_order_ids:
            return {'name': _('Related sale orders'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'res_model': 'sale.order',
                    'domain': [('id', 'in',
                                self.related_sale_order_ids.ids)]}

    @api.multi
    def button_view_related_out_pickings(self):
        self.ensure_one()
        if self.related_out_picking_ids:
            return {'name': _('Related out pickings'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'res_model': 'stock.picking',
                    'domain': [('id', 'in',
                                self.related_out_picking_ids.ids)]}
 
        