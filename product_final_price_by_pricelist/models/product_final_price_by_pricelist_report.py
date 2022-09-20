# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from psycopg2.extensions import AsIs


class ProductFinalPriceByPricelist(models.Model):
    _name = "product.final.price.by.pricelist.report"
    _description = "Product final price by pricelist List"
    _auto = False
    _rec_name = "product_final_id"
    _order = "product_final_id, pricelist_id, product_id"

    product_final_id = fields.Many2one(
        comodel_name="product.final", string="Final Product")
    position = fields.Char(string="Position")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product")
    pricelist_id = fields.Many2one(
        string="Pricelist", comodel_name="product.pricelist")
    price_unit = fields.Float(
        string="Unit Price", digits=dp.get_precision("Product Price"),
        default=0.0)

    _depends = {
        "product.location.exploded": [
            "product_final_id", "position", "product_id",
        ],
        "product.price.by.pricelist": [
            "product_id", "pricelist_id", "price_unit",
        ],
    }

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER () as id,
                product_final.product_final_id as product_final_id,
                product_final.position as position,
                product_final.product_id as product_id,
                product_price.pricelist_id as pricelist_id,
                product_price.price_unit as price_unit
        """
        return select_str

    def _from(self):
        from_str = """
                FROM product_location_exploded product_final
                JOIN product_price_by_pricelist product_price ON
                    product_final.product_id = product_price.product_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                product_final.product_final_id,
                product_final.position,
                product_final.product_id,
                product_price.pricelist_id,
                product_price.price_unit
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()), AsIs(self._from()),
                AsIs(self._group_by()),))
