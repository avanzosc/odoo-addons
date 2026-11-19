# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import base64

from odoo import models


class L10nEsAeatReportExportToBoe(models.TransientModel):
    _inherit = "l10n.es.aeat.report.export_to_boe"

    def _is_navarra_export(self, report):
        if "is_tax_agency_navarra" not in report._fields:
            return False
        return bool(
            report.is_tax_agency_navarra and report._get_navarra_export_config()
        )

    def _export_simple_record(self, line, val):
        if line.export_type == "raw_string":
            data = str(val or "").encode("iso-8859-1")[: line.size]
            return data.ljust(line.size, b" ")
        return super()._export_simple_record(line, val)

    def action_get_file_from_config(self, report):
        if self._is_navarra_export(report):
            return report._generate_navarra_file()
        return super().action_get_file_from_config(report)

    def action_get_file(self):
        active_id = self.env.context.get("active_id", False)
        active_model = self.env.context.get("active_model", False)
        if not active_id or not active_model:
            return super().action_get_file()
        report = self.env[active_model].browse(active_id)
        if not self._is_navarra_export(report):
            return super().action_get_file()
        contents = report._generate_navarra_file()
        file_name = report._get_navarra_export_filename()
        file = base64.encodebytes(contents)
        attachment_obj = self.env["ir.attachment"]
        attachment_obj.search(
            [("name", "=", file_name), ("res_model", "=", report._name)]
        ).unlink()
        attachment_obj.create(
            {
                "name": file_name,
                "datas": file,
                "res_model": report._name,
                "res_id": report.id,
            }
        )
        report.write(
            {
                "navarra_export_file": file,
                "navarra_export_filename": file_name,
            }
        )
        self.write({"state": "get", "data": file, "name": file_name})
        data_obj = self.env.ref("l10n_es_aeat.wizard_aeat_export")
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "view_id": [data_obj.id],
            "res_id": self.id,
            "target": "new",
        }
