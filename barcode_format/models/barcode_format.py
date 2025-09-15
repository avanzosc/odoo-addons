from odoo import api, fields, models


class BarcodeFormat(models.Model):
    _name = "barcode.format"
    _description = "Barcode Format"

    name = fields.Char(string="Format", required=True)

    type = fields.Selection(
        [("fijo", "Fijo"), ("variable", "Variable")], string="Type", required=True
    )

    model_id = fields.Many2one(
        "ir.model",
        string="Model to which it applies",
        required=True,
        ondelete="cascade",
        default=lambda self: self.env.ref(
            "stock.model_stock_move_line", raise_if_not_found=False
        ),
    )

    partner_ids = fields.Many2many(
        "res.partner",
        string="Partner",
        relation="barcode_format_partner_rel",
        column1="format_id",
        column2="partner_id",
        default=lambda self: self.env.context.get("default_partner_ids", []),
    )

    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )

    line_ids = fields.One2many(
        "barcode.format.line", "format_id", string="Format lines"
    )

    model_name = fields.Char(
        string="Model name", compute="_compute_model_name", store=True
    )

    @api.depends("model_id")
    def _compute_model_name(self):
        for record in self:
            record.model_name = record.model_id.model or False

    @api.onchange("type")
    def _onchange_type(self):
        if self.type == "fijo":
            pass
        elif self.type == "variable":
            self.line_ids = [(5, 0, 0)]
