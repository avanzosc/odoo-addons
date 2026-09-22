# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    market_id = fields.Many2one(
        string="Sale channel",
        comodel_name="res.partner.market",
        copy=False,
    )
    product_make_id = fields.Many2one(
        string="Make",
        comodel_name="product.make",
        copy=False,
    )
