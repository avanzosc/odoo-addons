# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductMake(models.Model):
    _name = "product.make"
    _description = "Products makes"

    name = fields.Char(string="Description", required=True)
    print_make_on_out_picking = fields.Boolean(
        string="Print make on out picking", default=False
    )
    logo = fields.Binary("Image", attachment=True)
    use_logo = fields.Boolean(
        string="Use this logo to print for other makes that do not have a logo",
        default=False,
    )
    three_address_in_sale_report = fields.Boolean(
        string="Show all three addresses in sales reports ", default=True
    )
    common_logo = fields.Binary("Image", attachment=True)
    sale_fiscal_position_id = fields.Many2one(
        comodel_name="account.fiscal.position",
        string="Fiscal position for sales",
    )
    market_to_print_ids = fields.Many2many(
        string="Market to print on out picking", comodel_name="res.partner.market"
    )
