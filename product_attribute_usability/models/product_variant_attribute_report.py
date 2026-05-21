
# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, tools


class ProductVariantAttributeReport(models.Model):
    _name = 'product_variant_attribute_report'
    _description = 'Product Variant Attribute Report'
    _auto = False
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product',
        string='Variant',
        readonly=True,
    )

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        readonly=True,
    )

    attribute_id = fields.Many2one(
        'product.attribute',
        string='Attribute',
        readonly=True,
    )

    value_id = fields.Many2one(
        'product.attribute.value',
        string='Value',
        readonly=True,
    )


    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        self.env.cr.execute("""
    CREATE OR REPLACE VIEW product_variant_attribute_report AS (

        SELECT
            row_number() OVER() AS id,

            pp.id AS product_id,
            pt.id AS product_tmpl_id,

            pav.attribute_id AS attribute_id,
            pav.id AS value_id

        FROM product_product pp

        JOIN product_template pt
            ON pt.id = pp.product_tmpl_id

        JOIN product_attribute_value_product_product_rel rel
            ON rel.product_product_id = pp.id

        JOIN product_attribute_value pav
            ON pav.id = rel.product_attribute_value_id

    )
    """)
        
    def action_open_product_template(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": "form",
            "res_id": self.product_tmpl_id.id,
            "target": "current",
        }
    
    def action_open_product_variant(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "view_mode": "form",
            "res_id": self.product_id.id,
            "target": "current",
        }
    
    def action_open_attribute(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.attribute",
            "view_mode": "form",
            "res_id": self.attribute_id.id,
            "target": "current",
        }

        
    def action_open_replace_attribute_wizard(self):
        action = self.env.ref(
            "product_attribute_usability.action_product_variant_attribute_wizard"
        ).read()[0]
        action["context"] = dict(
            self.env.context,
            active_ids=self.ids,
            active_model="product_variant_attribute_report",
        )
        return action