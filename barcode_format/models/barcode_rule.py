from odoo import api, fields, models


class BarcodeRule(models.Model):
    _inherit = "barcode.rule"
    _rec_name = "display_name"

    ai = fields.Integer(
        string="Application Identifier",
        help="The standard Application Identifier (AI)",
        compute="_compute_ai",
        store=True,
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    def _compute_ai(self):
        for rule in self:
            if rule.pattern and "(" in rule.pattern and ")" in rule.pattern:
                try:
                    rule.ai = int(rule.pattern.split(")")[0].lstrip("("))
                except ValueError:
                    rule.ai = 0
            else:
                rule.ai = 0

    @api.depends("name", "ai")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"({rec.ai}) {rec.name}" if rec.ai else rec.name

    def name_get(self):
        result = []
        for record in self:
            display_name = f"({record.ai}) {record.name}"
            result.append((record.id, display_name))
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = ["|", ("ai", operator, name), ("name", operator, name)] if name else []
        return self.search(domain + args, limit=limit).name_get()
