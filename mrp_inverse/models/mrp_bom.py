# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    inverse = fields.Boolean(string='Inverse', default=False)

    @api.multi
    def create_mrp_production(self):
        """ Create a manufacturing order from this BoM
        """
        self.ensure_one()

        production = self.env['mrp.production'].create({
            'bom_id': self.id,
            'inverse': self.inverse,
            'product_id': self._get_product().id,
            'product_qty': self.product_qty,
            'product_uom': self.product_uom.id,
        })

        return self._get_form_view('mrp.production', production)

    def _get_form_view(self, model_name, entity):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': model_name,
            'target': 'current',
            'res_id': entity.id,
            'context': self.env.context
        }

    def _get_product(self):
        if not self.product_id:
            return self.product_tmpl_id.product_variant_ids[:1]
        else:
            return self.product_id
