# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
import json

import logging

_logger = logging.getLogger(__name__)


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
        cond = [("active", "=", True)]
        langs = self.env["res.lang"].search(cond)
        for lang in langs:
            vals = {}
            if lang.code == "es_ES":
                vals["description_sale_es"] = self.description_sale_es
            elif lang.code == "ca_ES":
                vals["description_sale_cat"] = self.description_sale_cat
            elif lang.code == "en_US":
                vals["description_sale_en"] = self.description_sale_en

            # Check if the translation field is empty for the current language
            if isinstance(self.name2, dict) and not self.name2.get(lang.code):
                vals[lang.code] = "to_translate" if not vals else "translated"

            # Update or create the translation for the current language
            self.write(vals)


    def write(self, values):
        if "product_created_from_template" in self.env.context:
            return True
        if "from_cron" in self.env.context:
            return super().write(values)
        
        name2_values = {}

        if "description_sale_es" in values:
            name2_values["es_ES"] = values.get("description_sale_es")

        if "description_sale_cat" in values:
            name2_values["ca_ES"] = values.get("description_sale_cat")

        if "description_sale_en" in values:
            name2_values["en_US"] = values.get("description_sale_en")

        # Update name2 with the accumulated translation values using SQL
        if name2_values:
            for lang in name2_values:
                query = """
                    UPDATE product_product
                    SET name2 = jsonb_set(
                        COALESCE(name2, '{}'),
                        ARRAY[%s],
                        %s::jsonb,
                        true
                    )
                    WHERE id = %s
                """
                self.env.cr.execute(query, (
                    lang,  
                    json.dumps(name2_values[lang]),  # Serialize the dictionary value to JSON
                    self.id
                ))

        result = super().write(values)

        # If name2 or any of the translation fields is updated, propagate the changes to product variant
        if "update_name2_data_from_product" not in self.env.context and (
            "name2" in values
            or "description_sale_es" in values
            or "description_sale_cat" in values
            or "description_sale_en" in values
        ):
            for product in self.filtered(lambda x: x.product_variant_count == 1):
                # Update the corresponding fields in the product variant with the same values
                product.product_tmpl_id.with_context(
                    update_name2_data_from_product=True
                ).write(values)
                
                
                # Update name2 with the accumulated translation values using SQL
                if name2_values:
                    for lang in name2_values:
                        query = """
                            UPDATE product_template
                            SET name2 = jsonb_set(
                                COALESCE(name2, '{}'),
                                ARRAY[%s],
                                %s::jsonb,
                                true
                            )
                            WHERE id = %s
                        """
                        self.env.cr.execute(query, (
                            lang,
                            json.dumps(name2_values[lang]),  # Serialize the dictionary value to JSON
                            product.product_tmpl_id.id
                        ))

                
                
        
        return result

    def _ir_cron_name_products_by_language(self):
        cond = [
            "|",
            ("last_date_description_for_sale_by_language", "=", False),
            (
                "last_date_description_for_sale_by_language",
                "!=",
                fields.Date.context_today(self),
            ),
        ]
        templates = self.env["product.template"].search(cond)
        for template in templates:
            template.with_context(
                update_name2_data_from_product=True, from_cron=True
            ).put_description_sale_lang()

            if template.product_variant_count == 1:
                # Delete existing translations for the product variant
                template.product_variant_ids[0].write({"name2": {}})

                # Copy translations from template to product variant
                for lang_code, translation in template.name2.items():
                    variant = template.product_variant_ids[0]
                    variant.with_context(from_cron=True).write({
                        "name2": {lang_code: translation},
                        "description_sale_es": template.description_sale_es if lang_code == "es_ES" else variant.description_sale_es,
                        "description_sale_cat": template.description_sale_cat if lang_code == "ca_ES" else variant.description_sale_cat,
                        "description_sale_en": template.description_sale_en if lang_code == "en_US" else variant.description_sale_en,
                        "last_date_description_for_sale_by_language": fields.Date.context_today(self)
                    })

            template.with_context(from_cron=True).write({
                "last_date_description_for_sale_by_language": fields.Date.context_today(self)
            })
            self._cr.commit()
