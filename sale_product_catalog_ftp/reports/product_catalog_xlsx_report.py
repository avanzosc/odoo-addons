# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class ProductCatalogXlsx(models.AbstractModel):
    _name = "report.sale_product_catalog_ftp.product_catalog_xlsx_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Export a product catalog with B2B stock as xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        data = data or {}
        partner_id = data.get("partner_id")
        partner = self.env["res.partner"].browse(partner_id) if partner_id else None

        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table_header.set_text_wrap()

        headers = [
            _("Product"),
            _("EAN code"),
            _("Product reference"),
            _("Brand"),
            _("Product category"),
            _("Delivery date start"),
            _("Delivery date end"),
            _("Price"),
            _("RRP"),
            _("B2B stock"),
        ]

        for catalog in objects:
            worksheet = workbook.add_worksheet(catalog.display_name[:31])
            templates = (
                self.env["product.template"]
                .browse(catalog._get_product_tmpl_ids())
                .filtered("is_published")
            )
            all_attributes = templates.mapped("attribute_line_ids.attribute_id")

            for col, label in enumerate(headers):
                worksheet.write(0, col, label, table_header)
            attr_col_start = len(headers)
            for i, attribute in enumerate(all_attributes):
                worksheet.write(
                    0, attr_col_start + i, attribute.display_name, table_header
                )

            row = 1
            for template in templates:
                variant = template.product_variant_id
                if not variant:
                    continue
                pricelist_item = self._get_pricelist_item(variant, catalog, partner)
                worksheet.write(row, 0, variant.display_name)
                worksheet.write(row, 1, variant.barcode or "")
                worksheet.write(row, 2, variant.default_code or "")
                worksheet.write(row, 3, template.product_brand_id.name or "")
                worksheet.write(row, 4, template.categ_id.display_name or "")
                worksheet.write(
                    row,
                    5,
                    pricelist_item
                    and pricelist_item.date_start
                    and pricelist_item.date_start.date().isoformat()
                    or "",
                )
                worksheet.write(
                    row,
                    6,
                    pricelist_item
                    and pricelist_item.date_end
                    and pricelist_item.date_end.date().isoformat()
                    or "",
                )
                worksheet.write(
                    row,
                    7,
                    pricelist_item.fixed_price if pricelist_item else variant.lst_price,
                )
                worksheet.write(
                    row,
                    8,
                    pricelist_item.pvp_price
                    if pricelist_item
                    else self._get_list_price_tax(template),
                )
                worksheet.write(
                    row,
                    9,
                    variant.with_context(
                        force_company=catalog.company_id.id
                    ).b2b_virtual_available,
                )
                for i, attribute in enumerate(all_attributes):
                    ptav = variant.product_template_attribute_value_ids.filtered(
                        lambda v, attribute=attribute: v.attribute_id == attribute
                    )
                    worksheet.write(row, attr_col_start + i, ptav[:1].name or "")
                row += 1

    def _get_pricelist_item(self, product, catalog, partner):
        if not partner:
            return self.env["product.pricelist.item"]
        pricelist = partner.property_product_pricelist
        base_pricelists = pricelist.item_ids.mapped("base_pricelist_id")
        if base_pricelists:
            pricelist = base_pricelists[:1]
        rule_id = pricelist._get_product_rule(product, 1.0)
        return self.env["product.pricelist.item"].browse(rule_id)

    def _get_list_price_tax(self, template):
        if not template.taxes_id:
            return template.list_price
        tax_res = template.taxes_id.compute_all(
            template.list_price,
            currency=template.currency_id,
            quantity=1.0,
            product=template,
        )
        return tax_res["total_included"]
