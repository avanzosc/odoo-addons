# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class MedicalRecordNumber(models.Model):
    _name = 'medical.record.number'
    _description = 'Medical Record Number'
    _order = 'number desc'

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner')
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='res.partner')
    number = fields.Integer(string='Medical Record Number')
