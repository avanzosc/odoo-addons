# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ContractLineCreate(models.TransientModel):
    _name = "contract.line.create"
    _description = "Contract Line Creation Wizard"

    student_ids = fields.Many2many(comodel_name="res.partner")
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product",
        domain="[('recurrent_punctual','in',('recurrent','punctual'))]")
    date_start = fields.Date()
    date_end = fields.Date()
    unit_price = fields.Float()

    @api.model
    def default_get(self, fields):
        res = super(ContractLineCreate, self).default_get(fields)
        if self.env.context.get("active_model") == "res.partner":
            res.update({
                "student_ids": [(6, 0, self.env.context.get("active_ids"))],
            })
        return res

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.ensure_one()
        self.unit_price = self.product_id.lst_price

    @api.multi
    def button_create_contract_line(self):
        contract_line_obj = self.sudo().env["contract.line"]
        academic_year = self.env["education.academic_year"].search([
            ("date_start", "<=", self.date_start),
            ("date_end", ">=", self.date_end)
        ], limit=1)
        for student in self.student_ids.filtered(
                lambda s: s.educational_category == "student"):
            for payer in student.child2_ids.filtered("payer"):
                contract_line_obj.create_contract_line(
                    payer.responsible_id, payer.payment_percentage,
                    self.product_id, 1.0, self.unit_price, 0.0,
                    self.product_id.company_id, academic_year,
                    self.product_id.center_id, student.current_course_id,
                    student, date_start=self.date_start,
                    date_end=self.date_end)
            if self.product_id.education_type and (
                    self.product_id not in student.additional_product_ids):
                student.write({
                    "additional_product_ids": [(4, self.product_id.id)],
                })
