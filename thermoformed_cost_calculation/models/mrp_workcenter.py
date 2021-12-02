# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    frame_ids = fields.One2many(
        string='Frame',
        comodel_name='frame',
        inverse_name='workcenter_id')
