# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    living_situation = fields.Selection(
        [('separate', 'Separate'), ('coexistence', 'Coexistence')],
        string='Living situation')
    can_contact_with = fields.Boolean(
        string='Can not contact with', default=False)
    academic_record = fields.Boolean(
        string='Academic record', default=False)
    scholarship_request = fields.Boolean(
        string='Scholarship request', default=False)
    expectation_id = fields.Many2one(
        string='Expectation', comodel_name='res.partner.expectation')
    interested_in_dual = fields.Boolean(
        string='Interested in dual', default=False)
    employment_situation_id = fields.Many2one(
        string='Employment situation',
        comodel_name='res.partner.employment.situation')
    lanbide_registration = fields.Boolean(
        string='Lanbide registration', default=False)
