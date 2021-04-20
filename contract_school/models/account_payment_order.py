# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.models import expression


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        context = self.env.context
        if "search_center_id" in context:
            args = expression.AND(
                [args, [("company_partner_bank_id.partner_id", "=",
                         context.get("search_center_id"))]])
        result = super(AccountPaymentOrder, self)._search(
            args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)
        return result

    @api.multi
    def _prepare_move_line_partner_account(self, bank_line):
        vals = super(AccountPaymentOrder,
                     self)._prepare_move_line_partner_account(bank_line)
        vals.update({
            "academic_year_id": bank_line.academic_year_id.id,
            "school_id": bank_line.center_id.id,
            "course_id": bank_line.course_id.id,
            "child_id": bank_line.student_id.id,
        })
        return vals
