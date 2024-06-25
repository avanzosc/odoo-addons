# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


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

    def action_delete_stock_operations(self):
        self.env.cr.execute(
            "DELETE FROM stock_move_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM stock_move WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM stock_picking WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM stock_quant "
            "WHERE company_id in %s OR lot_id in (select l.id "
            "                      from   stock_production_lot as l"
            "                      where  l.id = stock_quant.lot_id "
            "                        and  l.company_id in %s)",
            [tuple(self.company_ids.ids), tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM stock_inventory WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_stock_production_lot(self):
        self.env.cr.execute(
            "DELETE FROM stock_production_lot WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_stock_valuation_operations(self):
        self.env.cr.execute(
            "DELETE FROM stock_valuation_layer WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_sale_operations(self):
        self.env.cr.execute(
            "DELETE FROM sale_order_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM sale_order WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_purchase_operations(self):
        self.env.cr.execute(
            "DELETE FROM purchase_order_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM purchase_order WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_analytic_operations(self):
        self.env.cr.execute(
            "DELETE FROM account_analytic_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_partial_reconcile WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_payment_order WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_payment_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_move_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_move WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_bank_statement WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_asset_line WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_asset WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_check_deposit WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_transport_operations(self):
        self.env.cr.execute(
            "DELETE FROM transport_carrier_lines_to_invoice WHERE company_id " "in %s",
            [tuple(self.company_ids.ids)],
        )

    def action_delete_mrp_operations(self):
        self.env.cr.execute(
            "DELETE FROM mrp_workorder "
            "WHERE production_id in (select p.id "
            "                        from mrp_production as p "
            "                        where p.id = mrp_workorder.production_id "
            "                          and p.company_id in %s)",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM mrp_production WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )

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
