# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vendor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
    )
    route_id = fields.Many2one(
        comodel_name="stock.location.route",
        string="Route",
        domain=[("sale_selectable", "=", True)],
        ondelete="restrict",
        check_company=True,
    )

    def update_vendor(self):
        self.ensure_one()
        for line in self.order_line:
            if line.check_valid_vendor(self.vendor_id):
                line.vendor_id = self.vendor_id

    def update_route(self):
        self.ensure_one()
        for line in self.order_line:
            line.route_id = self.route_id


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        if not self.product_id:
            return
        result = super().product_id_change()
        if not self.check_valid_vendor(self.vendor_id):
            self.vendor_id = False
        return result

    def check_valid_vendor(self, vendor):
        return vendor in self.env["res.partner"].search(
            safe_eval(self.vendor_id_domain)
        )
