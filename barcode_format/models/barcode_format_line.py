from odoo import api, fields, models


class BarcodeFormatLine(models.Model):
    _name = "barcode.format.line"
    _description = "Línea de Formato de Código de Barras"

    format_id = fields.Many2one(
        "barcode.format", string="Formato", required=True, ondelete="cascade"
    )

    field_id = fields.Many2one(
        "ir.model.fields", string="Campo", required=True, ondelete="cascade"
    )

    start_pos = fields.Integer(string="Posición inicio")

    final_pos = fields.Integer(string="Posición fin")

    gs1_barcode_id = fields.Many2one("gs1_barcode", string="Prefijo GS1")

    format_type = fields.Selection(
        [("fijo", "Fijo"), ("variable", "Variable")],
        string="Tipo de Formato",
        compute="_compute_format_type",
        store=True,
    )

    @api.depends("format_id.type")
    def _compute_format_type(self):
        for rec in self:
            rec.format_type = rec.format_id.type

    format_model_id = fields.Many2one(
        related="format_id.model_id", string="Modelo", store=True
    )

    @api.onchange("format_id")
    def _onchange_format_id(self):
        if self.format_id and self.format_id.model_id:
            model_name = self.format_id.model_id.model
            return {"domain": {"field_id": [("model", "=", model_name)]}}
