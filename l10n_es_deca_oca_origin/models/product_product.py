from odoo import _, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    def unlink(self):
        transport_product = self.env.ref(
            "l10n_es_deca_oca_origin.product_product_deca_transport"
        )
        for product in self:
            if product.id == transport_product.id:
                raise ValidationError(
                    _(
                        "You cannot delete the product: '%s',  because it"
                        " is a product registered in the system."
                    )
                    % product.display_name
                )
        return super().unlink()
