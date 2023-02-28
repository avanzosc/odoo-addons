# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_num_mrp_related_inspections(self):
        for picking in self:
            picking.num_mrp_related_inspections = len(
                picking.mrp_related_inspections_ids)

    mrp_related_inspections_ids = fields.Many2many(
        comodel_name="qc.inspection",
        relation="rel_picking_related_inspections",
        column1="picking_id", column2="inspection_id",
        string="MRP Related Inspections", copy=False)
    num_mrp_related_inspections = fields.Integer(
        string="Num. MRP Related inspections",
        compute="_compute_num_mrp_related_inspections")

    @api.multi
    def button_view_related_inspections(self):
        self.ensure_one()
        if self.mrp_related_inspections_ids:
            return {'name': _('Related inspections'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'res_model': 'qc.inspection',
                    'domain': [('id', 'in',
                                self.mrp_related_inspections_ids.ids)]}

    @api.multi
    def get_customer_for_certificacion(self):
        self.ensure_one()
        customer = ""
        if self.origin:
            cond = [("name", "=", self.origin)]
            sale = self.env["sale.order"].search(
                cond, limit=1)
            if sale:
                customer = sale.partner_id.name             
        return customer

    @api.multi
    def get_num_order_for_certificacion(self):
        self.ensure_one()
        num_order = ""
        if self.origin:
            cond = [("name", "=", self.origin)]
            sale = self.env["sale.order"].search(
                cond, limit=1)
            if sale:
                num_order = self.origin             
        return num_order

    @api.multi
    def get_total_weight_for_certificacion(self):
        self.ensure_one()
        total_weight = 0
        if self.move_lines:
            total_weight = self.move_lines[0].product_uom_qty
        return total_weight

    @api.multi
    def get_container_type_for_certificacion(self):
        self.ensure_one()
        container_type = ""
        if self.origin:
            cond = [("name", "=", self.origin)]
            sale = self.env["sale.order"].search(
                cond, limit=1)
            if (sale and sale.order_line and
                    sale.order_line[0].pri_pack):
                container_type = (
                    sale.order_line[0].pri_pack.name)           
        return container_type

    @api.multi
    def get_labeling_to_container_for_certificacion(self):
        self.ensure_one()
        name = ""
        if self.move_lines:
            name = self.move_lines[0].product_id.name_get()[0][1]
        return name
        