# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from psycopg2 import sql

from odoo import _, api, fields, models

CLEANUP_TABLE_LABELS = {
    "stock_move_line": "Stock Move Lines",
    "stock_valuation_layer": "Stock Valuation Layers",
    "stock_quant": "Stock Quants",
    "stock_move": "Stock Moves",
    "stock_picking": "Stock Pickings",
    "account_partial_reconcile": "Partial Reconciliations",
    "account_payment_line": "Payment Lines",
    "account_move_line": "Journal Items",
    "account_move": "Journal Entries",
    "account_bank_statement": "Bank Statements",
    "account_payment_order": "Payment Orders",
    "purchase_order_line": "Purchase Order Lines",
    "purchase_order": "Purchase Orders",
    "sale_order_line": "Sale Order Lines",
    "sale_order": "Sale Orders",
}


class CleaningDatabase(models.Model):
    _name = "cleaning.database"
    _description = "Cleaning Database Operations"

    name = fields.Char(string="Description", copy=False)
    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        relation="rel_cleaning_database_company",
        column1="cleaning_database_id",
        column2="company_id",
        required=True,
    )

    def _prepare_cleanup_indexes(self, min_rows=1000):
        """Create useful missing FK indexes before deleting operational data."""
        self.ensure_one()

        cleanup_tables = tuple(CLEANUP_TABLE_LABELS.keys())
        if not cleanup_tables:
            return

        self.env.cr.execute(
            """
            SELECT
                c.oid AS constraint_oid,
                child.relname AS table_name,
                a.attname AS column_name,
                child.reltuples::bigint AS estimated_rows
            FROM pg_constraint c
            JOIN pg_class child
                ON child.oid = c.conrelid
            JOIN pg_attribute a
                ON a.attrelid = c.conrelid
            AND a.attnum = c.conkey[1]
            WHERE c.contype = 'f'
            AND cardinality(c.conkey) = 1
            AND c.confrelid IN (
                SELECT to_regclass('public.' || table_name)
                FROM unnest(%s::text[]) AS table_name
                WHERE to_regclass('public.' || table_name) IS NOT NULL
            )
            AND child.reltuples >= %s
            AND NOT EXISTS (
                SELECT 1
                FROM pg_index i
                WHERE i.indrelid = c.conrelid
                    AND i.indisvalid
                    AND i.indisready
                    AND i.indkey[0] = a.attnum
            )
            ORDER BY pg_total_relation_size(c.conrelid) DESC
            """,
            (list(cleanup_tables), min_rows),
        )

        missing_indexes = self.env.cr.fetchall()

        for constraint_oid, table_name, column_name, _estimated_rows in missing_indexes:
            index_name = f"cleanup_fk_{constraint_oid}_idx"

            self.env.cr.execute(
                sql.SQL(
                    """
                    CREATE INDEX IF NOT EXISTS {index}
                    ON {table} ({column})
                    """
                ).format(
                    index=sql.Identifier(index_name),
                    table=sql.Identifier(table_name),
                    column=sql.Identifier(column_name),
                )
            )

            self.env.cr.execute(
                sql.SQL("ANALYZE {}").format(sql.Identifier(table_name))
            )

        return len(missing_indexes)

    def action_open_delete_warning(self):
        self.ensure_one()

        context = dict(
            self.env.context,
            active_id=self.id,
            active_model=self._name,
        )

        wiz = (
            self.env["cleaning.database.warning.wizard"]
            .with_context(**context)
            .create({"object_to_delete": context.get("default_object_to_delete")})
        )

        return {
            "name": _("Cleaning Database Warning"),
            "type": "ir.actions.act_window",
            "res_model": "cleaning.database.warning.wizard",
            "view_type": "form",
            "view_mode": "form",
            "res_id": wiz.id,
            "target": "new",
            "context": context,
        }

    # -------------------------------------------------------------------------
    # Generic helpers
    # -------------------------------------------------------------------------

    def _count_rows_to_delete(
        self,
        table,
        where_clause,
        params,
    ):
        self.env.cr.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE {where_clause}
            """,
            tuple(params),
        )

        return self.env.cr.fetchone()[0]

    # Batched destructive cleanup intentionally commits after each batch to
    # release locks, persist progress and avoid a huge long-running transaction.
    # pylint: disable=invalid-commit
    def _delete_in_batches(
        self,
        table,
        where_clause,
        params,
        batch_size=10000,
    ):
        total_deleted = 0

        total_to_delete = self._count_rows_to_delete(
            table=table,
            where_clause=where_clause,
            params=params,
        )
        table_label = CLEANUP_TABLE_LABELS.get(table, table)

        self.env.user._bus_send(
            "simple_notification",
            {
                "title": _("Database Cleanup"),
                "message": _("Starting %(table)s. %(total)s records to delete.")
                % {
                    "table": table_label,
                    "total": f"{total_to_delete:,}",
                },
                "type": "info",
                "sticky": False,
            },
        )

        self.env.cr.commit()

        while True:
            self.env.cr.execute("SET LOCAL lock_timeout = '10s'")

            self.env.cr.execute(
                f"""
                DELETE FROM {table}
                WHERE ctid IN (
                    SELECT ctid
                    FROM {table}
                    WHERE {where_clause}
                    LIMIT %s
                )
                """,
                tuple(params) + (batch_size,),
            )

            deleted = self.env.cr.rowcount

            if not deleted:
                break

            total_deleted += deleted

            self._notify_cleanup_progress(
                table=table,
                total_deleted=total_deleted,
                total_to_delete=total_to_delete,
            )

            self.env.cr.commit()

        self._notify_cleanup_progress(
            table=table,
            total_deleted=total_deleted,
            total_to_delete=total_to_delete,
            finished=True,
        )

        self.env.cr.commit()

        return total_deleted

    # pylint: enable=invalid-commit

    def _is_full_database_cleanup(self):
        self.ensure_one()

        all_company_ids = set(
            self.env["res.company"].with_context(active_test=False).search([]).ids
        )
        selected_company_ids = set(self.company_ids.ids)

        return bool(all_company_ids) and selected_company_ids == all_company_ids

    def _delete_company_table(self, table, batch_size=10000):
        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                table=table,
                where_clause="TRUE",
                params=(),
                batch_size=batch_size,
            )

        return self._delete_in_batches(
            table=table,
            where_clause="company_id = ANY(%s)",
            params=(self.company_ids.ids,),
            batch_size=batch_size,
        )

    # -------------------------------------------------------------------------
    # Complete cleanup
    # -------------------------------------------------------------------------

    # Batched destructive maintenance intentionally commits its work.
    # pylint: disable=invalid-commit
    def action_delete_all_operations(self):
        self.ensure_one()

        self._prepare_cleanup_indexes()

        self._delete_all_operations()

        self.env.invalidate_all()
        return True

    # pylint: enable=invalid-commit

    def _delete_all_operations(self):
        self._delete_stock_operations()
        self._delete_accounting_operations()
        self._delete_purchase_operations()
        self._delete_sale_operations()

    # -------------------------------------------------------------------------
    # Operation helpers
    # -------------------------------------------------------------------------

    def _delete_stock_operations(self):
        self._delete_company_table("stock_move_line")
        self._delete_company_table("stock_valuation_layer")
        self._delete_stock_quant()
        self._delete_company_table("stock_move")
        self._delete_company_table("stock_picking")

    def _delete_accounting_operations(self):
        self._delete_company_table("account_partial_reconcile")
        self._delete_company_table("account_payment_line")
        self._delete_company_table("account_move_line")
        self._delete_company_table("account_move")
        self._delete_company_table("account_bank_statement")
        self._delete_company_table("account_payment_order")

    def _delete_purchase_operations(self):
        self._delete_company_table("purchase_order_line")
        self._delete_company_table("purchase_order")

    def _delete_sale_operations(self):
        self._delete_company_table("sale_order_line")
        self._delete_company_table("sale_order")

    def _delete_stock_quant(self):
        self.ensure_one()
        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                table="stock_quant",
                where_clause="TRUE",
                params=(),
            )

        return self._delete_in_batches(
            table="stock_quant",
            where_clause="""
                company_id = ANY(%s)
                OR lot_id IN (
                    SELECT id
                    FROM stock_lot
                    WHERE company_id = ANY(%s)
                )
            """,
            params=(
                self.company_ids.ids,
                self.company_ids.ids,
            ),
        )

    # -------------------------------------------------------------------------
    # Individual actions
    # -------------------------------------------------------------------------

    def action_delete_stock_operations(self):
        self.ensure_one()

        self._delete_stock_operations()
        self.env.invalidate_all()

        return True

    def action_delete_accounting_operations(self):
        self.ensure_one()

        self._delete_accounting_operations()
        self.env.invalidate_all()

        return True

    def action_delete_purchase_operations(self):
        self.ensure_one()

        self._delete_purchase_operations()
        self.env.invalidate_all()

        return True

    def action_delete_sale_operations(self):
        self.ensure_one()

        self._delete_sale_operations()
        self.env.invalidate_all()

        return True

    def action_delete_stock_production_lot(self):
        self.ensure_one()

        self._delete_company_table("stock_lot")

        self.env.invalidate_all()

        return True

    def action_delete_sequence_operations(self):
        self.ensure_one()

        sequences = self.env["ir.sequence"].search(
            [
                ("number_next_actual", "!=", 1),
                ("company_id", "in", self.company_ids.ids),
            ]
        )

        sequences.write({"number_next_actual": 1})

        return True

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            vals["name"] = _("Creation date: {}").format(fields.Datetime.now())

        return super().create(values)

    def _notify_cleanup_progress(
        self,
        table,
        total_deleted,
        total_to_delete,
        finished=False,
    ):
        table_label = CLEANUP_TABLE_LABELS.get(table, table)

        remaining = max(
            total_to_delete - total_deleted,
            0,
        )

        percentage = (
            round(
                (total_deleted / total_to_delete) * 100,
                1,
            )
            if total_to_delete
            else 100.0
        )

        if finished:
            message = _("%(table)s completed. %(deleted)s records deleted.") % {
                "table": table_label,
                "deleted": f"{total_deleted:,}",
            }

            notification_type = "success"

        else:
            message = _(
                "%(table)s: %(deleted)s deleted. "
                "%(remaining)s remaining "
                "(%(percentage)s%% completed)."
            ) % {
                "table": table_label,
                "deleted": f"{total_deleted:,}",
                "remaining": f"{remaining:,}",
                "percentage": percentage,
            }

            notification_type = "info"

        self.env.user._bus_send(
            "simple_notification",
            {
                "title": _("Database Cleanup"),
                "message": message,
                "type": notification_type,
                "sticky": False,
            },
        )
