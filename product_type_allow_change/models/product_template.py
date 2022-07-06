# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("type")
    def _onchange_type(self):
        res = super(ProductTemplate, self)._onchange_type() or {}
        if ("warning" in res and
                self.env.user.has_group("product_type_allow_change."
                                        "group_product_allow_type_change")):
            warning = res.get("warning").get("message", _("Not launched warning!"))
            _logger.warning(warning)
            del res["warning"]
        return res

    def write(self, vals):
        if (any("type" in vals and vals["type"] != prod_tmpl.type for prod_tmpl in self)
                and self.env.user.has_group("product_type_allow_change."
                                            "group_product_allow_type_change")):
            existing_move_lines = self.env["stock.move.line"].search([
                ("product_id", "in", self.mapped("product_variant_ids").ids),
                ("state", "in", ["partially_available", "assigned"]),
            ])
            if existing_move_lines:
                _logger.warning(
                    _("You should not change the type of a product that is currently "
                      "reserved on a stock move. If you need to change the type, you "
                      "should first unreserve the stock move."))
                existing_move_lines.mapped("move_id")._do_unreserve()
        return super(ProductTemplate, self).write(vals)
