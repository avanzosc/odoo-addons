from odoo import api, fields, models


class BarcodeFormatLine(models.Model):
    _name = "barcode.format.line"
    _description = "Barcode Format Line"

    format_id = fields.Many2one(
        "barcode.format", string="Format", required=True, ondelete="cascade"
    )

    field_id = fields.Many2one(
        "ir.model.fields", string="Field", required=True, ondelete="cascade"
    )

    start_pos = fields.Integer(string="Start Position")

    final_pos = fields.Integer(string="End Position")

    decimals = fields.Integer(
        default=0,
    )

    decimal_position = fields.Integer(
        string="posición decimal",
    )

    barcode_rule_id = fields.Many2one(
        string="GS1 Prefix",
        comodel_name="barcode.rule",
        domain=[("barcode_nomenclature_id.is_gs1_nomenclature", "=", True)],
    )

    format_type = fields.Selection(
        [("fijo", "Fijo"), ("variable", "Variable")],
        compute="_compute_format_type",
        store=True,
    )

    @api.depends("format_id.type")
    def _compute_format_type(self):
        for rec in self:
            rec.format_type = rec.format_id.type

    format_model_id = fields.Many2one(
        related="format_id.model_id", string="Model", store=True
    )

    @api.onchange("format_id")
    def _onchange_format_id(self):
        if self.format_id and self.format_id.model_id:
            model_name = self.format_id.model_id.model
            return {"domain": {"field_id": [("model", "=", model_name)]}}
