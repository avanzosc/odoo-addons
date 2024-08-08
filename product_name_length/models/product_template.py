# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.constrains("name")
    def _check_product_name_lenght(self):
        product_name_max_length = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_name_max_length", default=55)
        )
        for template in self:
            if len(template.name) > product_name_max_length:
                raise ValidationError(
                    _("The length of the product name exceeds %s characters.")
                    % product_name_max_length
                )
