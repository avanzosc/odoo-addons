# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from openerp import api, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if not name == '':
            args += ['|', ('ref', operator, name)]
        results = super(StockProductionLot,
                        self).name_search(name, args, operator, limit)
        return results

    @api.multi
    def name_get(self):
        res = []
        for lot in self:
            p_name = '[' + lot.name + '] ' or ''
            p_name += lot.ref and lot.ref or ''
            res.append((lot.id, p_name))
        return res

    @api.multi
    def do_print_lot_report(self):
        return self.env['report'].get_action(self, 'stock.report_lot_barcode')
