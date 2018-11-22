# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'

    area_ids = fields.Many2many(
        string='Areas', comodel_name='res.partner.area',
        relation='rel_mass_mailing_area', column1='mass_mailing_id',
        column2='area_id', copy=False)
