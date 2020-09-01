# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    recurrent_punctual = fields.Selection(
        string='Recurrent/Punctual', related='product_id.recurrent_punctual')

    def create_contract_line(
            self, payer_partner, pay_percentage, product, quantity, price_unit,
            discount, originator, academic_year, center, course, student,
            sale_order=False, date_start=False, date_end=False, bank=False):
        contract_obj = self.sudo().env["contract.contract"]
        line_obj = self.sudo().env["contract.line"]
        contract = contract_obj.find_or_create_payer_contract(
            payer_partner, originator, academic_year, center, course,
            student, sale_order=sale_order, bank=bank)
        line_vals = {
            "contract_id": contract.id,
            "product_id": product.id,
            "payment_percentage": pay_percentage,
            "price_unit": price_unit,
            "quantity": quantity,
            "uom_id": product.uom_id.id,
            "discount": discount,
        }
        date_start = date_start or academic_year.date_start
        date_end = date_end or academic_year.date_end
        if product.recurrent_punctual == "recurrent":
            if date_start.month != product.month_start.number:
                date_start = date_start.replace(
                    month=product.month_start.number, day=1)
            if date_end != product.end_month.number:
                date_end = date_end.replace(
                    month=product.end_month, day=1)
            line_vals.update({
                "name": product.name,
                "date_start": date_start,
                "date_end": date_end,
                "recurring_next_date": date_start,
            })
            line_obj.create(line_vals)
        elif product.recurrent_punctual == "punctual":
            for month in product.punctual_month_ids:
                date_end = date_end.replace(day=1)
                if date_start.month <= month.number:
                    date = date_start.replace(month=month.number)
                else:
                    date = date_end.replace(month=month.number)
                line_vals.update({
                    "name": "{} [{}]".format(product.name, month.name),
                    "date_start": date,
                    "date_end": date,
                    "recurring_next_date": date,
                })
                line_obj.create(line_vals)
