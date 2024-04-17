# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_date_planned_without_hour(self):
        for line in self.filtered(lambda x: x.date_planned):
            line.date_planned_without_hour = line.date_planned.date()

    def _compute_my_product_code(self):
        for line in self:
            supplier_info = line.product_id.seller_ids.filtered(
                lambda s: (
                    s.product_id == line.product_id
                    and s.name == line.partner_id
                    and s.product_code
                )
            )
            if supplier_info:
                line.my_product_code = supplier_info[0].product_code
            if not supplier_info:
                supplier_info = line.product_id.seller_ids.filtered(
                    lambda s: (
                        s.product_tmpl_id == line.product_id.product_tmpl_id
                        and s.name == line.partner_id
                        and s.product_code
                    )
                )
                if supplier_info:
                    line.my_product_code = supplier_info[0].product_code
                else:
                    line.my_product_code = line.product_id.default_code

    def _compute_description_to_print(self):
        print("22222 entro por 2")
        for line in self:
            supplier_info = line.product_id.seller_ids.filtered(
                lambda s: (
                    s.product_id == line.product_id
                    and s.name == line.partner_id
                    and s.product_name
                )
            )
            if supplier_info:
                line.description_to_print = supplier_info[0].product_name
            if not supplier_info:
                supplier_info = line.product_id.seller_ids.filtered(
                    lambda s: (
                        s.product_tmpl_id == line.product_id.product_tmpl_id
                        and s.name == line.partner_id
                        and s.product_name
                    )
                )
                if supplier_info:
                    line.description_to_print = supplier_info[0].product_name
                else:
                    line.description_to_print = ""
        print("222 salgo de 2")

    date_planned_without_hour = fields.Date(
        string="Scheduled Date", compute="_compute_date_planned_without_hour"
    )
    my_product_code = fields.Char(string="Code", compute="_compute_my_product_code")
    description_to_print = fields.Char(
        string="Description", compute="_compute_description_to_print"
    )
