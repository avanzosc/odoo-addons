# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_supplier_move_price = fields.Float(
        string="Last supplier move price", digits="Product Price"
    )
    last_supplier_move_date = fields.Date(string="Last supplier move date")
    last_supplier_move_id = fields.Many2one(
        comodel_name="res.partner", string="Last supplier move"
    )

    def set_product_template_last_purchase_move(
        self,
        last_supplier_move_date,
        last_supplier_move_price,
        last_supplier_move_id,
    ):
        return self.write(
            {
                "last_supplier_move_date": last_supplier_move_date,
                "last_supplier_move_price": last_supplier_move_price,
                "last_supplier_move_id": (
                    last_supplier_move_id.id if last_supplier_move_id else False
                ),
            }
        )
