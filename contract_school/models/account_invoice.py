# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    child_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")])
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course")
    school_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")])
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year")

    def _get_refund_common_fields(self):
        common_fields = [
            "child_id", "course_id", "school_id", "academic_year_id"]
        return (super(AccountInvoice, self)._get_refund_common_fields() +
                common_fields)

    def _prepare_tax_line_vals(self, line, tax):
        vals = super(AccountInvoice, self)._prepare_tax_line_vals(line, tax)
        if line.payment_percentage:
            percentage = line.payment_percentage / 100
            vals.update({
                'base': vals['base'] * percentage,
                'amount': vals['amount'] * percentage,
            })
        return vals

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for line in res:
            line.update({
                "academic_year_id": self.academic_year_id.id,
                "school_id": self.school_id.id,
                "course_id": self.course_id.id,
                "child_id": self.child_id.id,
            })
        return res

    @api.model
    def tax_line_move_line_get(self):
        res = super(AccountInvoice, self).tax_line_move_line_get()
        for line in res:
            line.update({
                "academic_year_id": self.academic_year_id.id,
                "school_id": self.school_id.id,
                "course_id": self.course_id.id,
                "child_id": self.child_id.id,
            })
        return res

    @api.multi
    def _prepare_new_payment_order(self, payment_mode=None):
        self.ensure_one()
        vals = super(AccountInvoice, self)._prepare_new_payment_order(
            payment_mode=payment_mode)
        if payment_mode.bank_account_link == "variable" and self.school_id:
            journal = payment_mode.variable_journal_ids.filtered(
                lambda j: j.bank_account_id.partner_id == self.school_id)
            if len(journal) == 1:
                vals.update({
                    "journal_id": journal.id,
                })
        return vals

    @api.multi
    def create_account_payment_line(self):
        payorder_ids = []
        payment_types = self.mapped("payment_mode_id.payment_type")
        action_payment_type = (
            payment_types[0] if payment_types else "inbound")
        action = self.env['ir.actions.act_window'].for_xml_id(
            "account_payment_order",
            "account_payment_order_%s_action" % action_payment_type)
        for invoice in self:
            action = super(
                AccountInvoice, invoice.with_context(
                    search_center_id=invoice.school_id.id)
            ).create_account_payment_line()
            if action.get("res_id"):
                payorder_ids += [action.get("res_id")]
            else:
                domain = safe_eval(action.get("domain") or "[]")
                payorder_ids += domain[0][2]
        action.update({
            "view_mode": "tree,form,pivot,graph",
            "domain": "[('id', 'in', %s)]" % payorder_ids,
            "views": False,
        })
        return action
