# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockNumberPackageValidateWiz(models.TransientModel):
    _inherit = "stock.number.package.validate.wizard"

    def _print_package_label(self):
        report = self.env.ref(
            "stock_picking_box_label_report.action_picking_all_box_label_report"
        )
        report_action = report.report_action(self.pick_ids)
        report_action.update({"close_on_report_download": True})
        return report_action
