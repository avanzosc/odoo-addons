# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_show_stock_move_deno = fields.Boolean(
        string="Show stock move description in picking form",
        implied_group="stock_usability.group_show_stock_move_deno")
