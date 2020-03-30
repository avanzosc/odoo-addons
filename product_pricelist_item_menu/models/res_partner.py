# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = 'res.partner'

    count_pricelists_item = fields.Integer(
        string='Count pricelist items',
        compute='_compute_count_pricelists_item')

    def _compute_count_pricelists_item(self):
        for partner in self.filtered(lambda c: c.property_product_pricelist):
            partner.count_pricelists_item = len(
                partner.property_product_pricelist.item_ids)

    @api.multi
    def button_show_partner_pricelist_items(self):
        self.ensure_one()
        action = self.env.ref(
            'product_pricelist_item_menu.product_pricelist_item_menu_action')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(action_dict.get('context', '{}'))
        action_dict['context'].update({
            'search_pricelits_id': self.property_product_pricelist.id,
            'default_pricelist_id': self.property_product_pricelist.id,
        })
        domain = expression.AND([
            [('pricelist_id', '=', self.property_product_pricelist.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
