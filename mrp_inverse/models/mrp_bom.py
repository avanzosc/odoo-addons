# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    inverse = fields.Boolean(string='Inverse', default=False)

    @api.multi
    def create_mrp_production(self):
        """
        Create a manufacturing order from a BoM
        """
        self.ensure_one()
        production_obj = self.env['mrp.production']
        update_data = {
            'bom_id': self.id,
            'routing_id': self.routing_id.id,
            'inverse': self.inverse,
            'product_qty': self.product_qty,
            'product_uom': self.product_uom.id,
        }
        product_data = self._get_product()
        product_data.update(update_data)
        production_data = production_obj.new(product_data)
        try:
            if not self.product_id and production_data.product_tmpl_id:
                production_data.product_id = False
            production_data.onchange_product_tmpl_id()
        except:
            pass
        data = production_data._convert_to_write(production_data._cache)
        data.update(update_data)
        production = self.env['mrp.production'].create(data)
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
        product_dict = {
            'product_tmpl_id': self.product_tmpl_id.id,
            'product_id': self.product_id.id or
            self.product_tmpl_id.product_variant_ids[:1].id,
        }
        return product_dict
