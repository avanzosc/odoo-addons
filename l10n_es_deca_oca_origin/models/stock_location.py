from odoo import models
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = "stock.location"

    def unlink(self):
        locations = self.env.ref("l10n_es_deca_oca_origin.stock_location_deca_origin")
        locations |= self.env.ref(
            "l10n_es_deca_oca_origin.stock_location_deca_destination"
        )
        for location in self:
            if location.id in locations.ids:
                raise ValidationError(
                    self.env._(
                        "You cannot delete the location: '%s',  because it"
                        " is a location registered in the system."
                    )
                    % location.name
                )
        return super().unlink()
