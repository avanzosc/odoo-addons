# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResAreaSpecialization(models.Model):
    _name = 'res.area.specialization'
    _description = 'Areas specializations'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    opportunity_space_id = fields.Many2one(
        comodel_name='res.opportunity.space', required=True,
        string='Opportunity Space')
