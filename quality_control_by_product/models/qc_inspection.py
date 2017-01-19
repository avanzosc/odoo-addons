# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class QcInspection(models.Model):

    _inherit = 'qc.inspection'

    @api.multi
    def _get_load_line(self, line):
        inspections = self.search([('lot', '=', self.lot.id)])
        lot_inspections = inspections.filtered(
            lambda x: (x.object_id._name == 'stock.move' or
                       x.object_id._name == 'stock.pack.operation') and
            x.object_id.location_id.usage == 'supplier')
        lines = self.env['qc.inspection.line'].search(
            [('inspection_id', 'in', lot_inspections.ids),
             ('test_line', '=', line.id)])
        if not lines:
            lines = self.env['qc.inspection.line'].search(
                [('inspection_id', 'in', lot_inspections.ids),
                 ('test_line.name', '=', line.name)])
        return lines[:1]

    @api.multi
    def need_autoload(self):
        self.ensure_one()
        if self.lot:
            if self.object_id._name == 'stock.move' or \
                    self.object_id._name == 'stock.pack.operation':
                if self.object_id.location_dest_id.usage == 'customer':
                    return True
        return False

    def _prepare_inspection_line(self, test, line, fill=None):
        data = super(QcInspection, self)._prepare_inspection_line(test, line,
                                                                  fill=fill)
        if self.need_autoload():
            load_line = self._get_load_line(line)
            data['qualitative_value'] = load_line.qualitative_value.id
            data['quantitative_value'] = load_line.quantitative_value
        return data
