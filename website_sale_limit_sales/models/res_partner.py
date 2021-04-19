
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    limit_purchases_day = fields.Bool(string="Sale order limitation per days",
                                           help="")