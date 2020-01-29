# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def find_or_create_payer_contract(self, payer):
        contract_obj = self.sudo().env["contract.contract"]
        contract = contract_obj.search([
            ("company_id", "=", self.originator_id.id),
            ("sale_id", "=", self.order_id.id),
            ("partner_id", "=", payer.id),
            "|", ("date_end", ">=", fields.Date.context_today(self)),
            ("date_end", "=", False),
        ])
        if not contract:
            journal = self.env["account.journal"].search([
                ("type", "=", "sale"),
                ("company_id", "=", self.originator_id.id),
            ], limit=1)
            name = "[{}] {}".format(self.order_id.name, payer.display_name)
            contract = contract_obj.create({
                "name": name,
                "contract_type": "sale",
                "company_id": self.originator_id.id,
                "partner_id": payer.id,
                "sale_id": self.order_id.id,
                "pricelist_id": self.order_id.pricelist_id.id,
                "child_id": self.order_id.child_id.id,
                "academic_year_id": self.order_id.academic_year_id.id,
                "school_id": self.order_id.school_id.id,
                "course_id": self.order_id.course_id.id,
                "journal_id": journal.id,
            })
        return contract and contract[:1]

    def create_contract_line(self):
        self.ensure_one()
        line_obj = self.sudo().env["contract.line"]
        for payer in self.payer_ids:
            contract = self.find_or_create_payer_contract(payer.payer_id)
            line_vals = {
                "contract_id": contract.id,
                "product_id": self.product_id.id,
                "payment_percentage": payer.pay_percentage,
                "price_unit": self.price_unit,
                "quantity": self.product_uom_qty,
                "uom_id": self.product_id.uom_id.id,
                "discount": self.discount,
            }
            date_start = self.order_id.academic_year_id.date_start
            date_end = self.order_id.academic_year_id.date_end
            if self.product_id.recurrent_punctual == "recurrent":
                if date_start.month != self.product_id.month_start.number:
                    date_start = date_start.replace(
                        month=self.product_id.month_start.number, day=1)
                if date_end != self.product_id.end_month.number:
                    date_end = date_end.replace(
                        month=self.product_id.end_month, day=1)
                line_vals.update({
                    "name": self.product_id.name,
                    "date_start": date_start,
                    "date_end": date_end,
                    "recurring_next_date": date_start,
                })
                line_obj.create(line_vals)
            elif self.product_id.recurrent_punctual == "punctual":
                for month in self.product_id.punctual_month_ids:
                    date_end = date_end.replace(day=1)
                    if date_start.month <= month.number:
                        date = date_start.replace(month=month.number)
                    else:
                        date = date_end.replace(month=month.number)
                    line_vals.update({
                        "name": "{} [{}]".format(
                            self.product_id.name, month.name),
                        "date_start": date,
                        "date_end": date,
                        "recurring_next_date": date,
                    })
                    line_obj.create(line_vals)
