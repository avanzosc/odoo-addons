# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        res = super(ProductProduct,
                    self)._convert_prepared_anglosaxon_line(line, partner)
        invoice = self.env["account.invoice"].browse(line.get("invoice_id"))
        res.update({
            "academic_year_id": line.get(
                "academic_year_id", invoice.academic_year_id.id),
            "school_id": line.get("school_id", invoice.school_id.id),
            "course_id": line.get("course_id", invoice.course_id.id),
            "child_id": line.get("child_id", invoice.child_id.id),
        })
        return res
