# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity = fields.Selection(
        [('fattening', 'Fattening'),
         ('incubation', 'Incubation'),
         ('reproduction', 'Reproduction')], string="Activity", copy=False)
    farm_type = fields.Selection(
        [('integrated', 'Integrated'),
         ('own', 'Own')], string="Farm Type", copy=False)
