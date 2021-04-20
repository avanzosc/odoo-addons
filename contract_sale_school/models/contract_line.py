# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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
            if not contract.check_line_exists(product):
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
                if not contract.check_line_exists(product, date=date):
                    line_vals.update({
                        "name": "{} [{}]".format(product.name, month.name),
                        "date_start": date,
                        "date_end": date,
                        "recurring_next_date": date,
                    })
                    line_obj.create(line_vals)
        else:
            line_vals.update({
                "name": product.name,
                "date_start": date_start,
                "date_end": date_end,
                "recurring_next_date": date_end,
            })
            line_obj.create(line_vals)

    @api.multi
    def recompute_price(self):
        for line in self.filtered(
                lambda l: l.state not in ("closed", "canceled")):
            pricelist = (
                line.contract_id.pricelist_id or
                line.child_id.with_context(
                    force_company=line.contract_id.company_id.id
                ).property_product_pricelist)

            product = line.product_id.with_context(
                lang=line.contract_id.partner_id.lang,
                partner=line.contract_id.partner_id,
                quantity=line.quantity,
                date=line.recurring_next_date,
                pricelist=pricelist.id,
                uom=line.uom_id.id,
                fiscal_position=(line.contract_id.fiscal_position_id or
                                 self.env.context.get('fiscal_position'))
            )

            product_context = dict(self.env.context,
                                   partner_id=line.contract_id.partner_id.id,
                                   date=line.recurring_next_date,
                                   uom=line.uom_id.id)

            price, rule_id = pricelist.with_context(
                product_context).get_product_price_rule(
                line.product_id, line.quantity or 1.0,
                line.contract_id.partner_id)
            new_list_price, currency = product.with_context(
                product_context)._get_real_price_currency(
                rule_id, line.quantity, line.uom_id, pricelist.id,
                date=line.recurring_next_date,
                company_id=line.contract_id.company_id)

            if new_list_price != 0:
                if pricelist.currency_id != currency:
                    # we need new_list_price in the same currency as price
                    new_list_price = currency._convert(
                        new_list_price, pricelist.currency_id,
                        line.contract_id.company_id or
                        self.env.user.company_id,
                        line.recurring_next_date or fields.Date.today())
                discount = (new_list_price - price) / new_list_price * 100
                line.price_unit = new_list_price
                if (discount > 0 and new_list_price > 0) or (
                        discount < 0 and new_list_price < 0):
                    line.discount = discount
