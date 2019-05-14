# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestProductTemplate(TransactionCase):

    def setUp(self):
        super(TestProductTemplate, self).setUp()
        self.template_model = self.env['product.template']
        self.template = self.env['product.template'].search([], limit=1)

    def test_product_template(self):
        self.template.write({'list_price': 5,
                             'recurrent_punctual': 'recurrent'})
        self.assertEquals(self.template.total_annual, 50.0)
        vals = [(6, 0, [self.browse_ref('base_month.base_month_january').id,
                        self.browse_ref('base_month.base_month_march').id,
                        self.browse_ref('base_month.base_month_april').id])]
        self.template.write({'list_price': 5,
                             'recurrent_punctual': 'punctual',
                             'punctual_month_ids': vals})
        self.template._compute_total_anual()
        self.assertEquals(self.template.total_annual, 15.0)
