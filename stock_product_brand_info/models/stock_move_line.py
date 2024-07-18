# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_brand_code = fields.Char(
        compute="_compute_brand_info",
        store=True,
        copy=False,
    )
    brand_fabricators = fields.Char(
        compute="_compute_brand_info",
        store=True,
        copy=False,
    )

    @api.depends(
        "product_id",
        "product_id.product_tmpl_id",
        "product_id.product_tmpl_id.seller_ids",
        "product_id.product_tmpl_id.seller_ids.partner_id",
        "product_id.product_tmpl_id.seller_ids.product_brand_id",
        "product_id.product_tmpl_id.seller_ids.product_brand_id.code",
        "product_id.product_tmpl_id.seller_ids.product_brand_id",
    )
    def _compute_brand_info(self):
        for move in self:
            product_brand_code = ""
            brand_fabricators = ""
            if move.product_id:
                sellers = move.product_id.seller_ids.filtered(
                    lambda x: x.product_brand_id and x.product_brand_id.code
                )
                for seller in sellers:
                    brand_code = seller.product_brand_id.code
                    product_brand_code = (
                        brand_code
                        if not product_brand_code
                        else "{}, {}".format(product_brand_code, brand_code)
                    )
                    partner_name = seller.partner_id.name
                    brand_fabricators = (
                        partner_name
                        if not brand_fabricators
                        else "{}, {}".format(brand_fabricators, partner_name)
                    )
            move.product_brand_code = product_brand_code
            move.brand_fabricators = brand_fabricators

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)
        in_picking_lines = self.filtered(lambda x: x.picking_code == "incoming")
        if not result or len(self) != len(in_picking_lines):
            return result
        for clave in result.keys():
            for move_line in self:
                line_key = self._generate_keys_to_found()
                if line_key in clave:
                    result[clave]["fabricator"] = (
                        ""
                        if not move_line.brand_fabricators
                        else move_line.brand_fabricators
                    )
                    result[clave]["brand_code"] = (
                        ""
                        if not move_line.product_brand_code
                        else move_line.product_brand_code
                    )
        return result

    def _generate_keys_to_found(self):
        uom = self.product_uom_id
        name = self.product_id.display_name
        description = self.move_id.description_picking
        product = self.product_id
        if description == name or description == self.product_id.name:
            description = False
        line_key = f'{product.id}_{product.display_name}_{description or ""}_{uom.id}'
        return line_key
