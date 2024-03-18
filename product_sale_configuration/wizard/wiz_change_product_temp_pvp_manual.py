# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


class WizChangeProductTempPvpManual(models.TransientModel):
    _name = "wiz.change.product.temp.pvp.manual"
    _description = "Wizard for change in product template field manual PsP"

    manual_pvp = fields.Boolean(string='Manual PSP', value=False)

    @api.multi
    def button_change_manual_pvp(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        products = self.env['product.template'].browse(active_ids)
        if products:
            products.write(
                {'manual_pvp': self.manual_pvp})
            products._onchange_category_sale_price()
        return {'type': 'ir.actions.act_window_close'}
