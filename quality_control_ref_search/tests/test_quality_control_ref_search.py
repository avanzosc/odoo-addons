# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as common


class TestQualityControlRefSearch(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.inspection_model = self.env["qc.inspection"]

    def test_quality_control_ref_search(self):
        inspection_vals = {
            "object_id": ("res.partner," + str(self.ref("base.res_partner_2")))
        }
        self.inspection = self.inspection_model.create(inspection_vals)
        self.assertNotEqual(
            self.inspection.ref_model_name, False, "Inspections without reference model"
        )
        self.assertNotEqual(
            self.inspection.ref_name, False, "Inspections without reference name"
        )
