# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
try:
    from openerp.addons.quality_control.models.qc_trigger_line import\
        _filter_trigger_lines
except:
    _filter_trigger_lines = None


class Inventory(models.Model):
    _inherit = 'stock.inventory'

    @api.depends('qc_inspection_ids')
    def _compute_inspections(self):
        for record in self:
            record.created_inspections = len(record.qc_inspection_ids)

    qc_inspection_ids = fields.One2many(
        comodel_name='qc.inspection', inverse_name='inventory_id', copy=False,
        string='Inspections', help="Inspections related to this inventory.")
    created_inspections = fields.Integer(
        compute="_compute_inspections", string="Created inspections")


class InventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.model
    def _resolve_inventory_line(self, line):
        move_id = super(InventoryLine, self)._resolve_inventory_line(line)
        move = self.env['stock.move'].browse(move_id)
        inspection_model = self.env['qc.inspection']
        qc_trigger = self.env.ref(
            'quality_control_stock_inventory.qc_trigger_inventory')
        trigger_lines = set()
        for model in ['qc.trigger.product_category_line',
                      'qc.trigger.product_template_line',
                      'qc.trigger.product_line']:
            trigger_lines = trigger_lines.union(
                self.env[model].get_trigger_line_for_product(
                    qc_trigger, move.product_id))
        for trigger_line in _filter_trigger_lines(trigger_lines):
            inspection_model.with_context(
                default_inventory_line_id=line.id)._make_inspection(
                    move, trigger_line)
        return move_id
