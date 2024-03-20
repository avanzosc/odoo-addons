# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        string="Building use", comodel_name="building.use", copy=False,
    )
    building_section_ids = fields.One2many(
        string="Building Section/Area", comodel_name="building.section",
        inverse_name="partner_id", copy=False,
    )
    service_start_date = fields.Date(
        string="Service Start Date", copy=False,
    )
    
    maintainer_id = fields.Many2one('res.users', string='Maintainer')
    installer_id = fields.Many2one('res.users', string='Installer')
    administrator_id = fields.Many2one('res.users', string='Administrator')
    