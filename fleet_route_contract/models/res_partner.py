# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def add_passenger_contract_line(self):
        current_academic_year = self.env["education.academic_year"].search([
            ("current", "=", True),
        ])
        contract_line_wiz = self.env["contract.line.create"]
        for partner in self.filtered("stop_ids"):
            products = partner.mapped("stop_ids.route_product_id")
            if not products:
                stop_num = len(partner.stop_ids)
                if stop_num == 2:
                    products = partner.mapped(
                        "stop_ids.route_id.name_id.complete_route_product_id")
                elif stop_num == 1:
                    products = partner.mapped(
                        "stop_ids.route_id.name_id.half_route_product_id")
            for product in products:
                line_wiz = contract_line_wiz.create({
                    "student_ids": [(6, 0, partner.ids)],
                    "product_id": product.id,
                    "price_unit": product.lst_price,
                    "date_start": current_academic_year.date_start,
                    "date_end": current_academic_year.date_end,
                })
                line_wiz.button_create_contract_line()
