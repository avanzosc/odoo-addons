# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_name_max_length = fields.Integer(
        string="Max. Length Product Name",
    )
    product_name_max_length_for_labels = fields.Integer(
        string="Max. Length Product Name For Labels",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            product_name_max_length=int(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("product_name_max_length", default=250)
            ),
            product_name_max_length_for_labels=int(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("product_name_max_length_for_labels", default=55)
            ),
        )
        return res

    def set_values(self):
        result = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "product_name_max_length", self.product_name_max_length
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "product_name_max_length_for_labels",
            self.product_name_max_length_for_labels,
        )
        return result
