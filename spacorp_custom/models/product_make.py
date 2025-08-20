# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductMeke(models.Model):
    _inherit = "product.make"

    market_to_print_ids = fields.Many2many(
        string="Market to print on out picking", comodel_name="res.partner.market"
    )
