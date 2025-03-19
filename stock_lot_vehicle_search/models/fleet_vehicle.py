import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("lot_id.name", operator, name)]
        vehicles = self.search(domain + args, limit=limit)
        return vehicles.name_get()
