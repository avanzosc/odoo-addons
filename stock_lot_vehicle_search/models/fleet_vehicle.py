import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """
        Search for vehicles by name or lot_id.name if lot_id exists.
        """
        result = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        if not name or not hasattr(self, "lot_id"):
            return result

        vehicles = self.search(
            ["|", ("name", operator, name), ("lot_id.name", operator, name)]
            + (args or []),
            limit=limit,
        )
        result_ids = {r[0] for r in result}
        result += [(v.id, v.name) for v in vehicles if v.id not in result_ids]
        return result
