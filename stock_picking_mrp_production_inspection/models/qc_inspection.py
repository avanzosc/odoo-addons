# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import _, api, fields, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    def _compute_num_mrp_related_out_pickings(self):
        for inspection in self:
            inspection.num_mrp_related_out_pickings = len(
                inspection.mrp_related_out_picking_ids)

    mrp_related_out_picking_ids = fields.Many2many(
        comodel_name="stock.picking",
        relation="rel_picking_related_inspections",
        column1="inspection_id", column2="picking_id",
        string="Related out pickings", copy=False)
    num_mrp_related_out_pickings = fields.Integer(
        string="Num. Related out pickings",
        compute="_compute_num_mrp_related_out_pickings")

    @api.multi
    def button_view_related_out_pickings(self):
        self.ensure_one()
        if self.mrp_related_out_picking_ids:
            return {'name': _('Related out pickings'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'res_model': 'stock.picking',
                    'domain': [('id', 'in',
                                self.mrp_related_out_picking_ids.ids)]} 
        