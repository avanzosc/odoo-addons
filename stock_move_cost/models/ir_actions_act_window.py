# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_window"

    def read(self, fields=None, load="_classic_read"):
        result = super().read(fields=fields, load=load)
        if self.env.user.has_group("product_cost_security.group_product_cost"):
            return result
        for action in result:
            views = action.get("views", [])
            res_model = action.get("res_model")
            # stock.move.line: ocultar pivot
            if res_model == "stock.move.line":
                action["views"] = [
                    (view_id, view_type)
                    for view_id, view_type in views
                    if view_type != "pivot"
                ]
            # stock.move: ocultar graph
            elif res_model == "stock.move":
                for view_id, view_type in views:
                    action["views"] = [
                        (view_id, view_type)
                        for view_id, view_type in views
                        if view_type != "graph"
                    ]
        return result
