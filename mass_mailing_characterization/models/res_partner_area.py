# Copyright 2019 Roberto Lizana - Trey, Jorge Camacho - Trey
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResPartnerArea(models.Model):
    _inherit = 'res.partner.area'

    fixed = fields.Boolean(
        string='Fixed')
