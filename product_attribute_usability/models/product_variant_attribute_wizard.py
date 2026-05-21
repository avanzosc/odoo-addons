from odoo import models, fields, _
from odoo.exceptions import UserError


class ProductVariantAttributeWizard(models.TransientModel):
    _name = "product.variant.attribute.wizard"
    _description = "Replace Variant Attribute Value"

    attribute_id = fields.Many2one(
        "product.attribute",
        required=True,
    )
    old_value_id = fields.Many2one(
        "product.attribute.value",
        required=True,
        string="Old Value",
    )
    new_value_id = fields.Many2one(
        "product.attribute.value",
        required=True,
        string="New Value",
    )

    def action_replace_value(self):
        self.ensure_one()

        if self.old_value_id.attribute_id != self.attribute_id:
            raise UserError(_("Old value does not belong to selected attribute."))

        if self.new_value_id.attribute_id != self.attribute_id:
            raise UserError(_("New value does not belong to selected attribute."))

        if self.old_value_id == self.new_value_id:
            raise UserError(_("Old value and new value must be different."))

        active_ids = self.env.context.get("active_ids", [])

        reports = self.env["product_variant_attribute_report"].browse(active_ids)
        product_ids = reports.mapped("product_id").ids

        cr = self.env.cr

        cr.execute("""
            INSERT INTO product_attribute_value_product_template_attribute_line_rel
                (product_template_attribute_line_id, product_attribute_value_id)
            SELECT DISTINCT
                ptal.id,
                %s
            FROM product_product pp
            JOIN product_template_attribute_line ptal
                ON ptal.product_tmpl_id = pp.product_tmpl_id
            WHERE pp.id = ANY(%s)
              AND ptal.attribute_id = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM product_attribute_value_product_template_attribute_line_rel rel
                  WHERE rel.product_template_attribute_line_id = ptal.id
                    AND rel.product_attribute_value_id = %s
              )
        """, [
            self.new_value_id.id,
            product_ids,
            self.attribute_id.id,
            self.new_value_id.id,
        ])

        cr.execute("""
            DELETE FROM product_attribute_value_product_product_rel
            WHERE product_product_id = ANY(%s)
              AND product_attribute_value_id = %s
        """, [
            product_ids,
            self.old_value_id.id,
        ])

        cr.execute("""
            INSERT INTO product_attribute_value_product_product_rel
                (product_product_id, product_attribute_value_id)
            SELECT
                pp.id,
                %s
            FROM product_product pp
            WHERE pp.id = ANY(%s)
              AND NOT EXISTS (
                  SELECT 1
                  FROM product_attribute_value_product_product_rel rel
                  WHERE rel.product_product_id = pp.id
                    AND rel.product_attribute_value_id = %s
              )
        """, [
            self.new_value_id.id,
            product_ids,
            self.new_value_id.id,
        ])

        return {"type": "ir.actions.act_window_close"}