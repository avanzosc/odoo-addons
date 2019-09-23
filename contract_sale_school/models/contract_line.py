# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    recurrent_punctual = fields.Selection(
        string='Recurrent/Punctual', related='product_id.recurrent_punctual')
