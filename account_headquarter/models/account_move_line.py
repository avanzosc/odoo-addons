# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    headquarter_id = fields.Many2one(
        string="Headquarter",
        comodel_name="res.partner",
        domain="[('headquarter','=', True)]",
    )

    @api.model_create_multi
    def create(self, values):
        if isinstance(values, dict):
            values = self.treatment_headquarter(values)
        else:
            for val in values:
                val = self.treatment_headquarter(val)
        return super().create(values)

    def write(self, values):
        result = super().write(values)
        if "headquarter_id" in values:
            for line in self:
                line.update_analytic_lines_hearquarter()
        return result

    def treatment_headquarter(self, values):
        if values.get("exclude_from_invoice_tab", False):
            values["headquarter_id"] = False
            if (
                not values.get("exclude_from_invoice_tab", False)
                and not values.get("headquarter_id", False)
                and values.get("move_id", False)
            ):
                move = self.env["account.move"].browse(values.get("move_id"))
                if move.headquarter_id:
                    values["headquarter_id"] = move.headquarter_id.id
        return values

    def update_analytic_lines_hearquarter(self):
        for line in self:
            if line.analytic_line_ids:
                vals = {
                    "headquarter_id": (
                        line.headquarter_id.id if line.headquarter_id else False
                    )
                }
                line.analytic_line_ids.write(vals)

    @api.onchange("product_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        for line in self:
            if (
                "default_headquarter_id" in self.env.context
                and self.env.context.get("default_headquarter_id", False)
                and line.account_id
                and line.product_id
            ):
                account_group = line.account_id.group_id
                without_headquarter = account_group._find_account_group_headquarter()
                if without_headquarter:
                    line.headquarter_id = False
        return result
