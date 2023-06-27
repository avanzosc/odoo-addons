# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str


class ProductImport(models.Model):
    _inherit = "product.import"

    packaging_import_id = fields.Many2one(
        string="Packaging Import",
        comodel_name="product.packaging.import",
        readonly=True)

    def _get_line_values(self, row_values={}):
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
            values.update({
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
        packaging_import = self.packaging_import_id
        if not self.packaging_import_id:
            packaging_import = (
                self.env["product.packaging.import"].create({
                    "file_date": fields.Date.today(),
                    "company_id": self.company_id.id,
                    "filename": self.filename}))
            self.packaging_import_id = packaging_import.id
        for line in self.import_line_ids.filtered(
            lambda l: l.state == "done" and not (
                l.import_packaging_line_id)):
            packaging_import_line = (
                self.env["product.packaging.import.line"].create({
                    "product_name": line.product_name,
                    "product_default_code": line.product_default_code,
                    "product_id": line.product_id.id,
                    "packaging_name": line.packaging_name,
                    "barcode": line.packaging_barcode,
                    "quantity": line.packaging_quantity,
                    "max_weight": line.max_weight,
                    "weight": line.weight,
                    "length": line.length,
                    "width": line.width,
                    "height": line.width,
                    "import_id": packaging_import.id}))
            line.import_packaging_line_id = packaging_import_line.id

    def action_view_packaging_import(self):
        context = self.env.context.copy()
        return {
            'name': _("Packaging Import"),
            'view_mode': 'tree,form',
            'res_model': 'product.packaging.import',
            'domain': [('id', '=', self.packaging_import_id.ids)],
            'type': 'ir.actions.act_window',
            'context': context
        }
