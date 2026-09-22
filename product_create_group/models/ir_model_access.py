# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.private
    def init(self):
        accesses = self.search(
            [
                ("model_id", "=", "product.template"),
                "|",
                ("perm_create", "=", True),
                ("perm_unlink", "=", True),
            ]
        )
        try:
            accesses -= self.env.ref("product_create_group.access_create_product_tmpl")
        except ValueError:
            _logger.debug(
                "product_create_group ACL xmlid not yet available; "
                "stripping create/unlink on all existing product.template "
                "access records."
            )
        accesses.write({"perm_create": False, "perm_unlink": False})
