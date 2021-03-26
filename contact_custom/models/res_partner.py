# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    school_id = fields.Many2one(
        string='School', comodel_name='res.partner')
    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type')
