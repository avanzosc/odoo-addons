# Copyright 2020 Alfredo de la  Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import json

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def show_product_inventory(self):
        history_obj = self.env["stock.quantity.history"]
        vals = {"compute_at_date": 0, "date": fields.Datetime.now()}
        wiz = history_obj.create(vals)
        result = wiz.open_table()
        context = result.get("context")
        json_acceptable_string = context.replace("'", '"')
        context = json.loads(json_acceptable_string)
        context["search_default_product_id"] = self.product_id.id
        result["context"] = str(context)
        return result
