from odoo import api, fields, models


class BarcodeFormat(models.Model):
    _name = "barcode.format"
    _description = "Formato de Código de Barras"

    name = fields.Char(string="Formato", required=True)

    type = fields.Selection(
        [("fijo", "Fijo"), ("variable", "Variable")], string="Tipo", required=True
    )

    model_id = fields.Many2one(
        "ir.model",
        string="Modelo al que aplica",
        required=True,
        ondelete="cascade",
        default=lambda self: self.env.ref(
            "stock.model_stock_move_line", raise_if_not_found=False
        ),
    )

    partner_id = fields.Many2one("res.partner", string="Partner", ondelete="set null")

    line_ids = fields.One2many(
        "barcode.format.line", "format_id", string="Líneas del formato"
    )

    field_separator = fields.Char(
        string="Separador de campo",
        help="Caracter que separa campos en códigos de tipo variable",
    )

    @api.onchange("type")
    def _onchange_type(self):
        if self.type == "fijo":
            pass
        elif self.type == "variable":
            self.line_ids = [(5, 0, 0)]
