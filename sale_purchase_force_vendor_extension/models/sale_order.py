# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vendor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
    )
    route_id = fields.Many2one(
        comodel_name="stock.route",
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
    def _onchange_product_id_vendor(self):
        if self.vendor_id and not self.check_valid_vendor(self.vendor_id):
            self.vendor_id = False

    def check_valid_vendor(self, vendor):
        if not vendor:
            return False
        domain = self.vendor_id_domain or []
        valid_vendors = self.env["res.partner"].search(domain)
        return vendor in valid_vendors
