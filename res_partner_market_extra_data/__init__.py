from . import models
from odoo import api, SUPERUSER_ID


def _post_install_load_data(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partners = env["res.partner"].search([])
    partners_to_treat = partners.filtered(lambda x: x.customer_technology_id)
    for partner in partners_to_treat:
        partner.customer_technology_ids = [(6, 0, partner.customer_technology_id.ids)]
    partners_to_treat = partners.filtered(lambda x: x.customer_marker_id)
    for partner in partners_to_treat:
        partner.customer_market_ids = [(6, 0, partner.customer_marker_id.ids)]
    partners_to_treat = partners.filtered(lambda x: x.customer_state_id.id)
    for partner in partners_to_treat:
        partner.customer_state_ids = [(6, 0, partner.customer_state_id.ids)]
    partners_to_treat = partners.filtered(lambda x: x.customer_business_area_id.id)
    for partner in partners_to_treat:
        partner.customer_business_area_ids = [
            (6, 0, partner.customer_business_area_id.ids)
        ]
