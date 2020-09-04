# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api
from datetime import datetime


class FleetRoute(models.Model):
    _inherit = 'fleet.route'

    @api.multi
    def _get_report_fleet_base_filename(self):
        self.ensure_one()
        return self.display_name

    def _get_actual_date(self):
        self.ensure_one()
        return datetime.now().strftime('%Y-%m-%d')
