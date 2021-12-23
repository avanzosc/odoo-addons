# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    brands = env['product.brand'].search([])
    seq = 1
    for brand in brands:
        cr.execute("""
            UPDATE product_brand
            SET sequence = %s
            WHERE id = %s""", (seq, brand.id))
        seq += 1
