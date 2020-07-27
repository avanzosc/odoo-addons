# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.addons.sale_school.tests.common import TestSaleSchoolCommon


class ContractSaleSchoolCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(ContractSaleSchoolCommon, cls).setUpClass()
        cls.sale_order.write({
            "academic_year_id": cls.next_academic_year.id,
        })
        cls.progenitor.write({
            "customer_payment_mode_id": cls.payment_mode.id,
        })
        payer_line = cls.sale_order.order_line[:1].payer_ids[:1]
        payer_line.write({
            "pay_percentage": 100.0,
            "bank_id": payer_line.payer_id.bank_ids[:1].id,
        })
        cls.partner_model = cls.env["res.partner"]
        cls.relative = cls.progenitor.copy()
        cls.relative.write({
            "bank_ids": [(0, 0, {
                "acc_number": "ES1620856885270982816412",
            })],
        })
        family_vals = {
            "child2_id": cls.student.id,
            "responsible_id": cls.relative.id,
            "family_id": cls.family.id,
            "payer": True,
            "payment_percentage": 100.0,
            "bank_id": cls.relative.bank_ids[:1].id,
        }
        cls.family_obj.create(family_vals)
        cls.recurrent_product = cls.service.copy()
        cls.recurrent_product.write({
            "recurrent_punctual": "recurrent",
            "month_start": cls.env.ref("base_month.base_month_november").id,
            "end_month": cls.env.ref("base_month.base_month_january").id,
        })
        cls.product_punctual = cls.service.copy()
        cls.product_punctual.write({
            "recurrent_punctual": "punctual",
            "punctual_month_ids":
                [(6, 0, [cls.env.ref("base_month.base_month_may").id,
                         cls.env.ref("base_month.base_month_december").id])],
        })
