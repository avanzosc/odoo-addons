# Copyright 2015 Daniel Campos - AvanzOSC
# Copyright 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    machine_ok = fields.Boolean(
        string="Can be a Machine",
        help="Determines if the product is related with a machine.",
        default=False,
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    machine_ids = fields.One2many(
        string="Machines",
        comodel_name="machine",
        inverse_name="product_id",
    )
    machine_count = fields.Integer(
        compute="_compute_machine_count",
    )

    def _compute_machine_count(self):
        read_group = self.env["machine"]._read_group(
            domain=[("product_id", "in", self.ids)],
            groupby=["product_id"],
            aggregates=["__count"],
        )
        counts = {product.id: count for product, count in read_group}
        for product in self:
            product.machine_count = counts.get(product.id, 0)
