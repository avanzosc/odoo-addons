# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lang_ids = fields.Many2many(
        string='Languages', comodel_name='hr.skill',
        relation='rel_partner_language', column1='partner_id',
        column2='lang_id')
