# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    portal_custom_entry_show = fields.Many2many(
        comodel_name='ir.model.url', string="Show Entries")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    portal_custom_entry_show = fields.Many2many(
        comodel_name='ir.model.url', string='Show Entries',
        related='company_id.portal_custom_entry_show', readonly=False)
