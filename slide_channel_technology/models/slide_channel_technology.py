# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannelTechnology(models.Model):
    _name = 'slide.channel.technology'
    _description = "Technologies"

    name = fields.Char(string='Name')
    category_id = fields.Many2one(
        string='Category', comodel_name='slide.channel.technology.category')
    description = fields.Text(string='Description')
