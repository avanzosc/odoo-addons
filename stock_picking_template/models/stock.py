# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_template = fields.Boolean(string="Template", copy=False)
