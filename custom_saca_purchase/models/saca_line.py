# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
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

    def action_create_purchase(self):
        self.ensure_one()
        presaca = self.env.ref("custom_saca_purchase.stage_presaca")
        if self.stage_id == presaca and not self.purchase_order_id:
            if not self.supplier_id:
                raise ValidationError(
                    _("You must introduce the supplier."))
            now = fields.Datetime.now()
            purchase_order = self.env["purchase.order"].create({
                "partner_id": self.supplier_id.id,
                "date_order": now})
            purchase_order.saca_id = self.saca_id.id
            self.write({
                "purchase_order_id": purchase_order.id,
                "stage_id": (
                    self.env.ref("custom_saca_purchase.stage_saca").id)})
