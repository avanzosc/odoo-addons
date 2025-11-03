from . import models
from . import reports
from odoo import api, SUPERUSER_ID


def _put_sale_info_in_invoices(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [("invoice_ids", "!=", False)]
    sales = env["sale.order"].search(cond)
    for sale in sales:
        modified = False
        for invoice in sale.invoice_ids:
            if sale.team_id and not invoice.team_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET team_id = %s
                    WHERE id = %s
                """,
                    (sale.team_id.id, invoice.id),
                )
            if sale.commercial_make_id and not invoice.commercial_make_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET commercial_make_id = %s
                    WHERE id = %s
                """,
                    (sale.commercial_make_id.id, invoice.id),
                )
            if (
                sale.num_allowed_commercial_make
                and not invoice.num_allowed_commercial_make
            ):
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET num_allowed_commercial_make = %s
                    WHERE id = %s
                """,
                    (sale.num_allowed_commercial_make, invoice.id),
                )
            if sale.relation_id and not invoice.relation_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET relation_id = %s
                    WHERE id = %s
                """,
                    (sale.relation_id.id, invoice.id),
                )
            if sale.classification_id and not invoice.classification_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET classification_id = %s
                    WHERE id = %s
                """,
                    (sale.classification_id.id, invoice.id),
                )
            if sale.allowed_commercial_make_ids:
                for make in sale.allowed_commercial_make_ids:
                    env.cr.execute(
                        """
                    SELECT 1 FROM account_move_product_make_rel
                    WHERE account_move_id = %s AND product_make_id = %s
                    """,
                        (invoice.id, make.id),
                    )
                    if not env.cr.fetchone():
                        modified = True
                        env.cr.execute(
                            """
                            INSERT INTO account_move_product_make_rel
                            (account_move_id, product_make_id)
                            VALUES (%s, %s)
                        """,
                            (invoice.id, make.id),
                        )
            if sale.market_id and not invoice.market_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET market_id = %s
                    WHERE id = %s
                """,
                    (sale.market_id.id, invoice.id),
                )
            if sale.market_sector_id and not invoice.market_sector_id:
                modified = True
                env.cr.execute(
                    """
                    UPDATE account_move
                    SET market_sector_id = %s
                    WHERE id = %s
                """,
                    (sale.market_sector_id.id, invoice.id),
                )
            if sale.global_discount_ids_readonly:
                for discount in sale.global_discount_ids_readonly:
                    env.cr.execute(
                        """
                    SELECT 1 FROM account_move_global_discount_rel
                    WHERE invoice_id = %s AND global_discount_id = %s
                    """,
                        (invoice.id, discount.id),
                    )
                    if not env.cr.fetchone():
                        modified = True
                        env.cr.execute(
                            """
                            INSERT INTO account_move_global_discount_rel
                            (invoice_id, global_discount_id)
                            VALUES (%s, %s)
                        """,
                            (invoice.id, discount.id),
                        )
        for sale_line in sale.order_line:
            for invoice_line in sale_line.invoice_lines:
                if sale_line.allowed_make_ids:
                    for make in sale_line.allowed_make_ids:
                        env.cr.execute(
                            """
                            SELECT 1 FROM account_move_line_product_make_rel
                            WHERE account_move_line_id = %s AND product_make_id = %s
                        """,
                            (invoice_line.id, make.id),
                        )
                        if not env.cr.fetchone():
                            modified = True
                            env.cr.execute(
                                """
                                INSERT INTO account_move_line_product_make_rel
                                (account_move_line_id, product_make_id)
                                VALUES (%s, %s)
                            """,
                                (invoice_line.id, make.id),
                            )
                if sale_line.team_id and not invoice_line.team_id:
                    modified = True
                    env.cr.execute(
                        """
                        UPDATE account_move_line
                        SET team_id = %s
                        WHERE id = %s
                    """,
                        (sale_line.team_id.id, invoice_line.id),
                    )
                if sale_line.make_id and not invoice_line.make_id:
                    modified = True
                    env.cr.execute(
                        """
                        UPDATE account_move_line
                        SET make_id = %s
                        WHERE id = %s
                    """,
                        (sale_line.make_id.id, invoice_line.id),
                    )
        if modified:
            env.cr.commit()
