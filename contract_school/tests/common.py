# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contacts_school_education.tests.common import \
    TestContactsSchoolEducationCommon


class ContractSchoolCommon(TestContactsSchoolEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(ContractSchoolCommon, cls).setUpClass()
        cls.product_model = cls.env["product.product"]
        cls.contract_model = cls.env["contract.contract"]
        cls.line_model = cls.env["contract.line"]
        cls.partner_model = cls.env["res.partner"]
        cls.invoice_model = cls.env["account.invoice"]
        cls.tax_model = cls.env["account.tax"]
        cls.payorder_model = cls.env["account.payment.order"]
        cls.payorder_wizard = cls.env["account.payment.line.create"]
        start = cls.academic_year.date_start
        end = cls.academic_year.date_end
        cls.pricelist = cls.env["product.pricelist"].create({
            "name": "50% Discount Pricelist",
            "item_ids": [(0, 0, {
                "compute_price": "percentage",
                "percent_price": 50.0,
            })],
        })
        cls.tax_10 = cls.tax_model.create({
            "name": "10% Tax",
            "amount_type": "percent",
            "amount": 10,
        })
        cls.tax_20 = cls.tax_model.create({
            "name": "20% Tax",
            "amount_type": "percent",
            "amount": 20,
        })
        cls.relative = cls.partner_model.create({
            "name": "Test Relative",
            "educational_category": "otherrelative",
            "is_company": False,
            "email": "relative@email.test",
            "parent_id": cls.family.id,
            "bank_ids": [
                (0, 0, {
                    "acc_number": "0123456789",
                }),
                (0, 0, {
                    "acc_number": "9876543210",
                })]
        })
        cls.product1 = cls.product_model.create({
            "name": "Test Service 10%",
            "list_price": 10.0,
            "taxes_id": [(6, 0, cls.tax_10.ids)],
        })
        cls.product2 = cls.product_model.create({
            "name": "Test Product 20%",
            "list_price": 100.0,
            "taxes_id": [(6, 0, cls.tax_20.ids)],
        })
        cls.inbound_mode = cls.env.ref(
            "account_payment_mode.payment_mode_inbound_dd1"
        )
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "bank"),
             "|", ("company_id", "=", cls.env.user.company_id.id),
             ("company_id", "=", False)], limit=1
        )
        cls.bank = cls.env["res.partner.bank"].create({
            "acc_number": "0918273645",
            "partner_id": cls.journal.company_id.partner_id.id,
        })
        cls.journal.write({
            "bank_account_id": cls.bank.id,
        })
        cls.bank.write({
            "partner_id": cls.edu_partner.id,
        })  # in order to avoid some error raises
        cls.inbound_mode.variable_journal_ids = cls.journal
        contract_vals = {
            "name": "Contract for test contract_school",
            "partner_id": cls.relative.id,
            "pricelist_id": cls.pricelist.id,
            "contract_type": "sale",
            "child_id": cls.student.id,
            "academic_year_id": cls.academic_year.id,
            "school_id": cls.edu_partner.id,
            "course_id": cls.edu_course.id,
            "payment_mode_id": cls.inbound_mode.id,
        }
        cls.contract = cls.contract_model.create(contract_vals)
        line_vals = {
            "contract_id": cls.contract.id,
            "product_id": cls.product1.id,
            "name": cls.product1.name,
            "uom_id": cls.product1.uom_id.id,
            "recurring_next_date": cls.today,
            "date_start": start,
            "date_end": end,
        }
        cls.line = cls.line_model.create(line_vals)
        cls.line._onchange_product_id()
        cls.line.write({
            "price_unit": 800,
            "payment_percentage": 50.0,
        })
        cls.line2 = cls.line.copy()
        cls.line2._onchange_product_id()
        cls.line2.write({
            "product_id": cls.product2.id,
            "name": cls.product2.name,
            "price_unit": 200,
            "payment_percentage": 100.0,
            "recurring_next_date": start,
            "date_end": start,
        })
        cls.line3 = cls.line.copy()
        cls.line3._onchange_product_id()
        cls.line3.write({
            "price_unit": 300,
            "payment_percentage": 100.0,
            "recurring_next_date": end,
        })
