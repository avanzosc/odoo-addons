# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ExportProductXlsxReport(models.TransientModel):
    _name = "report.stock.product_xlsx.export"
    _description = "Wizard to export products in xlsx"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company.id,
        required=True,
    )
    family_id = fields.Many2one(
        comodel_name="product.category",
        string="Family",
    )
    sub_family_id = fields.Many2one(
        comodel_name="product.category",
        string="Subfamily",
    )
    internal_category_id = fields.Many2one(
        comodel_name="product.public.category",
        string="Internal Category",
    )
    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    @api.onchange("family_id")
    def _onchange_family_id(self):
        if self.sub_family_id and self.sub_family_id.parent_id != self.family_id:
            self.sub_family_id = False

    def export_xls(self):
        self.ensure_one()
        if self.company_id not in self.env.companies:
            raise UserError(_("You can only export data from an allowed company."))
        product_domain = [("company_id", "in", [False, self.company_id.id])]
        if self.family_id:
            product_domain.append(("family_id", "=", self.family_id.id))
        if self.sub_family_id:
            product_domain.append(("sub_family_id", "=", self.sub_family_id.id))
        if self.internal_category_id:
            product_domain.append(
                ("internal_category_id", "=", self.internal_category_id.id)
            )
        if self.product_brand_id:
            product_domain.append(("product_brand_id", "=", self.product_brand_id.id))
        products = self.env["product.product"].search(product_domain)

        report_action = (
            self.env.ref(
                "product_variant_stock_report_xlsx.product_product_record_xlsx"
            )
            .with_company(self.company_id.id)
            .report_action(
                products,
                data={"force_company_id": self.company_id.id},
            )
        )
        return report_action
