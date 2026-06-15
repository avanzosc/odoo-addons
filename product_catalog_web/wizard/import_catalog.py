# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import io

import openpyxl

from odoo import _, fields, models
from odoo.exceptions import UserError


class ImportCatalogWeb(models.TransientModel):
    _name = "import.catalog.web"
    _description = "Import products to catalog from Excel"

    file_bin = fields.Binary(string="Excel File", required=True)
    replace = fields.Boolean(
        string="Replace all products",
        help="If checked, removes all current products from the catalog before import.",
    )

    def action_import(self):
        self.ensure_one()
        active_id = self._context.get("active_id")
        if not active_id:
            raise UserError(_("No active catalog found."))

        try:
            data = base64.decodebytes(self.file_bin)
            workbook = openpyxl.load_workbook(io.BytesIO(data))
        except Exception:
            raise UserError(
                _("Could not read the file. Make sure it is a valid Excel file.")
            ) from None

        sheet = workbook.active
        product_obj = self.env["product.product"]
        catalog = self.env["product.catalog.web"].browse(active_id)

        product_ids = [] if self.replace else list(catalog.product_ids.ids)

        for row in sheet.iter_rows(min_row=2, values_only=True):
            default_code = str(row[0]).strip() if row[0] is not None else False
            if not default_code or default_code == "False":
                continue
            product = product_obj.search([("default_code", "=", default_code)], limit=1)
            if product:
                tmpl_id = product.product_tmpl_id.id
                if tmpl_id not in product_ids:
                    product_ids.append(tmpl_id)

        catalog.write({"product_ids": [(6, 0, product_ids)]})
        return {"type": "ir.actions.act_window_close"}
