# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
