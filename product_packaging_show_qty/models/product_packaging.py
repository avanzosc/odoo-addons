# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    def name_get(self):
        res = []
        for packaging in self:
            if packaging.qty and packaging.product_uom_id:
                name = _("%(packaging_name)s (%(packaging_qty)s %(uom_name)s)") % {
                    "packaging_name": packaging.name,
                    "packaging_qty": packaging.qty,
                    "uom_name": packaging.product_uom_id.name,
                }
            res.append(
                (
                    packaging.id,
                    name,
                )
            )
        return res
