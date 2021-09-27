# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    parent_is_company = fields.Boolean(
        string='Parent is a Company', related='parent_id.is_company',
        store=True)
    headquarter = fields.Boolean(
        string='Headquarter', default=False)
