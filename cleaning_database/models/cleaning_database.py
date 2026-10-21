# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models
from odoo.tools import sql

_logger = logging.getLogger(__name__)


class CleaningDatabase(models.Model):
    _name = "cleaning.database"
    _description = "Cleaning Database Operations"

    name = fields.Char(string="Description", copy=False)
    date_limit = fields.Datetime(copy=False)
    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        relation="rel_cleaning_database_company",
        column1="cleaning_database_id",
        column2="company_id",
        required=True,
    )

    def action_delete_stock_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)
        _logger.info("Delete stock_move_line table.")
        self.env.cr.execute(
            f"""DELETE FROM stock_move_line
                    WHERE picking_id IS NOT NULL AND
                    company_id in %s {extended_where_clause}""",
            where_params,
        )
        _logger.info("Delete stock_move table.")
        self.env.cr.execute(
            f"""DELETE FROM stock_move
                    WHERE picking_id IS NOT NULL AND
                    company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        _logger.info("Delete stock_picking table.")
        self.env.cr.execute(
            f"""DELETE FROM stock_picking
                    WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        _logger.info("Delete Stock Operations Done")

    def action_delete_inventory_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)
        self.env.cr.execute(
            f"""DELETE FROM stock_inventory_line
                WHERE inventory_id IN (
                    SELECT id FROM stock_inventory
                    WHERE company_id in %s {extended_where_clause})""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM stock_move_line
                    WHERE move_id IN (SELECT id FROM stock_move
                        WHERE inventory_id IN (
                            SELECT id FROM stock_inventory
                            WHERE company_id in %s {extended_where_clause}))""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM stock_move
                        WHERE inventory_id IN (
                            SELECT id FROM stock_inventory
                            WHERE company_id in %s {extended_where_clause})""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM stock_inventory
                    WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        _logger.info("Delete Stock Operations Done")

    def action_delete_quant(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        self.env.cr.execute(
            f"""DELETE FROM stock_move
                WHERE inventory_id IS Null AND picking_id IS Null
                AND company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.execute(
            f"""DELETE FROM stock_quant
                WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        # self.env.cr.execute(
        #     "DELETE FROM stock_quant "
        #     "WHERE company_id in %s OR lot_id in (select l.id "
        #     "                      from   stock_production_lot as l"
        #     "                      where  l.id = stock_quant.lot_id "
        #     "                        and  l.company_id in %s)",
        #     [tuple(self.company_ids.ids), tuple(self.company_ids.ids)],
        # )

    def action_delete_stock_production_lot(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        self.env.cr.execute(
            f"""DELETE FROM stock_production_lot
                   WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )

    def action_delete_stock_valuation_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        self.env.cr.execute(
            f"""DELETE FROM stock_valuation_layer
                   WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )

    def action_delete_sale_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        self.env.cr.execute(
            f"""DELETE FROM sale_order_line
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.execute(
            f"""DELETE FROM sale_order
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )

    def action_delete_purchase_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        _logger.info("Delete purchase_order_line")
        self.env.cr.execute(
            f"""DELETE FROM purchase_order_line
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        _logger.info("Delete purchase_order")
        self.env.cr.execute(
            f"""DELETE FROM purchase_order
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        _logger.info("Delete Purchase Operations Done")

    def action_delete_analytic_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)

        self.env.cr.execute(
            f"""DELETE FROM account_analytic_line
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM account_partial_reconcile
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM account_payment_order
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM account_payment_line
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM account_move_line
            WHERE move_id IN (
                SELECT id FROM account_move
                WHERE company_id in %s {extended_where_clause})""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM account_move
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        if sql.table_exists(self.env.cr, "account_bank_statement"):
            self.env.cr.execute(
                "DELETE FROM account_bank_statement WHERE company_id in %s",
                [tuple(self.company_ids.ids)],
            )
        self.env.cr.execute(
            f"""DELETE FROM account_move
            WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        self.env.cr.commit()  # pylint: disable=E8102
        if sql.table_exists(self.env.cr, "account_asset_line"):
            self.env.cr.execute(
                f"""DELETE FROM account_asset_line
                WHERE company_id in %s {extended_where_clause}""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
        if sql.table_exists(self.env.cr, "account_asset"):
            self.env.cr.execute(
                f"""DELETE FROM account_asset
                WHERE company_id in %s {extended_where_clause}""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
        if sql.table_exists(self.env.cr, "account_check_deposit"):
            self.env.cr.execute(
                f"""DELETE FROM account_check_deposit
                WHERE company_id in %s {extended_where_clause}""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102

    def action_delete_transport_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)
        if sql.table_exists(self.env.cr, "transport_carrier_lines_to_invoice"):
            self.env.cr.execute(
                f"""DELETE FROM transport_carrier_lines_to_invoice
                            WHERE company_id in %s {extended_where_clause}""",
                where_params,
            )

    def action_delete_mrp_operations(self):
        extended_where_clause = ""
        where_params = [tuple(self.company_ids.ids)]
        if self.date_limit:
            extended_where_clause = "AND create_date <= %s"
            where_params.append(self.date_limit)
        if sql.column_exists(self.env.cr, "stock_move_line", "workorder_id"):
            self.env.cr.execute(
                f"""DELETE FROM stock_move_line
                        WHERE workorder_id IS NOT NULL AND
                        company_id in %s {extended_where_clause}""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
            if sql.column_exists(self.env.cr, "stock_move", "workorder_id"):
                self.env.cr.execute(
                    f"""DELETE FROM stock_move
                                    WHERE workorder_id IS NOT NULL AND
                                    company_id in %s {extended_where_clause}""",
                    where_params,
                )
            self.env.cr.execute(
                f"""DELETE FROM mrp_workorder AS w
                    WHERE production_id IN (
                        SELECT p.id FROM mrp_production AS p
                        WHERE p.id = w.production_id
                        AND company_id in %s {extended_where_clause})""",
                where_params,
            )
        self.env.cr.commit()  # pylint: disable=E8102
        if sql.column_exists(self.env.cr, "stock_move_line", "production_id"):
            self.env.cr.execute(
                f"""DELETE FROM stock_move_line
                    WHERE production_id IS NOT NULL
                      AND company_id in %s {extended_where_clause}""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
        self.env.cr.execute(
            f"""DELETE FROM mrp_production
                WHERE company_id in %s {extended_where_clause}""",
            where_params,
        )
        _logger.info("Delete production operations DONE")

    def action_delete_pos_operations(self):
        if sql.table_exists(self.env.cr, "pos_config"):
            extended_where_clause = ""
            where_params = [tuple(self.company_ids.ids)]
            if self.date_limit:
                extended_where_clause = "AND create_date <= %s"
                where_params.append(self.date_limit)

            self.env.cr.execute(
                f"""DELETE FROM pos_order_line
                    WHERE order_id IN (
                        SELECT p.id FROM pos_order p
                        WHERE company_id in %s {extended_where_clause})""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
            self.env.cr.execute(
                f"""DELETE FROM pos_payment
                    WHERE pos_order_id IN (
                        SELECT p.id FROM pos_order p
                        WHERE company_id in %s {extended_where_clause})""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
            self.env.cr.execute(
                f"""DELETE FROM pos_order
                    WHERE company_id IN %s {extended_where_clause}""",
                where_params,
            )
            # self.env.cr.commit()  # pylint: disable=E8102
            # self.env.cr.execute(
            #     f"""DELETE FROM pos_session
            #         WHERE company_id IN %s {extended_where_clause}""",
            #     where_params,
            # )
            _logger.info("Delete PoS operations DONE")

    def action_delete_pos_quotation_operations(self):
        if sql.table_exists(self.env.cr, "pos_quotation"):
            extended_where_clause = ""
            where_params = [tuple(self.company_ids.ids)]
            if self.date_limit:
                extended_where_clause = "AND create_date <= %s"
                where_params.append(self.date_limit)
            self.env.cr.execute(
                f"""DELETE FROM pos_quotation_line
                    WHERE quotation_id IN (
                        SELECT p.id FROM pos_quotation p
                        WHERE company_id in %s {extended_where_clause})""",
                where_params,
            )
            self.env.cr.commit()  # pylint: disable=E8102
            self.env.cr.execute(
                f"""DELETE FROM pos_quotation
                    WHERE company_id IN %s {extended_where_clause}""",
                where_params,
            )
        _logger.info("Delete PoS Quotation operations DONE")

    def action_delete_sequance_operations(self):
        sequences = self.env["ir.sequence"].search(
            [
                ("number_next_actual", "!=", 1),
                ("company_id", "in", self.company_ids.ids),
            ]
        )
        for line in sequences:
            line.number_next_actual = 1

    @api.model
    def create(self, values):
        name = _("Creation date: {}".format(fields.Datetime.now()))
        values["name"] = name
        return super().create(values)
