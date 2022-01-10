# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _compute_packages_qty_weight(self):
        for picking in self:
            picking.packages_qty_weight = u'{} {} {} {}'.format(
                len(picking.quant_package_ids), '-',
                sum(picking.quant_package_ids.mapped('shipping_weight')),
                picking.weight_uom_name)

    quant_package_ids = fields.One2many(
        string='Packages', comodel_name='stock.quant.package',
        inverse_name='picking_id')
    packages_qty_weight = fields.Char(
        string='# Packages', compute='_compute_packages_qty_weight')
    qty_packages = fields.Integer(string='Number of Packages')

    def action_view_package(self):
        context = self.env.context.copy()
        context.update({'default_picking_id': self.id})
        return {
            'name': _("Packages"),
            'view_mode': 'tree',
            'res_model': 'stock.quant.package',
            'domain': [('id', 'in', self.quant_package_ids.ids)],
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref(
                'stock_picking_package_usability.stock_quant_package_view_tree'
                ).id,
            'context': context
        }

    def action_create_package(self):
        self.ensure_one()
        pack_vals = {
            'picking_id': self.id}
        for i in range(1, self.qty_packages + 1):
            name = u'{} {} {}{}'.format(self.name, '-', '00', i)
            pack_vals.update({'name': name})
            self.env['stock.quant.package'].create(pack_vals)

    def _put_in_pack(self, move_line_ids, create_package_level=True):
        move_line_ids = move_line_ids.filtered(
                    lambda x: not x.result_package_id)
        if move_line_ids:
            return super(StockPicking, self)._put_in_pack(
                move_line_ids, create_package_level=True)
