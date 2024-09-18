# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, res_ids=None, data=None):
        if (
            self.model == "account.move"
            or self.model == "sale.order"
            or self.model == "purchase.order"
            or self.model == "stock.picking"
            and res_ids
        ):
            if (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("display_name_in_footer")
            ):
                data = data and dict(data) or {}
                data.update({"display_name_in_footer": True})
        return super()._render_qweb_pdf(res_ids=res_ids, data=data)
