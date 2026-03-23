# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateLabelWizard(models.TransientModel):
    _name = "product.template.label.wizard"
    _description = "Product template label wizard"

    template_id = fields.Many2one(
        string="Product", comodel_name="product.template", readonly=True
    )
    template_label_line_ids = fields.One2many(
        string="Wizard Lines",
        comodel_name="product.template.label.wizard.line",
        inverse_name="wizard_id",
    )
    bin = fields.Char(size=20)
    allowed_lot_ids = fields.Many2many(comodel_name="stock.lot")
    quant_location = fields.Many2one(comodel_name="stock.location")
    report_date = fields.Date(string="Date", compute="_compute_report_date")

    def _compute_report_date(self):
        for wiz in self:
            wiz.report_date = fields.Date.context_today(self)

    def default_get(self, fields):
        result = super().default_get(fields)
        if "active_id" in self.env.context:
            result["template_id"] = self.env.context.get("active_id")
            cond = [("product_tmpl_id", "=", self.env.context.get("active_id"))]
            product = self.env["product.product"].search(cond, limit=1)
            if product:
                cond = [("product_id", "=", product.id)]
                lot = self.env["stock.lot"].search(cond)
                result["allowed_lot_ids"] = [(6, 0, lot.ids)]
        return result

    def print_template_label(self):
        if not self.template_label_line_ids:
            raise ValidationError(_("You must enter a line to print the label."))
        if (
            self.template_label_line_ids[0].lot_id
            and self.template_label_line_ids[0].lot_id.quant_ids
        ):
            quant = min(
                self.template_label_line_ids[0].lot_id.quant_ids,
                key=lambda x: x.id and x.location_id,
            )
            self.quant_location = quant.location_id.id
        action = self.env.ref(
            "stock_product_qr_label.action_product_template_label_wizard_report"
        )
        return action.report_action(self)


class ProductTemplateLabelWizardLine(models.TransientModel):
    _name = "product.template.label.wizard.line"
    _description = "Product template label wizard line"

    def _get_default_product_id(self):
        if "default_product_template" in self.env.context:
            cond = [
                (
                    "product_tmpl_id",
                    "=",
                    self.env.context.get("default_product_template"),
                )
            ]
            product = self.env["product.product"].search(cond, limit=1)
            if product:
                return product.id

    wizard_id = fields.Many2one(
        string="wizard", comodel_name="product.template.label.wizard"
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        default=_get_default_product_id,
    )
    lot_id = fields.Many2one(string="Lot", comodel_name="stock.lot")
    location_id = fields.Many2one(string="Location", comodel_name="stock.location")
    product_qty = fields.Integer(string="Quantity", default=0)
    qr_code = fields.Char(string="QR Code", compute="_compute_qr_code")

    def _compute_qr_code(self):
        for line in self:
            qr_code = "{} {}".format(
                (
                    line.wizard_id.template_id.default_code
                    if line.wizard_id.template_id.default_code
                    else ""
                ),
                line.lot_id.name if line.lot_id.name else "",
            )
            line.qr_code = qr_code
