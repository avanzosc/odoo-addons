# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    partner_shipping_id = fields.Many2one(
        string='Patient', comodel_name='res.partner',
        related='sale_order_id.partner_shipping_id', store=True)
