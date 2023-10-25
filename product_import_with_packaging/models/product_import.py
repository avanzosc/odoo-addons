# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons.base_import_wizard.models.base_import import convert2str


class ProductImport(models.Model):
    _inherit = "product.import"

    packaging_import_id = fields.Many2one(
        string="Packaging Import",
        comodel_name="product.packaging.import",
        readonly=True,
    )
    show_packaging_import = fields.Boolean(
        compute="_compute_show_packaging_import",
        store=True,
    )

    @api.depends(
        "packaging_import_id", "import_line_ids", "import_line_ids.packaging_name"
    )
    def _compute_show_packaging_import(self):
        for record in self:
            record.show_packaging_import = bool(record.packaging_import_id) or any(
                record.mapped("import_line_ids.packaging_name")
            )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            packaging_name = row_values.get("Packaging Name", "")
            packaging_barcode = row_values.get("Packaging Barcode", "")
            packaging_quantity = row_values.get("Packaging Quantity", "")
            max_weight = row_values.get("Max Weight", "")
            weight = row_values.get("Weight", "")
            length = row_values.get("Length", "")
            width = row_values.get("Width", "")
            height = row_values.get("Height", "")
            values.update(
                {
                    "packaging_name": packaging_name,
                    "packaging_barcode": convert2str(packaging_barcode),
                    "packaging_quantity": convert2str(packaging_quantity),
                    "max_weight": convert2str(max_weight),
                    "weight": weight,
                    "length": length,
                    "width": width,
                    "height": height,
                }
            )
        return values

    def action_import_packaging(self):
        self.ensure_one()
        if not self.show_packaging_import:
            return {}
        if self.show_packaging_import and not self.packaging_import_id:
            self.packaging_import_id = self.env["product.packaging.import"].create(
                {
                    "file_date": fields.Date.today(),
                    "company_id": self.company_id.id,
                    "filename": self.filename,
                },
            )
        packaging_import_lines = self.import_line_ids.filtered(
            lambda ln: ln.state == "done"
            and ln.packaging_name
            and ln.product_id
            and not ln.import_packaging_line_id
        )
        if self.packaging_import_id and packaging_import_lines:
            for line in packaging_import_lines:
                line._create_packaging_import_line()
        context = self.env.context.copy()
        return {
            "name": _("Packaging Import"),
            "view_mode": "form",
            "res_model": "product.packaging.import",
            "res_id": self.packaging_import_id.id,
            "type": "ir.actions.act_window",
            "context": context,
        }
