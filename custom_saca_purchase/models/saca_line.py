# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _default_stage_id(self):
        try:
            stage = self.env["saca.line.stage"].search([])
            if stage:
                stage = min(stage, key=lambda x: x.sequence)
                return stage.id
            else:
                return False
        except Exception:
            return False

    purchase_order_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order")
    purchase_order_line_ids = fields.One2many(
        string="Purchase Orden Line",
        comodel_name="purchase.order.line",
        inverse_name="saca_line_id")
    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="saca.line.stage",
        default=_default_stage_id)
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    date = fields.Date(
        string="Date",
        related="saca_id.date",
        store=True)

    @api.onchange("breeding_id")
    def onchange_product_id(self):
        self.product_id = False
        if self.breeding_id and self.breeding_id.estimate_weight_ids:
            line = self.breeding_id.estimate_weight_ids.search(
                [("date", "=", self.date),
                 ("batch_id", "=", self.breeding_id.id)], limit=1)
            self.product_id = line.product_id.id
            self.age = line.day
            self.weight_uom_id = line.weight_uom_id.id
            if line.real_weight:
                self.estimate_weight = line.real_weight
            else:
                self.estimate_weight = line.estimate_weight

    def action_create_purchase(self):
        self.ensure_one()
        presaca = self.env.ref("custom_saca_purchase.stage_presaca")
        if self.stage_id == presaca and not (
            self.purchase_order_id) and (
                self.product_id):
            if not self.supplier_id:
                raise ValidationError(
                    _("You must introduce a supplier."))
            now = fields.Datetime.now()
            purchase_order = self.env["purchase.order"].create({
                "partner_id": self.supplier_id.id,
                "date_order": now,
                "saca_line_id": self.id})
            self.write({
                "purchase_order_id": purchase_order.id,
                "stage_id": (
                    self.env.ref("custom_saca_purchase.stage_saca").id)})
            purchase_line = self.env["purchase.order.line"].create({
                "order_id": purchase_order.id,
                "product_id": self.product_id.id,
                "saca_line_id": self.id})
            if purchase_line.product_qty == 0:
                purchase_line.product_qty = 1
        else:
            raise ValidationError(
                    _("You must introduce a product."))
