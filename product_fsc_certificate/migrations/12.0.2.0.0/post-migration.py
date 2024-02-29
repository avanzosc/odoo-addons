# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """Force recomputing all is_fsc_certificate"""
    openupgrade.logged_query(
        env.cr,
        """UPDATE sale_order SET is_fsc_certificate = False"""
    )
    openupgrade.logged_query(
        env.cr,
        """UPDATE stock_picking SET is_fsc_certificate = False""",
    )
    openupgrade.logged_query(
        env.cr,
        """UPDATE account_invoice SET is_fsc_certificate = False""",
    )
    templates = env["product.template"].search(
        [("is_fsc_certificate", "=", True)],
    )
    order_lines = env["sale.order.line"].search([
        ("product_id", "in", templates.mapped("product_variant_ids").ids),
    ])
    openupgrade.logged_query(
        env.cr,
        """UPDATE sale_order SET is_fsc_certificate = True WHERE id IN (%s)""" %
        ",".join(str(id) for id in order_lines.mapped("order_id").ids)
    )
    stock_moves = env["stock.move"].search([
        ("product_id", "in", templates.mapped("product_variant_ids").ids),
    ])
    openupgrade.logged_query(
        env.cr,
        """UPDATE stock_picking SET is_fsc_certificate = True WHERE id IN (%s)""" %
        ",".join(str(id) for id in stock_moves.mapped("picking_id").ids)
    )
    invoice_lines = env["account.invoice.line"].search([
        ("product_id", "in", templates.mapped("product_variant_ids").ids),
    ])
    openupgrade.logged_query(
        env.cr,
        """UPDATE account_invoice SET is_fsc_certificate = True WHERE id IN (%s)""" %
        ",".join(str(id) for id in invoice_lines.mapped("invoice_id").ids)
    )

