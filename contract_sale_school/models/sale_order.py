# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _compute_contracts_count(self):
        for sale in self:
            sale.contracts_count = len(sale.contract_ids)

    contract_ids = fields.One2many(
        comodel_name="contract.contract",
        inverse_name="sale_id", string="Recurring contracts")
    contracts_count = fields.Integer(
        string="Contracts", compute="_compute_contracts_count")

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            recurrent_lines = sale.order_line.filtered(
                lambda l: l.product_id.recurrent_punctual)
            if recurrent_lines and not sale.academic_year_id:
                raise ValidationError(_("You must select an academic year."))
            if any(recurrent_lines.filtered(
                    lambda l: not l.originator_id or not l.payer_ids)):
                raise ValidationError(
                    _("Please check out originator and payer for "
                      "recurrent/punctual products."))
            for line in recurrent_lines:
                line.create_contract_line()
        return res

    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for sale in self:
            contract_lines = sale.mapped("contract_ids.contract_line_ids")
            active_contract_lines = contract_lines.filtered(
                lambda l: not l.is_canceled)
            active_contract_lines.filtered(
                lambda l: l.is_cancel_allowed).cancel()
            for active_line in active_contract_lines.filtered(
                    lambda l: not l.is_cancel_allowed and l.is_stop_allowed):
                today = fields.Date.context_today(self)
                end_date = (
                    active_line.last_date_invoiced
                    if (active_line.last_date_invoiced and
                        active_line.last_date_invoiced > today) else today)
                active_line.stop(end_date)
            contract_lines.filtered(
                lambda l: l.is_canceled and not l.last_date_invoiced).unlink()
            contracts = sale.contract_ids.filtered(
                lambda c: not c.contract_line_ids)
            contracts.unlink()
        return res

    @api.multi
    def action_view_contracts(self):
        self.ensure_one()
        action = self.env.ref("contract.action_customer_contract")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("sale_id", "in", self.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
