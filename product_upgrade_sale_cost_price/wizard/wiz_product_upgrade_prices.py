# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class WizProductUpgradePrices(models.TransientModel):
    _name = 'wiz.product.upgrade.prices'
    _description = 'Wizard for upgrade sale and cost price in products'

    increase_sale_price = fields.Boolean(
        string='Increase/Decrease sale price', default=False)
    sale_increase = fields.Float(
        string='Increment/Decrement', digits=(1, 3), default=0,
        help='By default an increase in the sale price of 1.4%. If you enter'
        ' amount in negative, the amount is decremented')
    increase_cost_price = fields.Boolean(
        string='Increase/Decrease cost price', default=False)
    cost_increase = fields.Float(
        string='Increment/Decrement', digits=(1, 3), default=0,
        help='By default an increase in the cost price of 1.4%. If you enter'
        ' amount in negative, the amount is decremented')

    @api.onchange('increase_sale_price')
    def onchange_increase_sale_price(self):
        self.sale_increase = 0.014 if self.increase_sale_price else 0

    @api.onchange('increase_cost_price')
    def onchange_increase_cost_price(self):
        self.cost_increase = 0.014 if self.increase_cost_price else 0

    @api.multi
    def update_product_prices(self):
        if self.sale_increase or self.cost_increase:
            products = self.env['product.product'].browse(
                self.env.context.get('active_ids'))
            products._upgrade_sale_and_cost_price_from_wizard(
                self.sale_increase, self.cost_increase)
