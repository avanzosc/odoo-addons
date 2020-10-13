# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Student',
        domain=[('educational_category', '=', 'student')])
    course_id = fields.Many2one(
        comodel_name='education.course', string='Education Course')
    school_id = fields.Many2one(
        comodel_name='res.partner', string='Education Center',
        domain=[('educational_category', '=', 'school')])
    academic_year_id = fields.Many2one(
        comodel_name='education.academic_year', string='Academic year')

    @api.multi
    def _prepare_invoice(self, date_invoice, journal=None):
        self.ensure_one()
        invoice_vals = super(ContractContract, self)._prepare_invoice(
            date_invoice, journal=journal)
        invoice_vals.update({
            "child_id": self.child_id.id,
            "course_id": self.course_id.id,
            "school_id": self.school_id.id,
            "academic_year_id": self.academic_year_id.id,
        })
        return invoice_vals
