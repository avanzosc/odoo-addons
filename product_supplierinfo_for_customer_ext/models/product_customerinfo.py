# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductCustomerInfo(models.Model):
    _inherit = "product.customerinfo"

    @api.model
    def create(self, vals):
        if ("params" in self.env.context and
            "model" in self.env.context.get("params",{}) and
            self.env.context.get("params").get(
                "model", "aa") == "product.product"):
            vals['product_id'] = self.env.context.get("params").get("id", "aa")
        if ("product_id" in vals and vals.get("product_id", False) and
                "product_tmpl_id" not in vals):
            product = self.env["product.product"].browse(
                vals.get("product_id"))
            vals["product_tmpl_id"] = product.product_tmpl_id.id
        customer_info = super(ProductCustomerInfo, self).create(vals)
        return customer_info

    def write(self, vals):
        if 'product_tmpl_id' in vals and not vals.get('product_tmpl_id'):
            del vals['product_tmpl_id']
        if ("product_id" in vals and vals.get("product_id", False) and
                "product_tmpl_id" not in vals):
            product = self.env["product.product"].browse(
                vals.get("product_id"))
            vals["product_tmpl_id"] = product.product_tmpl_id.id
        if "product_id" not in vals and "product_tmpl_id" not in vals:
            print ('222 entro por 2')
            for info in self:
                my_vals = vals.copy()
                if info.product_id and not info.product_tmpl_id:
                    my_vals["product_tmpl_id"] = (
                        info.product_id.product_tmpl_id.id)
                super(ProductCustomerInfo, info).write(my_vals)
        else:
            return super(ProductCustomerInfo, self).write(vals)

    def ir_cron_fix_product_producttmpl_in_product_customerinfo(self):
        product_obj = self.env['product.product']
        cond = [('product_id', '!=', False),
                ('product_tmpl_id', '=', False)]
        infos = self.env['product.customerinfo'].search(cond)
        for info in infos:
            info.product_tmpl_id = info.product_id.product_tmpl_id.id
        cond = [('product_id', '=', False),
                ('product_tmpl_id', '!=', False)]
        infos = self.env['product.customerinfo'].search(cond)
        for info in infos:
            if len(info.product_tmpl_id.product_variant_ids) == 1:
                info.product_id = (
                    info.product_tmpl_id.product_variant_ids[0].id)
            if (len(info.product_tmpl_id.product_variant_ids) > 1 and
                    info.product_name):
                cond = [('name', '=', info.product_name)]
                product = product_obj.search(cond)
                if product and len(product) == 1:
                    info.product_id = product.id
            if len(info.product_tmpl_id.product_variant_ids) == 0:
                cond = [("product_tmpl_id", '=', info.product_tmpl_id.id)]
                product = product_obj.search(cond)
                if product and len(product) == 1:
                    info.product_id = product.id
