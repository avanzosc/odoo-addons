# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lang_skill_ids = fields.One2many(
        comodel_name='res.partner.lang.skill', string='Language Skills',
        inverse_name='partner_id')
