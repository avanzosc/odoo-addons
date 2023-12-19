# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_total_anual(self):
        for template in self.filtered(lambda c: c.recurrent_punctual):
            if template.recurrent_punctual == 'recurrent':
                months = ((12 - template.month_start.number) +
                          template.end_month.number + 1)
                template.total_annual = template.list_price * months
            if template.recurrent_punctual == 'punctual':
                template.total_annual = (
                    template.list_price * len(template.punctual_month_ids))

    recurrent_punctual = fields.Selection(
        selection=[('recurrent', 'Recurrent'),
                   ('punctual', 'Punctual')], string='Recurrent/Punctual')
    punctual_month_ids = fields.Many2many(
        comodel_name='base.month', string='Punctual months',
        relation='rel_product_base_month',
        column1='product_id', column2='month_id')
    total_annual = fields.Float(
        string='Total annual', compute='_compute_total_anual',
        digits=dp.get_precision('Product Price'))
    month_start = fields.Many2one(
        comodel_name='base.month', string='Month start')
    end_month = fields.Many2one(
        comodel_name='base.month', string='End month')
