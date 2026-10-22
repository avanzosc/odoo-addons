# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def pre_init_hook(env):
    """
    Prepare new computed fields.
    """
    _logger.info("Pre-creating column last_payment_date for table account_move")
    if not column_exists(env.cr, "product_template", "product_state_id"):
        create_column(env.cr, "product_template", "product_state_id")


def post_init_hook(env):
    state_stock = env.ref("product_state_values.product_state_stock")
    cond = [("state", "=", "stock")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_stock.id

    state_clearance = env.ref("product_state_values.product_state_clearance")
    cond = [("state", "=", "clearance")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_clearance.id

    state_mto = env.ref("product_state_values.product_state_mto")
    cond = [("state", "=", "mto")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_mto.id

    state_sample = env.ref("product_state_values.product_state_sample")
    cond = [("state", "=", "sample")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_sample.id

    state_discontinued = env.ref("product_state_values.product_state_discontinued")
    cond = [("state", "=", "discontinued")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_discontinued.id

    state_inproject = env.ref("product_state_values.product_state_inproject")
    cond = [("state", "=", "inproject")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_inproject.id

    state_rstock = env.ref("product_state_values.product_state_rstock")
    cond = [("state", "=", "rstock")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_rstock.id

    state_sttock_cw = env.ref("product_state_values.product_state_sttock_cw")
    cond = [("state", "=", "sttock_cw")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_sttock_cw.id

    state_wstock = env.ref("product_state_values.product_state_wstock")
    cond = [("state", "=", "wstock")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_wstock.id

    state_available_oo = env.ref("product_state_values.product_state_available_oo")
    cond = [("state", "=", "available_oo")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_available_oo.id

    state_catalog = env.ref("product_state_values.product_state_catalog")
    cond = [("state", "=", "catalog")]
    products = env["product.template"].search(cond)
    if products:
        products.product_state_id = state_catalog.id
