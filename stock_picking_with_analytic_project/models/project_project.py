# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _compute_picking_count(self):
        for project in self.filtered(lambda x: x.analytic_account_id):
            cond = [('analytic_account_id', '=',
                     project.analytic_account_id.id)]
            pickings = self.env['stock.picking'].search(cond)
            project.picking_count = len(pickings)

    picking_count = fields.Integer(
        string='Pickings', compute='_compute_picking_count')

    def show_pickings_from_project(self):
        res = {}
        if self.analytic_account_id:
            cond = [('analytic_account_id', '=', self.analytic_account_id.id)]
            pickings = self.env['stock.picking'].search(cond)
            res = {'view_mode': 'tree,kanban,form,calendar',
                   'res_model': 'stock.picking',
                   'view_id': False,
                   'type': 'ir.actions.act_window',
                   'view_type': 'form',
                   'domain': [('id', 'in', pickings.ids)]}
        return res
