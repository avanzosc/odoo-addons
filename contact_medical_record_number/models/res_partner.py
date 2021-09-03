# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_medical_record = fields.Integer(
        string='Partner Medical Record Number')
    parent_medical_record = fields.Integer(
        string='Parent Medical Record Number')
    last_partner_number = fields.Integer(
        string='Last partner medical record number',
        compute='_compute_last_partner_number',
        store=False)
    last_parent_number = fields.Integer(
        string='Last parent medical record number',
        compute='_compute_last_parent_number',
        store=False)

    @api.depends('partner_medical_record', 'parent_id')
    def _compute_last_partner_number(self):
        if self.parent_id:
            self.parent_medical_record = self.parent_id.parent_medical_record
        contacts = self.env['res.partner'].search(
            [('partner_medical_record', '!=', 0)])
        if contacts:
            self.last_partner_number = max(
                contacts, key=lambda x: (
                    x.partner_medical_record)).partner_medical_record
        else:
            self.last_partner_number = 0

    @api.depends('parent_medical_record')
    def _compute_last_parent_number(self):
        contacts = self.env['res.partner'].search(
            [('parent_medical_record', '!=', 0)])
        if contacts:
            self.last_parent_number = max(
                contacts, key=lambda x: (
                    x.parent_medical_record)).parent_medical_record
        else:
            self.last_parent_number = 0
