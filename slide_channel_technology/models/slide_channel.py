# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    technology_id = fields.Many2one(
        string='Technology', comodel_name='slide.channel.technology')
    technology_category_id = fields.Many2one(
        string='Technology category', store=True,
        comodel_name='slide.channel.technology.category',
        related='technology_id.category_id')
    technology_description = fields.Text(
        string='Technology description', store=True,
        related='technology_id.description')
