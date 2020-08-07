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
        comodel_name="res.partner", string="Child",
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
