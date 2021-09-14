# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    child_medical_record = fields.Integer(
        string='Child Medical Record Number')
    adult_medical_record = fields.Integer(
        string='Adult Medical Record Number')
    last_child_number = fields.Integer(
        string='Last Child Medical Record Number',
        compute='_compute_last_child_number',
        store=False)
    last_adult_number = fields.Integer(
        string='Last Adult Medical Record Number',
        compute='_compute_last_adult_number',
        store=False)

    @api.depends('child_medical_record')
    def _compute_last_child_number(self):
        contacts = self.env['res.partner'].search(
            [('child_medical_record', '!=', 0)])
        if contacts:
            self.last_child_number = max(
                contacts, key=lambda x: (
                    x.child_medical_record)).child_medical_record
        else:
            self.last_child_number = 0

    @api.depends('adult_medical_record')
    def _compute_last_adult_number(self):
        contacts = self.env['res.partner'].search(
            [('adult_medical_record', '!=', 0)])
        if contacts:
            self.last_adult_number = max(
                contacts, key=lambda x: (
                    x.adult_medical_record)).adult_medical_record
        else:
            self.last_adult_number = 0
