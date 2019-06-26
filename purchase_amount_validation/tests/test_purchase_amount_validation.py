# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.product.tests import common


class TestAmountValidation(common.TestProductCommon):

    def setUp(self):
        super(TestAmountValidation, self).setUp()
        self.partner_id = self.env.ref('base.res_partner_1')
        self.product_id_1 = self.env.ref('product.product_product_8')
        self.product_id_2 = self.env.ref('product.product_product_11')
        res_users_purchase_user = self.env.ref('purchase.group_purchase_user')
        Users = self.env['res.users'].with_context({
            'no_reset_password': True, 'mail_create_nosubscribe': True})
        self.user_purchase_user = Users.create({
            'name': 'Pauline Poivraisselle',
            'login': 'pauline',
            'email': 'pur@example.com',
            'notification_type': 'inbox',
            'groups_id': [(6, 0, [res_users_purchase_user.id])]})
        self.po_vals = {
            'partner_id': self.partner_id.id,
            'order_line': [
                (0, 0, {
                    'name': self.product_id_1.name,
                    'product_id': self.product_id_1.id,
                    'product_qty': 5.0,
                    'product_uom': self.product_id_1.uom_po_id.id,
                    'price_unit': 500.0,
                    'date_planned': datetime.today().strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT),
                })],
        }

    def test_check_double_validation(self):
        # make double validation two step
        self.env.user.company_id.write({
            'po_double_validation': 'two_step',
            'po_double_validation_amount': 1000.00,
            'po_double_validation_amount2': 2000.00,
        })
        # Draft purchase order created
        self.po = self.env['purchase.order'].sudo(
            self.user_purchase_user).create(self.po_vals)
        self.assertTrue(self.po, 'Purchase: no purchase order created')
        # Purchase order confirm
        self.po.button_confirm()
        self.assertEqual(
            self.po.state, 'to approve',
            'Purchase: PO state should be "to approve".')
        # PO approved by manager
        self.po.button_approve()
        self.assertEqual(
            self.po.state, 'for management approval',
            'PO state should be "For Management Approval".')
        head_group = self.env.ref(
            'purchase_amount_validation.group_purchase_head')
        self.user_purchase_user.write({
            'groups_id': [(6, 0, [head_group.id])]
        })
        self.po.button_approve()
        self.assertEqual(
            self.po.state, 'purchase',
            'PO state should be "Purchase".')
        self.po.button_cancel()
        self.assertEqual(
            self.po.state, 'cancel',
            'PO state should be "Cancelled".')
        self.po.button_approve()  # Do nothing
        self.assertEqual(
            self.po.state, 'cancel',
            'PO state should be "Cancelled".')
