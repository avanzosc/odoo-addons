# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    payment_percentage = fields.Float(string='Percentage', default=100.0)
    user_id = fields.Many2one(
        comodel_name='res.users', string='User')
    observations = fields.Text(string='Observations')
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner",
        related="contract_id.partner_id", store=True)
    child_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        related="contract_id.child_id", store=True)
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course",
        related="contract_id.course_id", store=True)
    school_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        related="contract_id.school_id", store=True)
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year",
        related="contract_id.academic_year_id", store=True)
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist", string="Pricelist",
        related="contract_id.pricelist_id", store=True)

    @api.multi
    @api.depends('quantity', 'price_unit', 'discount', 'payment_percentage')
    def _compute_price_subtotal(self):
        super(ContractLine, self)._compute_price_subtotal()
        for line in self.filtered(lambda x: x.payment_percentage != 100.0):
            line.price_subtotal = (
                line.price_subtotal * line.payment_percentage) / 100

    @api.model
    def _prepare_invoice_line(self, invoice_id=False, invoice_values=False):
        self.ensure_one()
        res = super(ContractLine, self)._prepare_invoice_line(
            invoice_id=invoice_id, invoice_values=invoice_values)
        res['payment_percentage'] = self.payment_percentage
        return res
