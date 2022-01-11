# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    campaign_id = fields.Many2one(
        string='Campaign', comodel_name='utm.campaign')
    medium_id = fields.Many2one(
        string='Medium', comodel_name='utm.medium')
    source_id = fields.Many2one(
        string='Source', comodel_name='utm.source')
