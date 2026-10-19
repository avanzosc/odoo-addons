# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.http import request

always_public_paths = [
    "/shop/cart",
    "/shop/cart/update_json",
    "/shop/cart/quantity",
]


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _check_require_auth(cls):
        path = request.httprequest.path
        if path not in always_public_paths:
            return super()._check_require_auth()
