# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
import threading
from datetime import datetime, time, timedelta

from odoo import _, api, fields, models, sql_db
from odoo.tools import sql
from odoo.tools.misc import split_every

try:
    from openupgradelib import openupgrade
except ImportError:
    openupgrade = None

_table_exists = openupgrade.table_exists if openupgrade else sql.table_exists
_column_exists = openupgrade.column_exists if openupgrade else sql.column_exists

_logger = logging.getLogger(__name__)


class CleaningDatabase(models.Model):
    _name = "cleaning.database"
    _inherit = ["mail.thread", "mail.activity.mixin", "utm.mixin"]
    _description = "Cleaning Database Operations"

    def _get_base_batch_size(self):
        return int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("cleaning_database.base_batch_size", default=15)
        )

    name = fields.Char(string="Description", copy=False)
    date_limit = fields.Date(
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        relation="rel_cleaning_database_company",
        column1="cleaning_database_id",
        column2="company_id",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        copy=False,
    )

    analytic_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )

    sale_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    sale_orders_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    purchase_lines_2delete = fields.Integer(compute="_compute_deleted", store=False)
    purchase_orders_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_move_lines_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_moves_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_pickings_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_inventory_move_lines_2delete = fields.Integer(
        compute="_compute_deleted", store=False
    )
    stock_inventory_moves_2delete = fields.Integer(
        compute="_compute_deleted", store=False
    )
    stock_inventories_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_quants_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_lots_2delete = fields.Integer(compute="_compute_deleted", store=False)
    stock_valuation_layers_2delete = fields.Integer(
        compute="_compute_deleted", store=False
    )

    partial_reconciles_2delete = fields.Integer(compute="_compute_deleted", store=False)
    payment_orders_2delete = fields.Integer(compute="_compute_deleted", store=False)
    payment_lines_2delete = fields.Integer(compute="_compute_deleted", store=False)
    account_move_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    account_moves_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    bank_statements_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    bank_statement_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    asset_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    assets_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    check_deposits_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    transport_carrier_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    mrp_workorders_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    mrp_productions_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_order_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_payments_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_orders_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_quotation_lines_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_quotations_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )
    pos_sessions_2delete = fields.Integer(
        compute="_compute_deleted",
        store=False,
    )

    is_clean = fields.Boolean(
        string="Is Clean",
        compute="_compute_is_clean",
        store=False,
    )

    delete_accounting = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_manufacturing = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_stock = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_sale = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_purchase = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_point_of_sale = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_others = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    delete_analytic_operations = fields.Boolean(
        string="Delete Analytic Lines",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_asset_operations = fields.Boolean(
        string="Delete Assets",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_payment_operations = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_bank_statement_operations = fields.Boolean(
        string="Delete Bank Statements",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_account_move_operations = fields.Boolean(
        string="Delete Journal Entries",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_stock_valuation_operations = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_stock_operations = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_inventory_operations = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_stock_production_lot = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_quant = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_pos_quotations = fields.Boolean(
        string="Delete Point of Sale Quotations",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_pos_orders = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_pos_sessions = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_transport_operations = fields.Boolean(
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    delete_check_deposit_operations = fields.Boolean(
        string="Delete Check Deposits",
        default=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.depends("date_limit", "company_ids")
    def _compute_deleted(self):
        for rc in self:
            for f in self._fields:
                if f.endswith("_2delete"):
                    rc[f] = 0
            if not rc.company_ids:
                continue
            # SALE ORDERS
            rc.sale_orders_2delete = rc._count_records("sale_order")
            rc.sale_lines_2delete = rc._count_records(
                "sale_order_line",
                extra_from="JOIN sale_order "
                "ON sale_order_line.order_id = sale_order.id",
                table_alias="sale_order",
            )
            # PURCHASE ORDERS
            rc.purchase_orders_2delete = rc._count_records("purchase_order")
            rc.purchase_lines_2delete = rc._count_records(
                "purchase_order_line",
                extra_from="JOIN purchase_order "
                "ON purchase_order_line.order_id = purchase_order.id",
                table_alias="purchase_order",
            )
            # PICKINGS
            picking_extra = (
                "JOIN stock_picking " "ON stock_move.picking_id = stock_picking.id"
            )
            rc.stock_move_lines_2delete = rc._count_records(
                "stock_move_line",
                extra_from=f"JOIN stock_move "
                f"ON stock_move_line.move_id = stock_move.id {picking_extra}",
                table_alias="stock_picking",
            )
            rc.stock_moves_2delete = rc._count_records(
                "stock_move",
                extra_from=picking_extra,
                table_alias="stock_picking",
            )
            rc.stock_pickings_2delete = rc._count_records("stock_picking")
            # INVENTORIES
            inventory_extra = (
                "JOIN stock_inventory "
                "ON stock_move.inventory_id = stock_inventory.id"
            )
            rc.stock_inventory_move_lines_2delete = rc._count_records(
                "stock_move_line",
                extra_from=f"JOIN stock_move "
                f"ON stock_move_line.move_id = stock_move.id {inventory_extra}",
                table_alias="stock_inventory",
            )
            rc.stock_inventory_moves_2delete = rc._count_records(
                "stock_move",
                extra_from=inventory_extra,
                table_alias="stock_inventory",
            )
            rc.stock_inventories_2delete = rc._count_records("stock_inventory")
            rc.stock_quants_2delete = rc._count_records("stock_quant")
            rc.stock_lots_2delete = rc._count_records("stock_production_lot")
            rc.stock_valuation_layers_2delete = rc._count_records(
                "stock_valuation_layer"
            )
            rc.analytic_lines_2delete = rc._count_records("account_analytic_line")
            rc.partial_reconciles_2delete = rc._count_records(
                "account_partial_reconcile"
            )
            # PAYMENT ORDERS
            rc.payment_orders_2delete = rc._count_records("account_payment_order")
            rc.payment_lines_2delete = rc._count_records(
                "account_payment_line",
                extra_from="JOIN account_payment_order "
                "ON account_payment_line.order_id = account_payment_order.id",
                table_alias="account_payment_order",
            )
            # ACCOUNT MOVES
            rc.account_move_lines_2delete = rc._count_records(
                "account_move_line",
                extra_from="JOIN account_move "
                "ON account_move_line.move_id = account_move.id",
                table_alias="account_move",
            )
            rc.account_moves_2delete = rc._count_records("account_move")
            # ACCOUNT BANK STATEMENT
            rc.bank_statements_2delete = rc._count_records("account_bank_statement")
            rc.bank_statement_lines_2delete = rc._count_records(
                "account_bank_statement_line",
                extra_from="JOIN account_bank_statement "
                "ON account_bank_statement_line.statement_id = "
                "account_bank_statement.id",
                table_alias="account_bank_statement",
            )
            # ACCOUNT ASSETS
            rc.asset_lines_2delete = rc._count_records(
                "account_asset_line",
                extra_from="JOIN account_asset "
                "ON account_asset_line.asset_id = account_asset.id",
                table_alias="account_asset",
            )
            rc.assets_2delete = rc._count_records("account_asset")
            rc.check_deposits_2delete = rc._count_records("account_check_deposit")
            rc.transport_carrier_lines_2delete = rc._count_records(
                "transport_carrier_lines_to_invoice"
            )
            # MANUFACTURING
            rc.mrp_workorders_2delete = rc._count_records(
                "mrp_workorder",
                extra_from="JOIN mrp_production "
                "ON mrp_workorder.production_id = mrp_production.id",
                table_alias="mrp_production",
            )
            rc.mrp_productions_2delete = rc._count_records("mrp_production")
            # POINT OF SALE SESSIONS
            pos_extra = "JOIN pos_config ON pos_session.config_id = pos_config.id"
            rc.pos_sessions_2delete = rc._count_records(
                "pos_session",
                extra_from=pos_extra,
                table_alias="pos_config",
            )
            # POINT OF SALE ORDERS
            pos_order_extra = (
                f"JOIN pos_session "
                f"ON pos_order.session_id = pos_session.id {pos_extra}"
            )
            rc.pos_orders_2delete = rc._count_records(
                "pos_order",
                extra_from=pos_order_extra,
                table_alias="pos_config",
            )
            rc.pos_order_lines_2delete = rc._count_records(
                "pos_order_line",
                extra_from=f"JOIN pos_order "
                f"ON pos_order_line.order_id = pos_order.id {pos_order_extra}",
                table_alias="pos_config",
            )
            rc.pos_payments_2delete = rc._count_records(
                "pos_payment",
                extra_from=f"JOIN pos_order "
                f"ON pos_payment.pos_order_id = pos_order.id {pos_order_extra}",
                table_alias="pos_config",
            )
            # POINT OF SALE QUOTATIONS
            pos_quotation_extra = (
                f"JOIN pos_session "
                f"ON pos_quotation.pos_session_id = pos_session.id {pos_extra}"
            )
            rc.pos_quotations_2delete = rc._count_records(
                "pos_quotation",
                extra_from=pos_quotation_extra,
                table_alias="pos_config",
            )
            pos_quotation_join = (
                "JOIN pos_quotation "
                "ON pos_quotation_line.quotation_id = pos_quotation.id"
            )
            rc.pos_quotation_lines_2delete = rc._count_records(
                "pos_quotation_line",
                extra_from=f"{pos_quotation_join} {pos_quotation_extra}",
                table_alias="pos_config",
            )

    def _logged_execute(self, query, params=None):
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        if openupgrade:
            try:
                openupgrade.logged_query(new_cr, query, params or ())
                new_cr.commit()  # pylint: disable=invalid-commit
                return new_cr.rowcount
            finally:
                new_cr.close()
        else:
            try:
                new_cr.execute(query, params or ())
                new_cr.commit()  # pylint: disable=invalid-commit
                return new_cr.rowcount
            finally:
                new_cr.close()

    def _build_where(self, table_alias="", extra_conditions="", date_limit=None):
        """Build WHERE clause and params for company + optional date_limit.
        Use table_alias to qualify columns when JOINs are involved.
        """
        prefix = f"{table_alias}." if table_alias else ""
        where = f"{prefix}company_id = ANY(%s)"
        params = [list(self.company_ids.ids)]
        date_limit = date_limit or self.date_limit
        if date_limit:
            where += f" AND {prefix}create_date <= %s"
            params.append(datetime.combine(date_limit, time.max))
        if extra_conditions:
            where += " AND (" + extra_conditions + ")"
        return where, params

    def _check_empty(self, table, extra_from="", table_alias="", date_limit=None):
        cr = self.env.cr
        empty = True
        if _table_exists(cr, table):
            where, params = self._build_where(table_alias, date_limit=date_limit)
            cr.execute(
                f"SELECT {table}.id FROM {table} {extra_from} WHERE {where} LIMIT 1",
                params,
            )
            empty = not bool(cr.fetchone())
        return empty

    def _count_records(self, table, extra_from="", table_alias="", date_limit=None):
        cr = self.env.cr
        count = 0
        if _table_exists(cr, table):
            where, params = self._build_where(table_alias, date_limit=date_limit)
            cr.execute(
                f"SELECT COUNT({table}.id) FROM {table} {extra_from} WHERE {where}",
                params,
            )
            count = cr.fetchone()[0]
        return count

    def _get_min_create_date(
        self, table, extra_from="", table_alias="", date_limit=None
    ):
        cr = self.env.cr
        min_date = False
        if _table_exists(cr, table):
            where, params = self._build_where(table_alias, date_limit=date_limit)
            cr.execute(
                f"SELECT MIN({table}.create_date) FROM {table} {extra_from} WHERE {where}",
                params,
            )
            min_date = cr.fetchone()[0]
        return datetime.combine(min_date, time.min) if min_date else False

    def _get_end_date(self):
        return (
            datetime.combine(self.date_limit, time.max)
            if self.date_limit
            else fields.Datetime.now()
        )

    @api.depends("date_limit", "company_ids")
    def _compute_is_clean(self):
        for record in self:
            record.is_clean = all(
                getattr(record, fname) == 0
                for fname in record._fields
                if fname.endswith("_2delete")
            )

    def _batch_delete(
        self, table, where, params, no_iter, extra_from="", batch_size=False
    ):
        """Delete rows in batches, committing after each batch.
        Prevents long table locks, statement timeouts, and WAL bloat.
        Uses CTE (WITH) for efficient batch selection.
        Returns total deleted rows.
        """
        if not batch_size:
            batch_size = self._get_base_batch_size()
        total = 0
        _logger.info("Delete from %s", table)
        while True:
            deleted = self._logged_execute(
                f"""WITH batch AS (
                        SELECT {table}.id
                        FROM {table} {extra_from}
                        WHERE {where}
                        LIMIT %s
                    )
                    DELETE FROM {table}
                    USING batch
                    WHERE {table}.id = batch.id""",
                params + [batch_size],
            )
            total += deleted
            _logger.info("Deleted %s rows from %s (total: %s)", deleted, table, total)
            if deleted < batch_size or no_iter:
                break
        if deleted < batch_size:
            self._vacuum_tables([table])
        return total

    def _batch_set_null(
        self,
        target_table,
        target_column,
        fk_column,
        source_table,
        where,
        params,
        extra_from="",
        batch_size=False,
    ):
        """Set a column to NULL in batches, committing after each batch.
        Batch selects IDs from source_table, then UPDATEs target_table
        where fk_column matches the batch IDs.
        Returns total updated rows.
        """
        if not batch_size:
            batch_size = self._get_base_batch_size()
        total = 0
        _logger.info("Set null %s.%s", target_table, target_column)
        updated = self._logged_execute(
            f"""WITH batch AS (
                    SELECT {source_table}.id
                    FROM {source_table} {extra_from}
                    WHERE {where}
                    LIMIT %s
                )
                UPDATE {target_table}
                SET {target_column} = NULL
                FROM batch
                WHERE {target_table}.{fk_column} = batch.id""",
            params + [batch_size],
        )
        total += updated
        return total

    def _vacuum_tables(self, tables):
        """VACUUM ANALYZE tables to reclaim disk space.
        Opens an autocommit connection to bypass Odoo's transaction block."""
        if not tables:
            return
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        new_cr._cnx.autocommit = True
        try:
            for table in tables:
                new_cr.execute("VACUUM ANALYZE %s" % table)
                _logger.info("VACUUM ANALYZE %s done", table)
        finally:
            new_cr.close()

    def _batch_delete_by_parent(
        self,
        parent_table,
        company_ids,
        current,
        next_day,
        child_deletes,
        no_iter=True,
        set_nulls=None,
    ):
        """Delete records in batches based on parent table IDs.

        Selects a batch of parent IDs, optionally NULLs FK references
        in related tables, deletes all child records linked to those
        parents, then deletes the parents themselves.
        Ensures batch consistency across all operations.

        Args:
            parent_table: Root table to batch by.
            company_ids: List of company IDs.
            current: Start datetime (inclusive).
            next_day: End datetime (exclusive).
            child_deletes: List of tuples (table_name, where_clause)
                where_clause uses %%s placeholder for parent IDs array.
            no_iter: If True, process only one batch.
            set_nulls: Optional list of tuples
                (target_table, target_column, fk_column) to NULL FK
                references before deleting.
        """
        batch_size = self._get_base_batch_size()
        total = 0
        while True:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            try:
                new_cr.execute(
                    f"SELECT id FROM {parent_table} "
                    "WHERE company_id = ANY(%s) "
                    "AND create_date >= %s "
                    "AND create_date < %s "
                    "LIMIT %s",
                    [company_ids, current, next_day, batch_size],
                )
                parent_ids = [row[0] for row in new_cr.fetchall()]
                new_cr.commit()
            finally:
                new_cr.close()
            if not parent_ids:
                break
            for target_table, target_column, fk_column in set_nulls or []:
                self._logged_execute(
                    f"UPDATE {target_table} "
                    f"SET {target_column} = NULL "
                    f"WHERE {fk_column} = ANY(%s)",
                    [parent_ids],
                )
            for table, where_clause in child_deletes:
                self._logged_execute(
                    f"DELETE FROM {table} WHERE {where_clause}",
                    [parent_ids],
                )
            self._logged_execute(
                f"DELETE FROM {parent_table} WHERE id = ANY(%s)",
                [parent_ids],
            )
            total += len(parent_ids)
            _logger.info(
                "Deleted %s %s records and related children (total: %s)",
                len(parent_ids),
                parent_table,
                total,
            )
            if len(parent_ids) < batch_size or no_iter:
                break
        if total:
            tables_to_vacuum = list({t for t, _ in child_deletes}) + [parent_table]
            self._vacuum_tables(tables_to_vacuum)
        return total

    # =================================================================
    #  Delete Stock Operations
    # =================================================================

    def _delete_stock_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        child_deletes = []
        if self.stock_move_lines_2delete > 0:
            child_deletes.append(
                (
                    "stock_move_line",
                    "move_id IN "
                    "(SELECT id FROM stock_move WHERE picking_id = ANY(%s))",
                )
            )
        if self.stock_moves_2delete > 0:
            child_deletes.append(("stock_move", "picking_id = ANY(%s)"))
        self._batch_delete_by_parent(
            "stock_picking",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
        )
        _logger.info("Deleted stock pickings up to %s", next_day)
        return next_day

    def button_delete_stock_operations(self):
        self.ensure_one()
        _logger.info("Delete Stock Operations Start")
        if self.stock_pickings_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_picking")
            if not min_date:
                _logger.info("No stock pickings to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_stock_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Stock Operations Done")
        self.action_check_and_mark_done()

    def action_delete_stock_operations(self):
        self.ensure_one()
        _logger.info("Delete Stock Operations Start")
        if self.stock_pickings_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_picking")
            if not min_date:
                _logger.info("No stock pickings to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_stock_operations(current, company_ids, no_iter=True)
        if self.stock_pickings_2delete:
            _logger.info("Delete Stock Operations Pending")
        else:
            _logger.info("Delete Stock Operations Done")
        self.action_check_and_mark_done()

    def _delete_inventory_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        child_deletes = [
            ("stock_inventory_line", "inventory_id = ANY(%s)"),
            (
                "stock_move_line",
                "move_id IN "
                "(SELECT id FROM stock_move WHERE inventory_id = ANY(%s))",
            ),
            ("stock_move", "inventory_id = ANY(%s)"),
        ]
        self._batch_delete_by_parent(
            "stock_inventory",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
        )
        _logger.info("Deleted stock inventories up to %s", next_day)
        return next_day

    def button_delete_inventory_operations(self):
        self.ensure_one()
        _logger.info("Delete Inventory Operations Start")
        if self.stock_inventories_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_inventory")
            if not min_date:
                _logger.info("No stock inventories to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_inventory_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Inventory Operations Done")
        self.action_check_and_mark_done()

    def action_delete_inventory_operations(self):
        self.ensure_one()
        _logger.info("Delete Inventory Operations Start")
        if self.stock_inventories_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_inventory")
            if not min_date:
                _logger.info("No stock inventories to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_inventory_operations(current, company_ids, no_iter=True)
        if self.stock_inventories_2delete:
            _logger.info("Delete Inventory Operations Pending")
        else:
            _logger.info("Delete Inventory Operations Done")
        self.action_check_and_mark_done()

    def _delete_quant(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where_move = (
            "stock_move.company_id = ANY(%s) "
            "AND stock_move.create_date >= %s "
            "AND stock_move.create_date < %s "
            "AND stock_move.inventory_id IS NULL "
            "AND stock_move.picking_id IS NULL"
        )
        params_move = [company_ids, current, next_day]
        self._batch_delete("stock_move", where_move, params_move, no_iter)
        where = (
            "stock_quant.company_id = ANY(%s) "
            "AND stock_quant.create_date >= %s "
            "AND stock_quant.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete("stock_quant", where, params, no_iter)
        _logger.info("Deleted stock quants up to %s", next_day)
        return next_day

    def button_delete_quant(self):
        self.ensure_one()
        _logger.info("Delete Quant Operations Start")
        if self.stock_quants_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_quant")
            if not min_date:
                _logger.info("No stock quants to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_quant(current, company_ids, no_iter=False)
        _logger.info("Delete Quant Operations Done")
        self.action_check_and_mark_done()

    def action_delete_quant(self):
        self.ensure_one()
        _logger.info("Delete Quant Operations Start")
        if self.stock_quants_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_quant")
            if not min_date:
                _logger.info("No stock quants to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_quant(current, company_ids, no_iter=True)
        if self.stock_quants_2delete:
            _logger.info("Delete Quant Operations Pending")
        else:
            _logger.info("Delete Quant Operations Done")
        self.action_check_and_mark_done()

    def _delete_stock_production_lot(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "stock_production_lot.company_id = ANY(%s) "
            "AND stock_production_lot.create_date >= %s "
            "AND stock_production_lot.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete("stock_production_lot", where, params, no_iter)
        _logger.info("Deleted stock production lots up to %s", next_day)
        return next_day

    def button_delete_stock_production_lot(self):
        self.ensure_one()
        _logger.info("Delete Stock Production Lot Operations Start")
        if self.stock_lots_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_production_lot")
            if not min_date:
                _logger.info("No stock production lots to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_stock_production_lot(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Stock Production Lot Operations Done")
        self.action_check_and_mark_done()

    def action_delete_stock_production_lot(self):
        self.ensure_one()
        _logger.info("Delete Stock Production Lot Operations Start")
        if self.stock_lots_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_production_lot")
            if not min_date:
                _logger.info("No stock production lots to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_stock_production_lot(current, company_ids, no_iter=True)
        if self.stock_lots_2delete:
            _logger.info("Delete Stock Production Lot Operations Pending")
        else:
            _logger.info("Delete Stock Production Lot Operations Done")
        self.action_check_and_mark_done()

    def _delete_stock_valuation_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "stock_valuation_layer.company_id = ANY(%s) "
            "AND stock_valuation_layer.create_date >= %s "
            "AND stock_valuation_layer.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete("stock_valuation_layer", where, params, no_iter)
        _logger.info("Deleted stock valuation layers up to %s", next_day)
        return next_day

    def button_delete_stock_valuation_operations(self):
        self.ensure_one()
        _logger.info("Delete Stock Valuation Operations Start")
        if self.stock_valuation_layers_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_valuation_layer")
            if not min_date:
                _logger.info("No stock valuation layers to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_stock_valuation_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Stock Valuation Operations Done")
        self.action_check_and_mark_done()

    def action_delete_stock_valuation_operations(self):
        self.ensure_one()
        _logger.info("Delete Stock Valuation Operations Start")
        if self.stock_valuation_layers_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("stock_valuation_layer")
            if not min_date:
                _logger.info("No stock valuation layers to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_stock_valuation_operations(
                    current, company_ids, no_iter=True
                )
        if self.stock_valuation_layers_2delete:
            _logger.info("Delete Stock Valuation Operations Pending")
        else:
            _logger.info("Delete Stock Valuation Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Delete Sale Orders
    # =================================================================

    def _delete_sale_orders(self, current, company_ids, no_iter=False):
        next_day = current + timedelta(days=1)
        child_deletes = [
            ("sale_order_line", "order_id = ANY(%s)"),
        ]
        self._batch_delete_by_parent(
            "sale_order",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
        )
        _logger.info("Deleted sale orders up to %s", next_day)
        return next_day

    def button_delete_sale_orders(self):
        self.ensure_one()
        _logger.info("Delete Sale Operations Start")
        if self.delete_sale:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("sale_order")
            if not min_date:
                _logger.info("No sale orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_sale_orders(current, company_ids)
        _logger.info("Delete Sale Operations Done")
        self.action_check_and_mark_done()

    def action_delete_sale_orders(self):
        self.ensure_one()
        _logger.info("Delete Sale Operations Start")
        if self.delete_sale:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("sale_order")
            if not min_date:
                _logger.info("No sale orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_sale_orders(current, company_ids, no_iter=True)
        if self.sale_orders_2delete:
            _logger.info("Delete Sale Operations Pending")
        else:
            _logger.info("Delete Sale Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Delete Purchase Orders
    # =================================================================

    def _delete_purchase_orders(self, current, company_ids, no_iter=False):
        next_day = current + timedelta(days=1)
        child_deletes = [
            ("purchase_order_line", "order_id = ANY(%s)"),
        ]
        self._batch_delete_by_parent(
            "purchase_order",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
        )
        _logger.info("Deleted purchases up to %s", next_day)
        return next_day

    def button_delete_purchase_operations(self):
        self.ensure_one()
        _logger.info("Delete Purchase Operations Start")
        if self.purchase_orders_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("purchase_order")
            if not min_date:
                _logger.info("No purchase orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_purchase_orders(current, company_ids)
        _logger.info("Delete Purchase Operations Done")
        self.action_check_and_mark_done()

    def action_delete_purchase_operations(self):
        self.ensure_one()
        _logger.info("Delete Purchase Operations Start")
        if self.purchase_orders_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("purchase_order")
            if not min_date:
                _logger.info("No purchase orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_purchase_orders(current, company_ids, no_iter=True)
        if self.purchase_orders_2delete:
            _logger.info("Delete Purchase Operations Pending")
        else:
            _logger.info("Delete Purchase Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Analytic / Accounting Operations
    # =================================================================

    def _delete_analytic_operations(self, current, company_ids, no_iter=False):
        next_day = current + timedelta(days=1)
        where = "company_id = ANY(%s) AND create_date >= %s AND create_date < %s"
        params = [company_ids, current, next_day]
        self._batch_delete("account_analytic_line", where, params, no_iter)
        _logger.info("Deleted analytic records up to %s", next_day)
        return next_day

    def button_delete_analytic_operations(self):
        self.ensure_one()
        _logger.info("Delete Analytic Operations Start")
        if self.analytic_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_analytic_line")
            if not min_date:
                _logger.info("No analytic records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_analytic_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Analytic Operations Done")
        self.action_check_and_mark_done()

    def action_delete_analytic_operations(self):
        self.ensure_one()
        _logger.info("Delete Analytic Operations Start")
        if self.analytic_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_analytic_line")
            if not min_date:
                _logger.info("No analytic records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_analytic_operations(current, company_ids, no_iter=True)
        if self.analytic_lines_2delete:
            _logger.info("Delete Analytic Operations Pending")
        else:
            _logger.info("Delete Analytic Operations Done")
        self.action_check_and_mark_done()

    def _delete_account_move_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "account_move.company_id = ANY(%s) "
            "AND account_move.create_date >= %s "
            "AND account_move.create_date < %s"
        )
        extra_from = (
            "JOIN account_move " "ON account_move_line.move_id = account_move.id"
        )
        params = [company_ids, current, next_day]
        self._batch_delete(
            "account_partial_reconcile",
            where,
            params,
            no_iter,
            extra_from=f"JOIN account_move_line "
            f"ON account_partial_reconcile.credit_move_id = account_move_line.id {extra_from}",
        )
        self._batch_delete(
            "account_partial_reconcile",
            where,
            params,
            no_iter,
            extra_from=f"JOIN account_move_line "
            f"ON account_partial_reconcile.debit_move_id = account_move_line.id {extra_from}",
        )
        self._batch_delete(
            "account_move_line",
            where,
            params,
            no_iter,
            extra_from=extra_from,
        )
        self._batch_delete("account_move", where, params, no_iter)
        _logger.info("Deleted account move records up to %s", next_day)
        return next_day

    def button_delete_account_move_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Moves Operations Start")
        if self.account_moves_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_move")
            if not min_date:
                _logger.info("No account moves records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_account_move_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Account Move Operations Done")
        self.action_check_and_mark_done()

    def action_delete_account_move_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Moves Operations Start")
        if self.account_moves_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_move")
            if not min_date:
                _logger.info("No account moves records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_account_move_operations(current, company_ids, no_iter=True)
        if self.account_moves_2delete:
            _logger.info("Delete Account Moves Operations Pending")
        else:
            _logger.info("Delete Account Move Operations Done")
        self.action_check_and_mark_done()

    def _delete_asset_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "account_asset.company_id = ANY(%s) "
            "AND account_asset.create_date >= %s "
            "AND account_asset.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete(
            "account_asset_line",
            where,
            params,
            no_iter,
            extra_from="JOIN account_asset "
            "ON account_asset_line.asset_id = account_asset.id",
        )
        self._batch_delete("account_asset", where, params, no_iter)
        _logger.info("Deleted account asset records up to %s", next_day)
        return next_day

    def button_delete_asset_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Asset Operations Start")
        if self.assets_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_asset")
            if not min_date:
                _logger.info("No account asset records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_asset_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Account Asset Operations Done")
        self.action_check_and_mark_done()

    def action_delete_asset_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Asset Operations Start")
        if self.assets_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_asset")
            if not min_date:
                _logger.info("No account asset records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_asset_operations(current, company_ids, no_iter=True)
        if self.assets_2delete:
            _logger.info("Delete Account Asset Operations Pending")
        else:
            _logger.info("Delete Account Asset Operations Done")
        self.action_check_and_mark_done()

    def _delete_payment_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "account_payment_order.company_id = ANY(%s) "
            "AND account_payment_order.create_date >= %s "
            "AND account_payment_order.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete(
            "account_payment_line",
            where,
            params,
            no_iter,
            extra_from="JOIN account_payment_order "
            "ON account_payment_line.order_id = account_payment_order.id",
        )
        self._batch_delete("account_payment_order", where, params, no_iter)
        _logger.info("Deleted account payment records up to %s", next_day)
        return next_day

    def button_delete_payment_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Payment Operations Start")
        if self.payment_orders_2delete > 0 or self.payment_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_payment_order")
            if not min_date:
                _logger.info("No account payment records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_payment_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Account Payment Operations Done")
        self.action_check_and_mark_done()

    def action_delete_payment_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Payment Operations Start")
        if self.payment_orders_2delete > 0 or self.payment_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_payment_order")
            if not min_date:
                _logger.info("No account payment records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_payment_operations(current, company_ids, no_iter=True)
        if self.payment_orders_2delete or self.payment_lines_2delete:
            _logger.info("Delete Account Payment Operations Pending")
        else:
            _logger.info("Delete Account Payment Operations Done")
        self.action_check_and_mark_done()

    def _delete_bank_statement_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "account_bank_statement.company_id = ANY(%s) "
            "AND account_bank_statement.create_date >= %s "
            "AND account_bank_statement.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete(
            "account_bank_statement_line",
            where,
            params,
            no_iter,
            extra_from="JOIN account_bank_statement "
            "ON account_bank_statement_line.statement_id = account_bank_statement.id",
        )
        self._batch_delete("account_bank_statement", where, params, no_iter)
        _logger.info("Deleted bank statements records up to %s", next_day)
        return next_day

    def button_delete_bank_statement_operations(self):
        self.ensure_one()
        _logger.info("Delete Bank Statement Operations Start")
        if self.bank_statements_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_bank_statement")
            if not min_date:
                _logger.info("No bank statements records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_bank_statement_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Bank Statement Operations Done")
        self.action_check_and_mark_done()

    def action_delete_bank_statement_operations(self):
        self.ensure_one()
        _logger.info("Delete Bank Statement Operations Start")
        if self.bank_statements_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_bank_statement")
            if not min_date:
                _logger.info("No bank statements records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_bank_statement_operations(
                    current, company_ids, no_iter=True
                )
        if self.bank_statements_2delete:
            _logger.info("Delete Bank Statement Operations Pending")
        else:
            _logger.info("Delete Bank Statement Operations Done")
        self.action_check_and_mark_done()

    # def action_delete_partial_reconcile_operations(self):
    #     self.ensure_one()
    #     _logger.info("Delete Accounting Operations Start")
    #     self.env.cr
    #     company_ids = list(self.company_ids.ids)
    #     min_date = self._get_min_create_date("account_partial_reconcile")
    #     if not min_date:
    #         _logger.info("No accounting records to delete")
    #         self.action_check_and_mark_done()
    #         return
    #     end_date = self._get_end_date()
    #     current = datetime.combine(min_date, time.min)
    #     if current <= end_date:
    #         next_day = current + timedelta(days=1)
    #         where = "company_id = ANY(%s) AND create_date >= %s AND create_date < %s"
    #         params = [company_ids, current, next_day]
    #         self._batch_delete("account_partial_reconcile", where, params, True)
    #         _logger.info("Deleted accounting records up to %s", next_day)
    #         current = next_day
    #     _logger.info("Delete Accounting Operations Done")
    #     self.action_check_and_mark_done()

    def _delete_check_deposit_operations(self, current, company_ids, no_iter=True):
        cr = self.env.cr
        next_day = current + timedelta(days=1)
        where = "company_id = ANY(%s) AND create_date >= %s AND create_date < %s"
        params = [company_ids, current, next_day]
        if _table_exists(cr, "account_check_deposit"):
            self._batch_delete("account_check_deposit", where, params, no_iter)
        _logger.info("Deleted account check deposits up to %s", next_day)
        return next_day

    def button_delete_check_deposit_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Check Deposit Start")
        company_ids = list(self.company_ids.ids)
        min_date = self._get_min_create_date("account_check_deposit")
        if not min_date:
            _logger.info("No account check deposits to delete")
            self.action_check_and_mark_done()
            return
        end_date = self._get_end_date()
        current = datetime.combine(min_date, time.min)
        while current <= end_date:
            current = self._delete_check_deposit_operations(
                current, company_ids, no_iter=False
            )
        _logger.info("Delete Account Check Deposit Done")
        self.action_check_and_mark_done()

    def action_delete_check_deposit_operations(self):
        self.ensure_one()
        _logger.info("Delete Account Check Deposit Start")
        if self.check_deposits_2delete:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("account_check_deposit")
            if not min_date:
                _logger.info("No accounting records to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_check_deposit_operations(
                    current, company_ids, no_iter=True
                )
        if self.check_deposits_2delete:
            _logger.info("Delete Account Check Deposit Pending")
        else:
            _logger.info("Delete Account Check Deposit Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Transport Operations
    # =================================================================

    def _delete_transport_operations(self, current, company_ids, no_iter=True):
        next_day = current + timedelta(days=1)
        where = (
            "transport_carrier_lines_to_invoice.company_id = ANY(%s) "
            "AND transport_carrier_lines_to_invoice.create_date >= %s "
            "AND transport_carrier_lines_to_invoice.create_date < %s"
        )
        params = [company_ids, current, next_day]
        self._batch_delete("transport_carrier_lines_to_invoice", where, params, no_iter)
        _logger.info("Deleted transport carrier lines up to %s", next_day)
        return next_day

    def button_delete_transport_operations(self):
        self.ensure_one()
        _logger.info("Delete Transport Operations Start")
        if self.transport_carrier_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("transport_carrier_lines_to_invoice")
            if not min_date:
                _logger.info("No transport carrier lines to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_transport_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete Transport Operations Done")
        self.action_check_and_mark_done()

    def action_delete_transport_operations(self):
        self.ensure_one()
        _logger.info("Delete Transport Operations Start")
        if self.transport_carrier_lines_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("transport_carrier_lines_to_invoice")
            if not min_date:
                _logger.info("No transport carrier lines to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_transport_operations(current, company_ids, no_iter=True)
        if self.transport_carrier_lines_2delete:
            _logger.info("Delete Transport Operations Pending")
        else:
            _logger.info("Delete Transport Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  MRP Operations
    # =================================================================

    def _delete_mrp_operations(self, current, company_ids, no_iter=True):
        cr = self.env.cr
        next_day = current + timedelta(days=1)
        where = (
            "mrp_production.company_id = ANY(%s) "
            "AND mrp_production.create_date >= %s "
            "AND mrp_production.create_date < %s"
        )
        params = [company_ids, current, next_day]
        production_extra = (
            "JOIN mrp_production " "ON mrp_workorder.production_id = mrp_production.id "
        )
        workorder_extra = (
            f"JOIN mrp_workorder "
            f"ON stock_move.workorder_id = mrp_workorder.id {production_extra}"
        )
        if _column_exists(cr, "stock_move_line", "workorder_id"):
            self._batch_delete(
                "stock_move_line",
                where,
                params,
                no_iter,
                extra_from=f"JOIN stock_move "
                f"ON stock_move_line.move_id = stock_move.id {workorder_extra}",
            )
            if _column_exists(cr, "stock_move", "workorder_id"):
                self._batch_delete(
                    "stock_move",
                    where,
                    params,
                    no_iter,
                    extra_from=workorder_extra,
                )
        if self.mrp_workorders_2delete > 0:
            self._batch_delete(
                "mrp_workorder",
                where,
                params,
                no_iter,
                extra_from=production_extra,
            )
        if _column_exists(cr, "stock_move_line", "production_id"):
            self._batch_delete(
                "stock_move_line",
                where,
                params,
                no_iter,
                extra_from=f"JOIN stock_move "
                f"ON stock_move_line.move_id = stock_move.id {production_extra}",
            )
            if _column_exists(cr, "stock_move", "production_id"):
                self._batch_delete(
                    "stock_move",
                    where,
                    params,
                    no_iter,
                    extra_from=production_extra,
                )
        self._batch_delete("mrp_production", where, params, no_iter)
        _logger.info("Deleted MRP productions up to %s", next_day)
        return next_day

    def button_delete_mrp_operations(self):
        self.ensure_one()
        _logger.info("Delete MRP Operations Start")
        if self.mrp_productions_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("mrp_production")
            if not min_date:
                _logger.info("No MRP productions to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_mrp_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete MRP Operations Done")
        self.action_check_and_mark_done()

    def action_delete_mrp_operations(self):
        self.ensure_one()
        _logger.info("Delete MRP Operations Start")
        if self.mrp_productions_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("mrp_production")
            if not min_date:
                _logger.info("No MRP productions to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_mrp_operations(current, company_ids, no_iter=True)
        if self.mrp_productions_2delete:
            _logger.info("Delete MRP Operations Pending")
        else:
            _logger.info("Delete MRP Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Delete Point of Sale
    # =================================================================

    def _delete_pos_orders(self, current, company_ids, no_iter=False):
        cr = self.env.cr
        next_day = current + timedelta(days=1)
        set_nulls = [
            ("stock_move", "pos_order_id", "pos_order_id"),
            ("stock_picking", "pos_order_id", "pos_order_id"),
            ("account_bank_statement_line", "pos_statement_id", "pos_statement_id"),
        ]
        if _table_exists(cr, "tbai_invoice") and _column_exists(
            cr, "tbai_invoice", "pos_order_id"
        ):
            set_nulls.append(("tbai_invoice", "pos_order_id", "pos_order_id"))
        child_deletes = [
            ("pos_order_line", "order_id = ANY(%s)"),
            ("pos_payment", "pos_order_id = ANY(%s)"),
        ]
        self._batch_delete_by_parent(
            "pos_order",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
            set_nulls=set_nulls,
        )
        _logger.info("Deleted POS operations up to %s", next_day)
        return next_day

    def button_delete_pos_order(self):
        self.ensure_one()
        if self.pos_orders_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("pos_order")
            if not min_date:
                _logger.info("No POS orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_pos_orders(current, company_ids)
        _logger.info("Delete PoS Operations Done")
        self.action_check_and_mark_done()

    def action_delete_pos_orders(self):
        self.ensure_one()
        _logger.info("Delete POS Operations Start")
        if self.pos_orders_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("pos_order")
            if not min_date:
                _logger.info("No POS orders to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_pos_orders(current, company_ids, no_iter=True)
        if self.pos_orders_2delete == 0:
            _logger.info("Delete PoS Operations Done")
        else:
            _logger.info("Delete PoS Operations Not Finished")
        self.action_check_and_mark_done()

    def _delete_pos_quotations(self, current, company_ids, no_iter=False):
        cr = self.env.cr
        next_day = current + timedelta(days=1)
        set_nulls = [
            ("stock_picking", "pos_quotation_id", "pos_quotation_id"),
        ]
        if _table_exists(cr, "tbai_invoice") and _column_exists(
            cr, "tbai_invoice", "pos_order_quotation_id"
        ):
            set_nulls.append(
                ("tbai_invoice", "pos_order_quotation_id", "pos_order_quotation_id")
            )
        child_deletes = [
            ("pos_quotation_line", "quotation_id = ANY(%s)"),
        ]
        self._batch_delete_by_parent(
            "pos_quotation",
            company_ids,
            current,
            next_day,
            child_deletes,
            no_iter,
            set_nulls=set_nulls,
        )
        _logger.info("Deleted POS quotations up to %s", next_day)
        return next_day

    def button_delete_pos_quotation_operations(self):
        self.ensure_one()
        if self.pos_quotations_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("pos_quotation")
            if not min_date:
                _logger.info("No POS quotations to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_pos_quotations(current, company_ids)
        _logger.info("Delete PoS Operations Done")
        self.action_check_and_mark_done()

    def action_delete_pos_quotation_operations(self):
        self.ensure_one()
        _logger.info("Delete POS Quotation Operations Start")
        if self.pos_quotations_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date("pos_quotation")
            if not min_date:
                _logger.info("No POS quotations to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_pos_quotations(current, company_ids, no_iter=True)
        if self.pos_quotations_2delete:
            _logger.info("Delete POS Quotation Operations Pending")
        else:
            _logger.info("Delete PoS Quotation Operations Done")
        self.action_check_and_mark_done()

    def _delete_pos_session_operations(self, current, company_ids, no_iter=False):
        cr = self.env.cr
        next_day = current + timedelta(days=1)
        where = (
            "pos_config.company_id = ANY(%s) "
            "AND pos_session.create_date >= %s "
            "AND pos_session.create_date < %s"
        )
        params = [company_ids, current, next_day]
        extra_from = "JOIN pos_config ON pos_session.config_id = pos_config.id"
        self._batch_set_null(
            "pos_order",
            "session_id",
            "session_id",
            "pos_session",
            where,
            params,
            extra_from=extra_from,
        )
        self._batch_set_null(
            "account_bank_statement",
            "pos_session_id",
            "pos_session_id",
            "pos_session",
            where,
            params,
            extra_from=extra_from,
        )
        if _column_exists(cr, "stock_picking", "pos_session_id"):
            self._batch_set_null(
                "stock_picking",
                "pos_session_id",
                "pos_session_id",
                "pos_session",
                where,
                params,
                extra_from=extra_from,
            )
        if (
            self._count_records(
                "pos_session",
                extra_from=extra_from,
                table_alias="pos_config",
                date_limit=next_day,
            )
            > 0
        ):
            self._batch_delete(
                "pos_session",
                where,
                params,
                no_iter,
                extra_from=extra_from,
            )
        _logger.info("Deleted POS sessions up to %s", next_day)
        return next_day

    def button_delete_pos_session_operations(self):
        self.ensure_one()
        _logger.info("Delete POS Session Operations Start")
        if self.pos_quotations_2delete > 0 or self.pos_orders_2delete > 0:
            _logger.warning("PoS Sessions can't be deleted")
            return
        if self.pos_sessions_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date(
                "pos_session",
                extra_from="JOIN pos_config "
                "ON pos_session.config_id = pos_config.id",
                table_alias="pos_config",
            )
            if not min_date:
                _logger.info("No POS sessions to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            while current <= end_date:
                current = self._delete_pos_session_operations(
                    current, company_ids, no_iter=False
                )
        _logger.info("Delete POS Session Operations Done")
        self.action_check_and_mark_done()

    def action_delete_pos_session_operations(self):
        self.ensure_one()
        _logger.info("Delete POS Session Operations Start")
        if self.pos_quotations_2delete > 0 or self.pos_orders_2delete > 0:
            _logger.warning("PoS Sessions can't be deleted")
            return
        if self.pos_sessions_2delete > 0:
            company_ids = list(self.company_ids.ids)
            min_date = self._get_min_create_date(
                "pos_session",
                extra_from="JOIN pos_config "
                "ON pos_session.config_id = pos_config.id",
                table_alias="pos_config",
            )
            if not min_date:
                _logger.info("No POS sessions to delete")
                self.action_check_and_mark_done()
                return
            end_date = self._get_end_date()
            current = datetime.combine(min_date, time.min)
            if current <= end_date:
                self._delete_pos_session_operations(current, company_ids, no_iter=True)
        if self.pos_sessions_2delete:
            _logger.info("Delete POS Session Operations Pending")
        else:
            _logger.info("Delete POS Session Operations Done")
        self.action_check_and_mark_done()

    # =================================================================
    #  Sequences
    # =================================================================

    def action_restart_sequences(self):
        self.ensure_one()
        sequences = self.env["ir.sequence"].search(
            [
                ("number_next_actual", "!=", 1),
                ("company_id", "in", self.company_ids.ids),
            ]
        )
        for line in sequences:
            line.number_next_actual = 1
        _logger.info("Reset Sequences Done")

    # =================================================================
    #  Lifecycle
    # =================================================================

    def button_schedule(self):
        records = self.filtered(lambda r: r.state == "draft")
        records.write({"state": "scheduled"})
        for record in records:
            record.message_post(body=_("Cleaning has been scheduled"))

    def _check_delete_analytic(self):
        self.ensure_one()
        if self.analytic_lines_2delete == 0:
            self.delete_analytic_operations = False

    def _check_accounting(self):
        self.ensure_one()
        # self.invalidate_cache()

        if (
            not self.delete_analytic_operations
            and not self.delete_account_move_operations
            and not self.delete_asset_operations
            and not self.delete_payment_operations
            and not self.delete_bank_statement_operations
            and not self.delete_check_deposit_operations
        ):
            self.delete_accounting = False

    def _check_sale_deleted(self):
        self.ensure_one()
        if self.sale_orders_2delete == 0 and self.sale_lines_2delete == 0:
            self.delete_sale = False

    def action_check_and_mark_done(self):
        self.ensure_one()

        self._check_delete_analytic()
        if (
            self.partial_reconciles_2delete == 0
            and self.account_move_lines_2delete == 0
            and self.account_moves_2delete == 0
        ):
            self.delete_account_move_operations = False
        if self.assets_2delete == 0 and self.asset_lines_2delete == 0:
            self.delete_asset_operations = False
        if self.payment_orders_2delete == 0 and self.payment_lines_2delete == 0:
            self.delete_payment_operations = False
        if self.bank_statements_2delete == 0 and self.bank_statement_lines_2delete == 0:
            self.delete_bank_statement_operations = False
        if self.check_deposits_2delete == 0:
            self.delete_check_deposit_operations = False

        self._check_accounting()

        if self.stock_valuation_layers_2delete == 0:
            self.delete_stock_valuation_operations = False
        if (
            self.stock_move_lines_2delete == 0
            and self.stock_moves_2delete == 0
            and self.stock_pickings_2delete == 0
        ):
            self.delete_stock_operations = False
        if (
            self.stock_inventory_move_lines_2delete == 0
            and self.stock_inventory_moves_2delete == 0
            and self.stock_inventories_2delete == 0
        ):
            self.delete_inventory_operations = False
        if self.stock_lots_2delete == 0:
            self.delete_stock_production_lot = False
        if self.stock_quants_2delete == 0:
            self.delete_quant = False

        if (
            self.pos_order_lines_2delete == 0
            and self.pos_payments_2delete == 0
            and self.pos_orders_2delete == 0
        ):
            self.delete_pos_orders = False
        if self.pos_quotation_lines_2delete == 0 and self.pos_quotations_2delete == 0:
            self.delete_pos_quotations = False
        if self.pos_sessions_2delete == 0:
            self.delete_pos_sessions = False

        if self.transport_carrier_lines_2delete == 0:
            self.delete_transport_operations = False

        if self.mrp_productions_2delete == 0 and self.mrp_workorders_2delete == 0:
            self.delete_manufacturing = False

        if (
            not self.delete_stock_valuation_operations
            and not self.delete_stock_operations
            and not self.delete_inventory_operations
            and not self.delete_stock_production_lot
            and not self.delete_quant
        ):
            self.delete_stock = False

        if self.sale_orders_2delete == 0:
            self.delete_sale = False

        if self.purchase_orders_2delete == 0 and self.purchase_lines_2delete == 0:
            self.delete_purchase = False

        if (
            not self.delete_pos_quotations
            and not self.delete_pos_orders
            and not self.delete_pos_sessions
        ):
            self.delete_point_of_sale = False

        if not self.delete_transport_operations:
            self.delete_others = False

        if (
            not self.delete_accounting
            and not self.delete_manufacturing
            and not self.delete_stock
            and not self.delete_sale
            and not self.delete_purchase
            and not self.delete_point_of_sale
            and not self.delete_others
            and self.state != "done"
        ):
            self.state = "done"
            self.message_post(body=_("Cleaning has been completed"))

    def action_full_delete(self):
        self.ensure_one()
        self.action_check_and_mark_done()
        if self.delete_accounting:
            if self.delete_analytic_operations:
                self.action_delete_analytic_operations()
            elif self.delete_asset_operations:
                self.action_delete_asset_operations()
            elif self.delete_bank_statement_operations:
                self.action_delete_bank_statement_operations()
            elif self.delete_check_deposit_operations:
                self.action_delete_check_deposit_operations()
            elif self.delete_account_move_operations:
                self.action_delete_account_move_operations()
        elif self.delete_manufacturing:
            self.action_delete_mrp_operations()
        elif self.delete_stock:
            if self.delete_stock_operations:
                self.action_delete_stock_operations()
            elif self.delete_inventory_operations:
                self.action_delete_inventory_operations()
            elif self.delete_stock_production_lot:
                self.action_delete_stock_production_lot()
            elif self.delete_quant:
                self.action_delete_quant()
            elif self.delete_stock_valuation_operations:
                self.action_delete_stock_valuation_operations()
        elif self.delete_sale:
            self.action_delete_sale_orders()
        elif self.delete_purchase:
            self.action_delete_purchase_operations()
        elif self.delete_point_of_sale:
            if self.delete_pos_quotations:
                self.action_delete_pos_quotation_operations()
            elif self.delete_pos_orders:
                self.action_delete_pos_orders()
            elif self.delete_pos_sessions:
                self.action_delete_pos_session_operations()
        elif self.delete_others:
            if self.delete_transport_operations:
                self.action_delete_transport_operations()

    def cron_action_full_delete(self, split_size=100, automatic=False):
        """Refresh action. Called by cronjob."""
        auto_commit = not getattr(threading.current_thread(), "testing", False)
        cleaning_ids = self.search(
            [
                ("state", "=", "scheduled"),
            ]
        ).ids
        i = 0
        j = len(cleaning_ids)
        for cleaning_chunk_ids in split_every(split_size, cleaning_ids):
            for cleaning in self.browse(cleaning_chunk_ids).exists():
                try:
                    i += 1
                    _logger.info(
                        "Cleaning: {}. ({}/{})".format(cleaning.display_name, i, j)
                    )
                    if automatic:
                        with self.env.cr.savepoint():
                            cleaning.action_full_delete()
                    else:
                        cleaning.action_full_delete()
                except Exception:
                    _logger.exception("Fail to clean: {}".format(cleaning.display_name))
                    if not automatic:
                        raise
            if auto_commit:
                self._cr.commit()  # pylint: disable=invalid-commit
        return True

    @api.model
    def create(self, values):
        name = _("Creation date: {}".format(fields.Datetime.now()))
        if isinstance(values, list):
            for vals in values:
                vals["name"] = name
        else:
            values["name"] = name
        return super().create(values)
