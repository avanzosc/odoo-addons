# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models

class CleaningDatabase(models.Model):
    _name = "cleaning.database"
    _description = "Cleaning Database Operations"

    def action_delete_operations(self):
        self.env.cr.execute("""
            DELETE FROM stock_move_line;
            DELETE FROM stock_move;
            DELETE FROM stock_picking;
            DELETE FROM sale_order_line;
            DELETE FROM sale_order;
            DELETE FROM purchase_order_line;
            DELETE FROM purchase_order;
            DELETE FROM account_analytic_line;
            DELETE FROM stock_quant;
            DELETE FROM stock_valuation_layer;
            DELETE FROM account_partial_reconcile;
            DELETE FROM account_payment_order;
            DELETE FROM account_payment_line;
            DELETE FROM account_move_line;
            DELETE FROM account_move;
            DELETE FROM transport_carrier_lines_to_invoice;
            DELETE FROM stock_inventory;
            DELETE FROM mrp_workorder;
            DELETE FROM mrp_production;
            DELETE FROM stock_production_lot;
        """)
        sequences = self.env["ir.sequence"].search([("number_next_actual", "!=", 1)])
        for line in sequences:
            line.number_next_actual = 1
