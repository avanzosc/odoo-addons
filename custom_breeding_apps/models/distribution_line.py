# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DistributionLine(models.Model):
    _name = "distribution.line"
    _description = "Distribution Line"
    _order = "seq"

    seq = fields.Integer(string="Sequence")
    lot_id = fields.Many2one(
        string="Lot/Serial number", comodel_name="stock.production.lot"
    )
    distribute_qty = fields.Integer(string="Quantity")
    picking_id = fields.Many2one(string="Picking", comodel_name="stock.picking")
    batch_id = fields.Many2one(string="Mother", comodel_name="stock.picking.batch")
    warehouse_id = fields.Many2one(string="Farm", comodel_name="stock.warehouse")
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    birth_estimate_date = fields.Date(
        string="Birth estimate date",
        related="picking_id.birth_estimate_date",
        store=True,
    )
    estimate_birth = fields.Integer(
        string="Estimate Birth", compute="_compute_estimate_birth", store=True
    )
    pending_qty = fields.Integer(
        string="Pending Qty", compute="_compute_pending_qty", store=True
    )

    @api.depends(
        "picking_id",
        "estimate_birth",
        "picking_id.distribution_ids",
        "picking_id.distribution_ids.distribute_qty",
        "product_id",
        "batch_id",
    )
    def _compute_pending_qty(self):
        for line in self:
            pending_qty = 0
            distribution_lines = line.picking_id.distribution_ids.filtered(
                lambda c: c.batch_id == line.batch_id
            )
            if line.picking_id and distribution_lines:
                pending_qty = line.estimate_birth - sum(
                    distribution_lines.mapped("distribute_qty")
                )
            line.pending_qty = pending_qty

    @api.depends(
        "picking_id",
        "picking_id.move_line_ids_without_package",
        "picking_id.move_line_ids_without_package.birth_estimate_qty",
        "product_id",
        "batch_id",
    )
    def _compute_estimate_birth(self):
        for line in self:
            estimate_birth = 0
            if (line.picking_id) and (
                line.picking_id.move_line_ids_without_package.filtered(
                    lambda x: x.batch_id == line.batch_id
                )
            ):
                estimate_birth = sum(
                    line.picking_id.move_line_ids_without_package.filtered(
                        lambda x: x.batch_id == line.batch_id
                    ).mapped("birth_estimate_qty")
                )
            line.estimate_birth = estimate_birth

    @api.onchange("picking_id")
    def onchange_picking_id(self):
        domain = {}
        self.ensure_one()
        product = self.env["product.product"].search([("one_day_chicken", "=", True)])
        if product and len(product) == 1:
            self.product_id = product[0].id
        if self.picking_id:
            move_lines = self.picking_id.move_line_ids_without_package.filtered(
                lambda x: x.batch_id
            )
            mothers = move_lines.mapped("batch_id")
            if not mothers:
                raise ValidationError(_("There is no movement with mothers."))
            if mothers:
                domain = {"domain": {"batch_id": [("id", "in", mothers.ids)]}}
                if len(mothers) == 1:
                    self.batch_id = mothers[0].id
        return domain
