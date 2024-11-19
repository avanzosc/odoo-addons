# Copyright 2024 Berezi Amubieta - AvanzOSC
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

    def action_open_delete_warning(self):
        wiz_obj = self.env["cleaning.database.warning.wizard"]
        vals = {}
        if "default_object_to_delete" in self.env.context:
            vals = {"object_to_delete": self.env.context["default_object_to_delete"]}
        wiz = wiz_obj.with_context(active_id=self.id).create(vals)
        context = self.env.context.copy()
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
            "                      from   stock_lot as l"
            "                      where  l.id = stock_quant.lot_id "
            "                        and  l.company_id in %s)",
            [tuple(self.company_ids.ids), tuple(self.company_ids.ids)],
        )

    def action_delete_stock_production_lot(self):
        self.env.cr.execute(
            "DELETE FROM stock_lot WHERE company_id in %s",
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

    def action_delete_accounting_operations(self):
        self.env.cr.execute(
            "DELETE FROM account_partial_reconcile WHERE company_id in %s",
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
            "DELETE FROM account_payment_order WHERE company_id in %s",
            [tuple(self.company_ids.ids)],
        )
        self.env.cr.execute(
            "DELETE FROM account_payment_line WHERE company_id in %s",
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
        name = _("Creation date: {}").format(fields.Datetime.now())
        values["name"] = name
        return super().create(values)
