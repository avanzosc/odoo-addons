# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _renovate_sale_and_contract_from_wizard(self):
        for sale in self:
            new_sale = sale.copy()
            vals = {'date_start': (
                    fields.Date.from_string(sale.project_id.date) +
                    relativedelta(days=1)),
                    'date': (fields.Date.from_string(sale.project_id.date) +
                             relativedelta(years=1))}
            new_sale.project_id = sale.project_id.copy(vals)
            new_sale._update_new_sale_contract_information(sale)
            sale.project_id.set_close()
            new_sale.project_id.set_open()

    def _update_new_sale_contract_information(self, origin_sale):
        self.project_id.name = self.name
        if origin_sale.name != origin_sale.project_id.name:
            self.project_id.name = '{} {}'.format(
                origin_sale.project_id.name,
                fields.Date.from_string(self.project_id.date_start).year)
