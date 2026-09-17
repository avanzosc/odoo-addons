# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ProductImportLine(models.Model):
    _inherit = "product.import.line"

    season_name = fields.Char(copy=False)
    season_id = fields.Many2one(
        comodel_name="seasonality",
        domain="[('name', 'ilike', season_name)]",
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        product, __ = self._check_product()
        season, log_info_season = self._check_season(product=product)
        if log_info_season:
            update_values["log_info"] = "\n".join(
                filter(None, [update_values.get("log_info"), log_info_season])
            )
            update_values["state"] = "error"
            update_values["action"] = "nothing"
        update_values["season_id"] = season and season.id
        return update_values

    def _check_season(self, product=False):
        self.ensure_one()
        log_info = ""
        if self.season_id:
            return self.season_id, log_info
        if product and not self.season_name:
            return product.season_id, log_info
        if not self.season_name:
            return False, log_info
        season_obj = self.env["seasonality"]
        seasons = season_obj.search([("name", "=", self.season_name)])
        if not seasons:
            log_info = _("Season named %(season_name)s not found.") % {
                "season_name": self.season_name,
            }
        elif len(seasons) > 1:
            seasons = False
            log_info = _("More than one season exist.")
        return seasons, log_info

    def _product_values(self):
        values = super()._product_values()
        if self.season_id:
            values["season_id"] = self.season_id.id
        return values
