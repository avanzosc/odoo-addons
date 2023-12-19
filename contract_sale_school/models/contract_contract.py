# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.models import expression
from odoo.exceptions import UserError


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')

    def find_or_create_payer_contract(
            self, payer_partner, originator, academic_year, center, course,
            student, sale_order=False, bank=False):
        contract_obj = self.sudo().env["contract.contract"]
        contract_domain = [
            ("company_id", "=", originator.id),
            ("partner_id", "=", payer_partner.id),
            ("academic_year_id", "=", academic_year.id),
            ("school_id", "=", center.id),
            ("course_id", "=", course.id),
            ("child_id", "=", student.id),
        ]
        payment_mode = payer_partner.sudo().with_context(
            force_company=originator.id
        ).customer_payment_mode_id
        mandate = False
        if payment_mode.payment_method_id.mandate_required:
            if not bank:
                bank = (
                    payer_partner.bank_ids.filtered("use_default") or
                    payer_partner.bank_ids[:1])
                if len(bank) > 1:
                    raise UserError(
                        _("There is more than one bank account defined as "
                          "default for partner {}").format(
                            payer_partner.display_name))
            mandate = bank and bank.sudo()._find_mandate(originator)
        if mandate:
            contract_domain = expression.AND([
                [("mandate_id", "=", mandate.id)], contract_domain])
        if sale_order:
            contract_domain = expression.AND([
                [("sale_id", "=", sale_order.id)], contract_domain])
        contract = contract_obj.search(contract_domain)
        if not contract:
            journal = self.env["account.journal"].search([
                ("type", "=", "sale"),
                ("company_id", "=", originator.id),
            ], limit=1)
            name = "{} ({})".format(
                payer_partner.display_name, academic_year.display_name)
            if sale_order:
                name = "[{}] {}".format(sale_order.name, name)
            pricelist = sale_order and sale_order.pricelist_id.filtered(
                lambda p: p.company_id == originator or not p.company_id)
            if not pricelist:
                pricelist = student.with_context(
                    force_company=originator.id
                ).property_product_pricelist
            contract = contract_obj.create({
                "name": name,
                "contract_type": "sale",
                "company_id": originator.id,
                "partner_id": payer_partner.id,
                "mandate_id": mandate and mandate.id,
                "payment_mode_id": payment_mode.id,
                "sale_id": sale_order and sale_order.id,
                "child_id": student.id,
                "academic_year_id": academic_year.id,
                "school_id": center.id,
                "course_id": course.id,
                "journal_id": journal.id,
                "pricelist_id": pricelist and pricelist.id,
            })
        return contract and contract[:1]

    @api.multi
    def check_line_exists(self, product, date=False):
        self.ensure_one()
        exists = self.contract_line_ids.filtered(
            lambda l: l.product_id == product and
            l.state in ("upcoming", "in-progress"))
        if exists and date:
            exists = exists.filtered(lambda l: l.date_start == date)
        return bool(exists)
