from . import models
from odoo import api, SUPERUSER_ID


def _post_install_load_data(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    lines = env["stock.warehouse.orderpoint"].search([])
    lines.update_forecast_info()
