# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import hashlib
import json
import logging

from psycopg2 import sql

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


CLEANUP_TABLE_LABELS = {
    # Stock
    "stock_move_line": "Stock Move Lines",
    "stock_valuation_layer": "Stock Valuation Layers",
    "stock_quant": "Stock Quants",
    "stock_move": "Stock Moves",
    "stock_picking": "Stock Pickings",
    "stock_inventory": "Stock Inventories",
    "stock_production_lot": "Stock Production Lots",
    # Accounting
    "account_analytic_line": "Analytic Entries",
    "account_partial_reconcile": "Partial Reconciliations",
    "account_payment_order": "Payment Orders",
    "account_payment_line": "Payment Lines",
    "l10n_es_aeat_mod347_move_record": "AEAT 347 Move Records",
    "l10n_es_aeat_mod349_partner_record_detail": ("AEAT 349 Partner Record Details"),
    "account_move_line": "Journal Items",
    "account_move": "Journal Entries",
    "account_bank_statement": "Bank Statements",
    "account_asset_line": "Asset Lines",
    "account_asset": "Assets",
    "account_check_deposit": "Check Deposits",
    # Purchase
    "purchase_order_line": "Purchase Order Lines",
    "purchase_order": "Purchase Orders",
    # Sale
    "sale_order_line": "Sale Order Lines",
    "sale_order": "Sale Orders",
    # MRP
    "mrp_workorder": "MRP Work Orders",
    "mrp_production": "Manufacturing Orders",
    # Custom
    "transport_carrier_lines_to_invoice": "Transport Carrier Lines To Invoice",
}


class CleaningDatabase(models.Model):
    _name = "cleaning.database"
    _description = "Cleaning Database Operations"

    name = fields.Char(
        string="Description",
        copy=False,
    )

    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        relation="rel_cleaning_database_company",
        column1="cleaning_database_id",
        column2="company_id",
        required=True,
    )

    # -------------------------------------------------------------------------
    # Generic helpers
    # -------------------------------------------------------------------------

    def _is_full_database_cleanup(self):
        self.ensure_one()

        all_company_ids = set(
            self.env["res.company"]
            .sudo()
            .with_context(active_test=False)
            .search([])
            .ids
        )
        selected_company_ids = set(self.company_ids.ids)

        return bool(all_company_ids) and selected_company_ids == all_company_ids

    def _cleanup_progress_channel(self):
        self.ensure_one()

        return json.dumps(
            [
                self.env.cr.dbname,
                "cleaning.database.progress",
                self.env.uid,
            ],
            separators=(",", ":"),
        )

    def _send_cleanup_notification(
        self,
        message,
        notification_type="info",
        finished=False,
    ):
        self.ensure_one()

        self.env["bus.bus"].sendone(
            self._cleanup_progress_channel(),
            {
                "type": "cleaning_database_progress",
                "title": _("Database Cleanup"),
                "message": message,
                "notification_type": notification_type,
                "finished": finished,
            },
        )

    def _notify_cleanup_progress(
        self,
        table,
        total_deleted,
        total_to_delete=None,
        finished=False,
    ):
        self.ensure_one()

        table_label = CLEANUP_TABLE_LABELS.get(
            table,
            table,
        )

        if finished:
            message = _("%(table)s completed. %(deleted)s records deleted.") % {
                "table": table_label,
                "deleted": "{:,}".format(total_deleted),
            }

            notification_type = "success"

        elif total_to_delete is None:
            message = _("%(table)s\n%(deleted)s records deleted...") % {
                "table": table_label,
                "deleted": "{:,}".format(total_deleted),
            }

            notification_type = "info"

        else:
            remaining = max(
                total_to_delete - total_deleted,
                0,
            )

            percentage = (
                round(
                    total_deleted * 100.0 / total_to_delete,
                    1,
                )
                if total_to_delete
                else 100.0
            )

            message = _(
                "%(table)s\n"
                "%(deleted)s / %(total)s deleted\n"
                "%(percentage)s%% completed\n"
                "%(remaining)s remaining"
            ) % {
                "table": table_label,
                "deleted": "{:,}".format(total_deleted),
                "total": "{:,}".format(total_to_delete),
                "percentage": percentage,
                "remaining": "{:,}".format(remaining),
            }

            notification_type = "info"

        self._send_cleanup_notification(
            message=message,
            notification_type=notification_type,
            finished=finished,
        )

    # pylint: disable=invalid-commit
    def _prepare_cleanup_indexes(self, min_estimated_rows=1000):
        """Create missing FK indexes useful for the cleanup.

        Only single-column foreign keys pointing to cleanup tables are
        considered.

        Small referencing tables are ignored because creating an index on
        them normally costs more than it helps during this maintenance task.
        """
        self.ensure_one()

        cleanup_tables = list(CLEANUP_TABLE_LABELS)

        self.env.cr.execute(
            """
            SELECT
                child_namespace.nspname AS schema_name,
                child.relname AS table_name,
                attribute.attname AS column_name,
                parent.relname AS referenced_table,
                GREATEST(child.reltuples::bigint, 0) AS estimated_rows
            FROM pg_constraint constraint_info
            JOIN pg_class child
                ON child.oid = constraint_info.conrelid
            JOIN pg_namespace child_namespace
                ON child_namespace.oid = child.relnamespace
            JOIN pg_class parent
                ON parent.oid = constraint_info.confrelid
            JOIN pg_namespace parent_namespace
                ON parent_namespace.oid = parent.relnamespace
            JOIN pg_attribute attribute
                ON attribute.attrelid = constraint_info.conrelid
            AND attribute.attnum = constraint_info.conkey[1]
            WHERE constraint_info.contype = 'f'
            AND array_length(constraint_info.conkey, 1) = 1
            AND child_namespace.nspname = 'public'
            AND parent_namespace.nspname = 'public'
            AND parent.relname = ANY(%s)
            AND GREATEST(child.reltuples::bigint, 0) >= %s
            AND NOT EXISTS (
                SELECT 1
                FROM pg_index index_info
                WHERE index_info.indrelid = constraint_info.conrelid
                    AND index_info.indisvalid
                    AND index_info.indisready
                    AND index_info.indpred IS NULL
                    AND index_info.indkey[0] = attribute.attnum
            )
            ORDER BY child.reltuples DESC
            """,
            (
                cleanup_tables,
                min_estimated_rows,
            ),
        )

        missing_indexes = self.env.cr.fetchall()

        if not missing_indexes:
            _logger.info("Database Cleanup - No missing FK indexes detected.")
            return 0

        _logger.info(
            "Database Cleanup - %s missing FK indexes detected.",
            len(missing_indexes),
        )

        created = 0

        for (
            schema_name,
            table_name,
            column_name,
            referenced_table,
            estimated_rows,
        ) in missing_indexes:
            base_name = "{}_{}_cleanup_idx".format(
                table_name,
                column_name,
            )

            if len(base_name) > 63:
                digest = hashlib.sha1(base_name.encode("utf-8")).hexdigest()[:8]

                index_name = "{}_{}".format(
                    base_name[:54],
                    digest,
                )
            else:
                index_name = base_name

            _logger.info(
                "Database Cleanup - Creating index %s on %s.%s "
                "(FK -> %s, estimated rows: %s)",
                index_name,
                table_name,
                column_name,
                referenced_table,
                estimated_rows,
            )

            self.env.cr.execute(
                sql.SQL(
                    """
                    CREATE INDEX IF NOT EXISTS {}
                    ON {}.{} ({})
                    """
                ).format(
                    sql.Identifier(index_name),
                    sql.Identifier(schema_name),
                    sql.Identifier(table_name),
                    sql.Identifier(column_name),
                )
            )

            # This is a destructive maintenance tool and commits are
            # intentional. Persist each potentially expensive index.
            self.env.cr.commit()

            created += 1

        _logger.info(
            "Database Cleanup - FK index preparation finished. %s indexes created.",
            created,
        )

        return created

    def _clean_orphan_pseudo_relations(self):
        """Clear orphan Reference and Many2oneReference values.

        References are cleared when:

        * the referenced model no longer exists in the registry, or
        * the referenced model belongs to one of the cleanup tables and
        the referenced record no longer exists.

        References to models outside the cleanup scope are left untouched.
        """
        self.ensure_one()

        cleanup_tables = set(CLEANUP_TABLE_LABELS)
        available_models = set(self.env.registry.models)

        cleanup_models = {}

        for model_name, model in self.env.registry.models.items():
            table_name = getattr(model, "_table", False)

            if table_name in cleanup_tables:
                cleanup_models[model_name] = table_name

        total_cleaned = 0
        processed_fields = set()

        _logger.info("Database Cleanup - Starting orphan pseudo-relation cleanup.")

        for model_name, model in self.env.registry.models.items():
            if not getattr(model, "_auto", False):
                continue

            table_name = getattr(model, "_table", False)

            if not table_name:
                continue

            for field_name, field in model._fields.items():
                if not field.store:
                    continue

                if getattr(field, "inherited", False):
                    continue

                # -------------------------------------------------------------
                # fields.Reference
                # -------------------------------------------------------------
                if field.type == "reference":
                    field_key = (
                        "reference",
                        table_name,
                        field_name,
                    )

                    if field_key in processed_fields:
                        continue

                    processed_fields.add(field_key)

                    if field.required:
                        _logger.warning(
                            "Database Cleanup - Skipping required Reference "
                            "field %s.%s.",
                            model_name,
                            field_name,
                        )
                        continue

                    self.env.cr.execute(
                        sql.SQL(
                            """
                            SELECT DISTINCT
                                split_part({}, ',', 1)
                            FROM {}
                            WHERE {} IS NOT NULL
                            AND {} != ''
                            """
                        ).format(
                            sql.Identifier(field_name),
                            sql.Identifier(table_name),
                            sql.Identifier(field_name),
                            sql.Identifier(field_name),
                        )
                    )

                    referenced_models = [
                        row[0] for row in self.env.cr.fetchall() if row[0]
                    ]

                    for referenced_model in referenced_models:
                        # Model disappeared completely from the registry.
                        if referenced_model not in available_models:
                            self.env.cr.execute(
                                sql.SQL(
                                    """
                                    UPDATE {}
                                    SET {} = NULL
                                    WHERE split_part({}, ',', 1) = %s
                                    """
                                ).format(
                                    sql.Identifier(table_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(field_name),
                                ),
                                (referenced_model,),
                            )

                            cleaned = self.env.cr.rowcount

                        # Existing model, but one of the models whose
                        # operational records are being cleaned.
                        elif referenced_model in cleanup_models:
                            referenced_table = cleanup_models[referenced_model]

                            self.env.cr.execute(
                                sql.SQL(
                                    """
                                    UPDATE {} AS source
                                    SET {} = NULL
                                    WHERE split_part(
                                            source.{},
                                            ',',
                                            1
                                        ) = %s
                                    AND NOT EXISTS (
                                        SELECT 1
                                            FROM {} AS target
                                            WHERE target.id = CASE
                                                WHEN split_part(
                                                    source.{},
                                                    ',',
                                                    2
                                                ) ~ '^[0-9]+$'
                                                THEN split_part(
                                                    source.{},
                                                    ',',
                                                    2
                                                )::integer
                                                ELSE NULL
                                            END
                                    )
                                    """
                                ).format(
                                    sql.Identifier(table_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(referenced_table),
                                    sql.Identifier(field_name),
                                    sql.Identifier(field_name),
                                ),
                                (referenced_model,),
                            )

                            cleaned = self.env.cr.rowcount

                        else:
                            continue

                        if cleaned:
                            total_cleaned += cleaned

                            _logger.info(
                                "Database Cleanup - Cleared %s orphan "
                                "references from %s.%s to %s.",
                                cleaned,
                                table_name,
                                field_name,
                                referenced_model,
                            )

                            self.env.cr.commit()

                # -------------------------------------------------------------
                # fields.Many2oneReference
                # -------------------------------------------------------------
                elif field.type == "many2one_reference":
                    model_field_name = field.model_field

                    if not model_field_name:
                        continue

                    model_field = model._fields.get(model_field_name)

                    if (
                        not model_field
                        or not model_field.store
                        or getattr(model_field, "inherited", False)
                    ):
                        continue

                    field_key = (
                        "many2one_reference",
                        table_name,
                        field_name,
                        model_field_name,
                    )

                    if field_key in processed_fields:
                        continue

                    processed_fields.add(field_key)

                    if field.required:
                        _logger.warning(
                            "Database Cleanup - Skipping required "
                            "Many2oneReference field %s.%s.",
                            model_name,
                            field_name,
                        )
                        continue

                    self.env.cr.execute(
                        sql.SQL(
                            """
                            SELECT DISTINCT {}
                            FROM {}
                            WHERE {} IS NOT NULL
                            AND {} IS NOT NULL
                            """
                        ).format(
                            sql.Identifier(model_field_name),
                            sql.Identifier(table_name),
                            sql.Identifier(field_name),
                            sql.Identifier(model_field_name),
                        )
                    )

                    referenced_models = [
                        row[0] for row in self.env.cr.fetchall() if row[0]
                    ]

                    for referenced_model in referenced_models:
                        if referenced_model not in available_models:
                            self.env.cr.execute(
                                sql.SQL(
                                    """
                                    UPDATE {}
                                    SET {} = NULL
                                    WHERE {} = %s
                                    AND {} IS NOT NULL
                                    """
                                ).format(
                                    sql.Identifier(table_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(model_field_name),
                                    sql.Identifier(field_name),
                                ),
                                (referenced_model,),
                            )

                            cleaned = self.env.cr.rowcount

                        elif referenced_model in cleanup_models:
                            referenced_table = cleanup_models[referenced_model]

                            self.env.cr.execute(
                                sql.SQL(
                                    """
                                    UPDATE {} AS source
                                    SET {} = NULL
                                    WHERE source.{} = %s
                                    AND source.{} IS NOT NULL
                                    AND NOT EXISTS (
                                        SELECT 1
                                            FROM {} AS target
                                            WHERE target.id = source.{}
                                    )
                                    """
                                ).format(
                                    sql.Identifier(table_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(model_field_name),
                                    sql.Identifier(field_name),
                                    sql.Identifier(referenced_table),
                                    sql.Identifier(field_name),
                                ),
                                (referenced_model,),
                            )

                            cleaned = self.env.cr.rowcount

                        else:
                            continue

                        if cleaned:
                            total_cleaned += cleaned

                            _logger.info(
                                "Database Cleanup - Cleared %s orphan "
                                "many2one references from %s.%s to %s.",
                                cleaned,
                                table_name,
                                field_name,
                                referenced_model,
                            )

                            self.env.cr.commit()

        _logger.info(
            "Database Cleanup - Orphan pseudo-relation cleanup "
            "finished. %s references cleared.",
            total_cleaned,
        )

        return total_cleaned

    # pylint: enable=invalid-commit

    def _count_rows_to_delete(
        self,
        table,
        where_clause,
        params,
    ):
        self.env.cr.execute(
            """
            SELECT COUNT(*)
            FROM {}
            WHERE {}
            """.format(
                table,
                where_clause,
            ),
            tuple(params),
        )

        return self.env.cr.fetchone()[0]

    # Destructive maintenance operation.
    # Commits are intentional so huge cleanups do not keep
    # one enormous transaction open.
    # pylint: disable=invalid-commit
    def _delete_in_batches(
        self,
        table,
        where_clause,
        params,
        batch_size=10000,
        count_rows=True,
        notification_every=50000,
    ):
        self.ensure_one()

        total_deleted = 0

        total_to_delete = (
            self._count_rows_to_delete(
                table,
                where_clause,
                params,
            )
            if count_rows
            else None
        )

        table_label = CLEANUP_TABLE_LABELS.get(
            table,
            table,
        )

        if total_to_delete is None:
            _logger.info(
                "Database Cleanup - Starting %s without initial count.",
                table_label,
            )
        else:
            _logger.info(
                "Database Cleanup - Starting %s. %s records to delete.",
                table_label,
                total_to_delete,
            )

            if total_to_delete:
                self._notify_cleanup_progress(
                    table=table,
                    total_deleted=0,
                    total_to_delete=total_to_delete,
                )

                # Deliver the initial progress notification immediately.
                self.env.cr.commit()

        while True:
            self.env.cr.execute("SET LOCAL lock_timeout = '10s'")

            self.env.cr.execute(
                """
                DELETE FROM {table}
                WHERE ctid IN (
                    SELECT ctid
                    FROM {table}
                    WHERE {where_clause}
                    LIMIT %s
                )
                """.format(
                    table=table,
                    where_clause=where_clause,
                ),
                tuple(params) + (batch_size,),
            )

            deleted = self.env.cr.rowcount

            if not deleted:
                break

            total_deleted += deleted

            if total_to_delete is not None:
                percentage = (
                    total_deleted * 100.0 / total_to_delete
                    if total_to_delete
                    else 100.0
                )

                _logger.info(
                    "Database Cleanup - %s: %s/%s deleted (%.1f%%)",
                    table_label,
                    total_deleted,
                    total_to_delete,
                    percentage,
                )
            else:
                _logger.info(
                    "Database Cleanup - %s: %s records deleted.",
                    table_label,
                    total_deleted,
                )

            if total_deleted % notification_every == 0:
                self._notify_cleanup_progress(
                    table=table,
                    total_deleted=total_deleted,
                    total_to_delete=total_to_delete,
                )

            self.env.cr.commit()

        _logger.info(
            "Database Cleanup - Finished %s. %s records deleted.",
            table_label,
            total_deleted,
        )

        self._notify_cleanup_progress(
            table=table,
            total_deleted=total_deleted,
            total_to_delete=total_to_delete,
            finished=True,
        )

        self.env.cr.commit()

        return total_deleted

    # pylint: enable=invalid-commit

    def _delete_company_table(
        self,
        table,
        batch_size=10000,
    ):
        self.ensure_one()

        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                table,
                "TRUE",
                (),
                batch_size=batch_size,
            )

        return self._delete_in_batches(
            table,
            "company_id = ANY(%s)",
            (self.company_ids.ids,),
            batch_size=batch_size,
        )

    # -------------------------------------------------------------------------
    # Complete cleanup
    # -------------------------------------------------------------------------

    def action_delete_all_operations(self):
        self.ensure_one()

        _logger.warning(
            "Database Cleanup - Starting COMPLETE cleanup for companies: %s",
            self.company_ids.mapped("name"),
        )

        # Prepare indexes before deleting millions of records.
        self._prepare_cleanup_indexes()

        self._delete_all_operations()

        self._clean_orphan_pseudo_relations()

        self.env.cache.invalidate()

        _logger.warning(
            "Database Cleanup - COMPLETE cleanup finished for companies: %s",
            self.company_ids.mapped("name"),
        )

        return True

    def _delete_all_operations(self):
        self.ensure_one()

        # Custom/leaf records first.
        self._delete_transport_operations()

        # Stock before MRP because stock moves can be linked to productions.
        self._delete_stock_operations()

        # Manufacturing.
        self._delete_mrp_operations()

        # Accounting, including payment orders and assets.
        self._delete_accounting_operations()

        # Commercial documents last.
        self._delete_purchase_operations()
        self._delete_sale_operations()

    # -------------------------------------------------------------------------
    # Stock
    # -------------------------------------------------------------------------

    def _delete_stock_quant(self):
        self.ensure_one()

        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                "stock_quant",
                "TRUE",
                (),
                count_rows=False,
            )

        total_deleted = 0

        # Normal quants belonging directly to the selected companies.
        total_deleted += self._delete_in_batches(
            "stock_quant",
            "company_id = ANY(%s)",
            (self.company_ids.ids,),
            count_rows=False,
        )

        # Remaining quants linked to lots belonging to the selected companies.
        total_deleted += self._delete_in_batches(
            "stock_quant",
            """
            lot_id IN (
                SELECT id
                FROM stock_production_lot
                WHERE company_id = ANY(%s)
            )
            """,
            (self.company_ids.ids,),
            count_rows=False,
        )

        return total_deleted

    def _delete_stock_operations(self):
        self.ensure_one()

        self._delete_company_table("stock_move_line")

        self._delete_company_table("stock_valuation_layer")

        self._delete_stock_quant()

        self._delete_company_table("stock_move")

        self._delete_company_table("stock_picking")

        self._delete_company_table("stock_inventory")

    def action_delete_stock_operations(self):
        self.ensure_one()

        self._delete_stock_operations()

        self.env.cache.invalidate()

        return True

    def action_delete_stock_valuation_operations(self):
        self.ensure_one()

        self._delete_company_table("stock_valuation_layer")

        self.env.cache.invalidate()

        return True

    def action_delete_stock_production_lot(self):
        self.ensure_one()

        self._delete_company_table("stock_production_lot")

        self._clean_orphan_pseudo_relations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # Sale
    # -------------------------------------------------------------------------

    def _delete_sale_operations(self):
        self.ensure_one()

        self._delete_company_table("sale_order_line")

        self._delete_company_table("sale_order")

    def action_delete_sale_operations(self):
        self.ensure_one()

        self._delete_sale_operations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # Purchase
    # -------------------------------------------------------------------------

    def _delete_purchase_operations(self):
        self.ensure_one()

        self._delete_company_table("purchase_order_line")

        self._delete_company_table("purchase_order")

    def action_delete_purchase_operations(self):
        self.ensure_one()

        self._delete_purchase_operations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # Accounting
    # -------------------------------------------------------------------------

    def _delete_accounting_operations(self):
        self.ensure_one()

        self._delete_company_table("account_analytic_line")

        self._delete_company_table("account_partial_reconcile")

        self._delete_company_table("account_payment_order")

        self._delete_company_table("account_payment_line")

        self._delete_aeat_349_partner_record_details()

        self._delete_company_table("account_move_line")

        self._delete_aeat_347_move_records()

        self._delete_company_table("account_move")

        self._delete_company_table("account_bank_statement")

        self._delete_company_table("account_asset_line")

        self._delete_company_table("account_asset")

        self._delete_company_table("account_check_deposit")

    def action_delete_analytic_operations(self):
        """
        Keep the old method name because the XML view already calls it.
        """
        self.ensure_one()

        self._delete_accounting_operations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # MRP
    # -------------------------------------------------------------------------

    def _delete_mrp_operations(self):
        self.ensure_one()

        if self._is_full_database_cleanup():
            self._delete_in_batches(
                "mrp_workorder",
                "TRUE",
                (),
            )
        else:
            self._delete_in_batches(
                "mrp_workorder",
                """
                production_id IN (
                    SELECT id
                    FROM mrp_production
                    WHERE company_id = ANY(%s)
                )
                """,
                (self.company_ids.ids,),
            )

        self._delete_company_table("mrp_production")

    def action_delete_mrp_operations(self):
        self.ensure_one()

        self._delete_mrp_operations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # Transport
    # -------------------------------------------------------------------------

    def _delete_transport_operations(self):
        self.ensure_one()

        self._delete_company_table("transport_carrier_lines_to_invoice")

    def action_delete_transport_operations(self):
        self.ensure_one()

        self._delete_transport_operations()

        self.env.cache.invalidate()

        return True

    # -------------------------------------------------------------------------
    # Sequences
    # -------------------------------------------------------------------------

    def action_delete_sequance_operations(self):
        """
        Keep the old misspelled method name because the current XML
        view already calls it.
        """
        self.ensure_one()

        sequences = self.env["ir.sequence"].search(
            [
                ("number_next_actual", "!=", 1),
                ("company_id", "in", self.company_ids.ids),
            ]
        )

        for sequence in sequences:
            sequence.number_next_actual = 1

        return True

    # -------------------------------------------------------------------------
    # ORM
    # -------------------------------------------------------------------------

    @api.model
    def create(self, values):
        values["name"] = _("Creation date: %s") % fields.Datetime.now()

        return super().create(values)

    def _delete_aeat_349_partner_record_details(self):
        self.ensure_one()

        self.env.cr.execute(
            """
            SELECT to_regclass(
                'public.l10n_es_aeat_mod349_partner_record_detail'
            )
            """
        )

        if not self.env.cr.fetchone()[0]:
            return 0

        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                "l10n_es_aeat_mod349_partner_record_detail",
                "TRUE",
                (),
            )

        return self._delete_in_batches(
            "l10n_es_aeat_mod349_partner_record_detail",
            """
            move_line_id IN (
                SELECT id
                FROM account_move_line
                WHERE company_id = ANY(%s)
            )
            """,
            (self.company_ids.ids,),
        )

    def _delete_aeat_347_move_records(self):
        self.ensure_one()

        self.env.cr.execute(
            """
            SELECT to_regclass(
                'public.l10n_es_aeat_mod347_move_record'
            )
            """
        )

        if not self.env.cr.fetchone()[0]:
            return 0

        if self._is_full_database_cleanup():
            return self._delete_in_batches(
                "l10n_es_aeat_mod347_move_record",
                "TRUE",
                (),
            )

        return self._delete_in_batches(
            "l10n_es_aeat_mod347_move_record",
            """
            move_id IN (
                SELECT id
                FROM account_move
                WHERE company_id = ANY(%s)
            )
            """,
            (self.company_ids.ids,),
        )
