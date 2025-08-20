# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLineAgent(models.Model):
    _inherit = "sale.order.line.agent"

    active = fields.Boolean(string="Active", default=True)
