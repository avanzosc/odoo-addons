# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DistributionLine(models.Model):
    _name = "distribution.line"
    _description = "Distribution Line"
    _order = "seq"

    seq = fields.Integer(
        string="Sequence")
    lot_id = fields.Many2one(
        string="Lot/Serial number",
        comodel_name="stock.production.lot")
    distribute_qty = fields.Float(
        string="Quantity")
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking")
    batch_id = fields.Many2one(
        string="Mother",
        comodel_name="stock.picking.batch")
    warehouse_id = fields.Many2one(
        string="Farm",
        comodel_name="stock.warehouse")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    birth_estimate_date = fields.Date(
        string="Birth estimate date",
        related="picking_id.birth_estimate_date",
        store=True)
    estimate_birth = fields.Float(
        string="Estimate Birth",
        compute="_compute_estimate_birth",
        store=True)

    @api.depends("picking_id", "picking_id.move_line_ids_without_package",
                 "picking_id.move_line_ids_without_package.birth_estimate_qty",
                 "product_id", "lot_id")
    def _compute_estimate_birth(self):
        for line in self:
            line.estimate_birth = 0
            if (
                line.picking_id) and (
                    line.picking_id.move_line_ids_without_package):
                line.estimate_birth = (
                    line.picking_id.move_line_ids_without_package.filtered(
                        lambda x: x.batch_id == line.batch_id and (
                            x.lot_id == line.lot_id))[0].birth_estimate_qty)

    @api.onchange("picking_id")
    def onchange_picking_id(self):
        domain = {}
        self.ensure_one()
        if self.picking_id:
            move_lines = (
                self.picking_id.move_line_ids_without_package.filtered(
                    lambda x: x.batch_id))
            mothers = []
            for line in move_lines:
                mothers.append(line.batch_id.id)
            if not mothers:
                raise ValidationError(
                    _("There is no movement with mothers.")
                    )
            if mothers:
                domain = {"domain": {"batch_id": [("id", "in", mothers)]}}
                if len(mothers) == 1:
                    self.batch_id = mothers[0]
        return domain

    @api.onchange("batch_id")
    def onchange_batch_id(self):
        domain = {}
        self.ensure_one()
        if self.batch_id:
            move_lines = (
                self.picking_id.move_line_ids_without_package.filtered(
                    lambda x: x.batch_id == self.batch_id))
            lots = []
            for line in move_lines:
                lots.append(line.lot_id.id)
            if not lots:
                raise ValidationError(
                    _("There is no movement with mothers and lots.")
                    )
            if lots:
                domain = {"domain": {"lot_id": [("id", "in", lots)]}}
                if len(lots) == 1:
                    self.lot_id = lots[0]
        return domain
