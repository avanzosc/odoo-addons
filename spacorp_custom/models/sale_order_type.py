# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    analytic_account_id = fields.Many2one(
        string="Analytic account", comodel_name="account.analytic.account"
    )
