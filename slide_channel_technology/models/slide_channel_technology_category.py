# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannelTechnologyCategory(models.Model):
    _name = 'slide.channel.technology.category'
    _description = "Technology categories"

    name = fields.Char(string='Description')
