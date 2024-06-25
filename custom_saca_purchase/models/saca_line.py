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
        string="Purchase Order", comodel_name="purchase.order", copy=False
    )
    purchase_order_line_ids = fields.One2many(
        string="Purchase Orden Line",
        comodel_name="purchase.order.line",
        inverse_name="saca_line_id",
        copy=False,
    )
    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="saca.line.stage",
        default=_default_stage_id,
        copy=False,
    )
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    price_unit = fields.Float(
        string="Price Unit",
        related="purchase_order_line_ids.price_unit",
        readonly=False,
        digits="Weight Decimal Precision",
    )
    purchase_ids = fields.One2many(
        string="Purchase Order",
        comodel_name="purchase.order",
        compute="_compute_purchase_ids",
    )
    count_purchases = fields.Integer(
        string="Purchases Count", compute="_compute_count_purchases"
    )

    def _compute_count_purchases(self):
        for saca in self:
            saca.count_purchases = len(saca.purchase_ids)

    def _compute_purchase_ids(self):
        for line in self:
            purchase = []
            if line.purchase_order_id:
                purchase.append(line.purchase_order_id.id)
            line.purchase_ids = [(6, 0, purchase)]

    def action_view_purchase_ids(self):
        context = self.env.context.copy()
        return {
            "name": _("Purchase Order"),
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "domain": [("id", "in", self.purchase_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }

    @api.onchange("estimate_burden", "estimate_weight")
    def onchange_estimate_burden(self):
        if self.estimate_burden and self.estimate_weight:
            for line in self.purchase_order_line_ids:
                line.product_qty = self.estimate_burden * (self.estimate_weight)

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            for line in self.purchase_order_line_ids:
                line.product_id = self.product_id.id
                line.onchange_product_id()

    @api.onchange("breeding_id", "external_supplier")
    def onchange_breeding_id(self):
        result = super().onchange_breeding_id()
        self.product_id = False
        if self.breeding_id and self.breeding_id.estimate_weight_ids:
            line = self.breeding_id.estimate_weight_ids.search(
                [("date", "=", self.date), ("batch_id", "=", self.breeding_id.id)],
                limit=1,
            )
            self.product_id = line.product_id.id
            if line.weight_uom_id.id == self.env.ref("uom.product_uom_kgm").id:
                n = 1
            elif line.weight_uom_id.id == self.env.ref("uom.product_uom_gram").id:
                n = 0.001
            if line.real_weight:
                self.estimate_weight = line.real_weight * n
            elif line.estimate_week_weight:
                self.estimate_weight = line.estimate_week_weight * n
            elif line.estimate_weight:
                self.estimate_weight = line.estimate_weight * n
        return result

    def action_create_purchase(self):
        self.ensure_one()
        company = self.company_id
        supplier = self.supplier_id
        if supplier == company.partner_id:
            raise ValidationError(
                _(
                    "You cannot create a purchase from a supplier whose "
                    + "company is owned by your company"
                )
            )
        presaca = self.env.ref("custom_saca_purchase.stage_presaca")
        if (
            self.stage_id == presaca
            and not (self.purchase_order_id)
            and (self.product_id)
        ):
            if not self.supplier_id:
                raise ValidationError(_("You must introduce a supplier."))
            now = fields.Datetime.now()
            purchase_order = self.env["purchase.order"].create(
                {
                    "partner_id": self.supplier_id.id,
                    "picking_type_id": self.sudo()
                    .env["stock.picking.type"]
                    .search(
                        [
                            ("code", "=", "incoming"),
                            ("warehouse_id.company_id", "=", company.id),
                        ]
                    )[:1]
                    .id,
                    "date_order": now,
                    "saca_line_id": self.id,
                    "company_id": company.id,
                }
            )
            self.write(
                {
                    "purchase_order_id": purchase_order.id,
                    "stage_id": (self.env.ref("custom_saca_purchase.stage_saca").id),
                }
            )
            purchase_line = self.env["purchase.order.line"].create(
                {
                    "order_id": purchase_order.id,
                    "product_id": self.product_id.id,
                    "saca_line_id": self.id,
                }
            )
            if purchase_line.product_qty == 0:
                purchase_line.product_qty = 1
        else:
            raise ValidationError(_("You must introduce a product."))
