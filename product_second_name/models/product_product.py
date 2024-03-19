# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    name2 = fields.Char(string="Product name on sales", translate=True)
    last_date_description_for_sale_by_language = fields.Date(
        string="Last date description for sale by language"
    )
    description_sale_es = fields.Char(
        string="Name of the product in sales (Spanish)", copy=False
    )
    description_sale_en = fields.Char(
        string="Name of the product in sales (English)", copy=False
    )
    description_sale_cat = fields.Char(
        string="Name of the product in sales (Catalan)", copy=False
    )
    allowed_location = fields.Char(string="Allowed location")

    @api.model
    def create(self, values):
        if "default_name2" in self.env.context:
            values["name2"] = self.env.context.get("default_name2")
        if "default_description_sale_es" in self.env.context:
            values["description_sale_es"] = self.env.context.get(
                "default_description_sale_es"
            )
        if "default_description_sale_en" in self.env.context:
            values["description_sale_en"] = self.env.context.get(
                "default_description_sale_en"
            )
        if "default_description_sale_cat" in self.env.context:
            values["description_sale_cat"] = self.env.context.get(
                "default_description_sale_cat"
            )
        if "name2" not in values or not values.get("name2", ""):
            values["name2"] = "*****"
        if "description_sale_es" not in values or not values.get(
            "description_sale_es", ""
        ):
            if values.get("name2") == "*****":
                values["description_sale_es"] = "*****"
            else:
                if self.env.user.lang == "es_ES":
                    values["description_sale_es"] = values.get("name2")
                else:
                    values["description_sale_es"] = "*****"
        else:
            if values.get("name2") == "*****":
                values["name2"] = values.get("description_sale_es")
        if "description_sale_en" not in values or not values.get(
            "description_sale_en", ""
        ):
            if values.get("name2") == "*****":
                values["description_sale_en"] = "*****"
            else:
                if self.env.user.lang == "en_US":
                    values["description_sale_en"] = values.get("name2")
                else:
                    values["description_sale_en"] = "*****"
        else:
            if values.get("name2") == "*****":
                values["name2"] = values.get("description_sale_en")
        if "description_sale_cat" not in values or not values.get(
            "description_sale_cat", ""
        ):
            if values.get("name2") == "*****":
                values["description_sale_cat"] = "*****"
            else:
                if self.env.user.lang == "ca_ES":
                    values["description_sale_cat"] = values.get("name2")
                else:
                    values["description_sale_cat"] = "*****"
        else:
            if values.get("name2") == "*****":
                values["name2"] = values.get("description_sale_cat")
        product = super(
            ProductProduct,
            self.with_context(
                default_name2=values.get("name2"),
                default_description_sale_es=values.get("description_sale_es"),
                default_description_sale_en=values.get("description_sale_en"),
                default_description_sale_cat=values.get("description_sale_cat"),
            ),
        ).create(values)
        product.create_translations()
        return product

    def create_translations(self):
        translation_obj = self.env["ir.translation"]
        cond = [("active", "=", True)]
        langs = self.env["res.lang"].search(cond)
        for lang in langs:
            cond = [
                ("name", "=", "product.product,name2"),
                ("type", "=", "model"),
                ("res_id", "=", self.id),
                ("lang", "=", lang.code),
            ]
            translation = translation_obj.search(cond, limit=1)
            vals = {}
            if lang.code == "es_ES":
                vals["value"] = self.description_sale_es
            if lang.code == "ca_ES":
                vals["value"] = self.description_sale_cat
            if lang.code == "en_US":
                vals["value"] = self.description_sale_en
            if vals.get("value") == "*****":
                vals["state"] = "to_translate"
            else:
                vals["state"] = "translated"
            if not translation:
                vals.update(
                    {
                        "name": "product.product,name2",
                        "type": "model",
                        "res_id": self.id,
                        "lang": lang.code,
                        "scr": self.name2,
                    }
                )
                translation_obj.create(vals)
            else:
                translation.write(vals)

    @api.multi
    def write(self, values):
        if "from_cron" in self.env.context:
            return super().write(values)
        translation_obj = self.env["ir.translation"]
        if "description_sale_es" in values:
            super(
                ProductProduct,
                self.with_context(lang="es_ES", language_description=True),
            ).write({"name2": values.get("description_sale_es")})
        if "description_sale_cat" in values:
            super(
                ProductProduct,
                self.with_context(lang="ca_ES", language_description=True),
            ).write({"name2": values.get("description_sale_cat")})
        if "description_sale_en" in values:
            for product in self:
                cond = [
                    ("name", "=", "product.product,name2"),
                    ("type", "=", "model"),
                    ("res_id", "=", product.id),
                    ("lang", "=", "en_US"),
                    ("state", "=", "to_translate"),
                ]
                translation = translation_obj.search(cond, limit=1)
                if not translation:
                    cond = [
                        ("name", "=", "product.product,name2"),
                        ("type", "=", "model"),
                        ("res_id", "=", product.id),
                        ("lang", "=", "en_US"),
                        ("state", "=", "translated"),
                    ]
                    translation = translation_obj.search(cond, limit=1)
                if translation:
                    translation_vals = {
                        "state": "translated",
                        "src": values.get("description_sale_en"),
                        "value": values.get("description_sale_en"),
                    }
                    translation.sudo().with_context(language_description=True).write(
                        translation_vals
                    )
        result = super().write(values)
        if "update_name2_data_from_template" not in self.env.context and (
            "name2" in values
            or "description_sale_es" in values
            or "description_sale_cat" in values
            or "description_sale_en" in values
        ):
            for product in self.filtered(
                lambda x: x.product_tmpl_id.product_variant_count == 1
            ):
                if "name2" in values:
                    product.product_tmpl_id.with_context(
                        update_name2_data_from_product=True
                    ).write({"name2": values.get("name2")})
                if "description_sale_es" in values:
                    product.product_tmpl_id.with_context(
                        update_name2_data_from_product=True
                    ).write({"description_sale_es": values.get("description_sale_es")})
                if "description_sale_cat" in values:
                    product.product_tmpl_id.with_context(
                        update_name2_data_from_product=True
                    ).write(
                        {"description_sale_cat": values.get("description_sale_cat")}
                    )
                if "description_sale_en" in values:
                    product.product_tmpl_id.with_context(
                        update_name2_data_from_product=True
                    ).write({"description_sale_en": values.get("description_sale_en")})
        return result

    def _ir_cron_name_products_by_language(self):
        translation_obj = self.env["ir.translation"]
        cond = [
            "|",
            ("last_date_description_for_sale_by_language", "=", False),
            (
                "last_date_description_for_sale_by_language",
                "!=",
                fields.Date.context_today(self),
            ),
        ]
        templates = self.env[("product.template")].search(cond)
        for template in templates:
            template.with_context(
                update_name2_data_from_product=True, from_cron=True
            ).put_description_sale_lang()
            if template.product_variant_count == 1:
                cond = [
                    ("name", "=", "product.product,name2"),
                    ("type", "=", "model"),
                    ("res_id", "=", template.product_variant_ids[0].id),
                ]
                translations = translation_obj.search(cond)
                if translations:
                    translations.unlink()
                cond = [
                    ("name", "=", "product.template,name2"),
                    ("type", "=", "model"),
                    ("res_id", "=", template.id),
                ]
                translations = translation_obj.search(cond)
                if translations:
                    for translation in translations:
                        variant = template.product_variant_ids[0]
                        translation.with_context(
                            language_description=True, from_cron=True
                        ).copy(
                            {
                                "name": "product.product,name2",
                                "state": translation.state,
                                "res_id": variant.id,
                            }
                        )
                        if translation.lang == "es_ES":
                            variant.with_context(
                                from_cron=True
                            ).description_sale_es = template.description_sale_es
                        if translation.lang == "ca_ES":
                            variant.with_context(
                                from_cron=True
                            ).description_sale_cat = template.description_sale_cat
                        if translation.lang == "en_US":
                            variant.with_context(
                                from_cron=True
                            ).description_sale_en = template.description_sale_en
                template.product_variant_ids[0].with_context(
                    from_cron=True
                ).last_date_description_for_sale_by_language = fields.Date.context_today(
                    self
                )
            template.with_context(
                from_cron=True
            ).last_date_description_for_sale_by_language = fields.Date.context_today(
                self
            )
            self._cr.commit()
