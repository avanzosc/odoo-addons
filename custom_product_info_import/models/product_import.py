# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ProductImport(models.Model):
    _inherit = "product.import"

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            product_diameter = row_values.get("Diameter", "")
            product_hardness = row_values.get("Hardness", "")
            core_color = row_values.get("Core Color", "")
            wheel_color = row_values.get("Wheel Color", "")
            values.update(
                {
                    "product_diameter": product_diameter,
                    "product_hardness": product_hardness,
                    "core_color": core_color,
                    "wheel_color": wheel_color,
                }
            )
        return values

class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    product_diameter = fields.Integer(
        string="Diameter"
    )
    product_hardness = fields.Integer(
        string="Hardness"
    )
    core_color = fields.Char(
        string="Core Color",
    )
    wheel_color = fields.Char(
        string="Wheel Color",
    )
    core_color_id = fields.Many2one(
        string="Core Color",
        comodel_name="product.color"
    )
    wheel_color_id = fields.Many2one(
        string="Wheel Color",
        comodel_name="product.color"
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = (
            [update_values.get("log_info")]
            if update_values.get("log_info", False)
            else []
        )
        core_color = wheel_color = False
        if self.core_color:
            core_color, log_info_core_color = self._check_core_color()
            if log_info_core_color:
                log_infos.append(log_info_core_color)
        if self.wheel_color:
            wheel_color, log_info_wheel_color = self._check_wheel_color()
            if log_info_wheel_color:
                log_infos.append(log_info_wheel_color)
        state = "error" if log_infos else "pass"
        action = "nothing"
        if update_values.get("product_id", False) and state != "error":
            action = "update"
        elif state != "error":
            action = "create"
        update_values.update(
            {
                "core_color_id": core_color and core_color.id,
                "wheel_color_id": wheel_color and wheel_color.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _check_core_color(self):
        self.ensure_one()
        log_info = ""
        if self.core_color_id:
            return self.core_color_id, log_info
        return self._check_color(self.core_color)

    def _check_wheel_color(self):
        self.ensure_one()
        log_info = ""
        if self.wheel_color_id:
            return self.wheel_color_id, log_info
        return self._check_color(self.wheel_color)

    def _check_color(self, color_name=False):
        self.ensure_one()
        log_info = ""
        color_obj = self.env["product.color"]
        search_domain = [("name", "ilike", color_name)]
        colors = color_obj.search(search_domain)
        if not colors:
            log_info = _("Color not found.")
        elif len(colors) > 1:
            colors = False
            log_info = _("More than one color found.")
        return colors and colors[:1], log_info

    def _product_values(self):
        self.ensure_one()
        values = super(ProductImportLine, self)._product_values()
        values.update({
            "diameter": self.product_diameter,
            "hardness": self.product_hardness,
            "core_color_id": self.core_color_id and self.core_color_id.id,
            "wheel_color_id": self.wheel_color_id and self.wheel_color_id.id,
        })
        return values
