# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizCreateAutoReorderingRule(models.TransientModel):
    _name = "wiz.create.auto.reordering.rule"
    _description = "Wizard for create reordering rules"

    line_ids = fields.One2many(
        string="Lines",
        comodel_name="wiz.create.auto.reordering.rule.line",
        inverse_name="wiz_id",
    )

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        cond = [("automatic_rule", "=", True)]
        locations = self.env["stock.location"].search(cond)
        if locations:
            vals = []
            for location in locations:
                vals.append((0, 0, {"location_id": location.id}))
            result["line_ids"] = vals
        return result

    def button_create_reordering_rules(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        products = self.env["product.product"].browse(active_ids)
        if products:
            locations = self.line_ids.mapped("location_id")
            if locations:
                products._create_reordering_rule(default_locations=locations)
        return {"type": "ir.actions.act_window_close"}


class WizCreateAutoReorderingRuleLine(models.TransientModel):
    _name = "wiz.create.auto.reordering.rule.line"
    _description = "Lines for wizard for create reordering rules"

    wiz_id = fields.Many2one(
        string="Wizard", comodel_name="wiz.create.auto.reordering.rule"
    )
    location_id = fields.Many2one(string="Location", comodel_name="stock.location")
