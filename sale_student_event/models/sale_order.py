# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner')
    student_school_id = fields.Many2one(
        string='Student school', related='student_id.education_center_id',
        comodel_name='res.partner', store=True)
    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')

    @api.onchange("student_id")
    def _onchange_student_id(self):
        for sale in self.filtered(lambda x: x.student_id):
            sale.partner_id = sale.student_id.commercial_partner_id
