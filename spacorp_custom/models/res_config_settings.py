# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from ast import literal_eval

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    text_delivery_vouchers = fields.Text(
        string="Text for delivery vouchers", translate=True
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        # the value of the parameter is a nonempty string
        text = literal_eval(
            get_param("spacorp_custom.text_delivery_vouchers", default="False")
        )
        res.update(
            text_delivery_vouchers=text,
        )
        return res

    def set_values(self):
        super().set_values()
        set_param = self.env["ir.config_parameter"].sudo().set_param
        set_param(
            "spacorp_custom.text_delivery_vouchers", repr(self.text_delivery_vouchers)
        )
