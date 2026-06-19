# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockDebtTransferLine(models.TransientModel):
    _name = "stock.debt.transfer.line"
    _description = "Debt Transfer Line"

    debt_transfer_id = fields.Many2one(
        "stock.debt.transfer", "Debt Transfer", required=True
    )
    picking_id = fields.Many2one("stock.picking", "Transfer", required=True)
    to_process = fields.Boolean("To Process")


class StockDebtTransfer(models.TransientModel):
    _name = "stock.debt.transfer"
    _description = "Debt Transfer"

    pick_ids = fields.Many2many("stock.picking", "stock_picking_debt_transfer_rel")
    show_transfers = fields.Boolean()
    debt_transfer_line_ids = fields.One2many(
        "stock.debt.transfer.line", "debt_transfer_id", string="Debt Transfer Lines"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if "debt_transfer_line_ids" in fields and res.get("pick_ids"):
            res["debt_transfer_line_ids"] = [
                (0, 0, {"to_process": True, "picking_id": pick_id})
                for pick_id in res["pick_ids"][0][2]
            ]
            # default_get returns x2m values as [(6, 0, ids)]
            # because of webclient limitations
        return res

    def process(self):
        pickings_to_do = self.env["stock.picking"]
        pickings_not_to_do = self.env["stock.picking"]
        for line in self.debt_transfer_line_ids:
            if line.to_process is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        pickings_to_validate = self.env.context.get("button_validate_picking_ids")
        if pickings_to_validate:
            pickings_to_validate = self.env["stock.picking"].browse(
                pickings_to_validate
            )
            pickings_to_validate = pickings_to_validate - pickings_not_to_do
            return pickings_to_validate.with_context(skip_debt=True).button_validate()
        return True

    def process_no_debt(self):
        """Don't process for concerned pickings (ones with invalid lots), but
        process for all other pickings (in case of multi)."""
        # Remove `self.pick_ids` from `button_validate_picking_ids` and call
        # `button_validate` with the subset (if any).
        pickings_to_validate = self.env["stock.picking"].browse(
            self.env.context.get("button_validate_picking_ids")
        )
        pickings_to_validate = pickings_to_validate - self.pick_ids
        if pickings_to_validate:
            return pickings_to_validate.with_context(skip_debt=True).button_validate()
        return True
