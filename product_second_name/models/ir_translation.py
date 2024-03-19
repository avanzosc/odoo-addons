# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class IrTranslation(models.Model):
    _inherit = "ir.translation"

    @api.multi
    def write(self, values):
        result = super().write(values)
        if (
            "language_description" not in self.env.context
            and "value" in values
            and values.get("value", False)
        ):
            for translation in self.filtered(
                lambda x: x.name in ("product.template,name2", "product.product,name2")
            ):
                translation.new_name2_tranlation_to_fields()
        return result

    def new_name2_tranlation_to_fields(self):
        product_obj = self.env["product.product"]
        template_obj = self.env["product.template"]
        vals = {}
        if self.lang == "es_ES":
            vals = {"description_sale_es": self.value}
        if self.lang == "ca_ES":
            vals = {"description_sale_cat": self.value}
        if self.lang == "en_US":
            vals = {"description_sale_en": self.value}
        if vals:
            if self.name == "product.template,name2":
                template = template_obj.browse(self.res_id)
                template.write(vals)
            else:
                product = product_obj.browse(self.res_id)
                product.write(vals)
