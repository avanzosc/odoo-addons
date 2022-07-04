# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class EstimateWeight(models.Model):
    _name = "estimate.weight"
    _description = "Estimate Weight"

    def _get_default_weight_uom(self):
        try:
            return self.env.ref("uom.product_uom_gram").id
        except Exception:
            return False

    def _get_default_total_weight_uom(self):
        try:
            return self.env.ref("uom.product_uom_kgm").id
        except Exception:
            return False

    day = fields.Integer(string='Day')
    estimate_weight = fields.Float(string='Estimate Weight')
    estimate_week_weight = fields.Float(string='Estimate Week Weight')
    real_weight = fields.Float(string='Real Weight')
    weight_uom_id = fields.Many2one(
        string="Weight UOM",
        comodel_name="uom.uom",
        default=_get_default_weight_uom,
        domain=lambda self: [
            ("category_id", "=",
             self.env.ref("uom.product_uom_categ_kgm").id)])
    batch_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    date = fields.Date(string="Date")
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
        store=True)
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="batch_id.warehouse_id",
        store=True)
    farmer_id = fields.Many2one(
        string="Farmer",
        comodel_name="res.partner",
        related="warehouse_id.farmer_id",
        store=True)
    growth = fields.Float(
        string="Growth",
        compute="_compute_growth",
        store=True)
    unit = fields.Integer(string="Units")
    casualities = fields.Integer(string="Casualities")
    total_weight = fields.Float(
        string="Total Weight",
        compute="_compute_total_weight")
    total_weight_uom_id = fields.Many2one(
        string="Total Weight UOM",
        comodel_name="uom.uom",
        default=_get_default_total_weight_uom,
        domain=lambda self: [
            ("category_id", "=",
             self.env.ref("uom.product_uom_categ_kgm").id)])

    @api.depends("day", "estimate_weight")
    def _compute_growth(self):
        for line in self:
            line.growth = 0
            cond = [("batch_id", "=", line.batch_id.id),
                    ("day", "=", line.day - 1)]
            before_line = self.env["estimate.weight"].search(cond, limit=1)
            if line.day and before_line:
                line.growth = (
                    line.estimate_weight - before_line.estimate_weight)

    @api.depends("estimate_week_weight", "unit", "estimate_weight", "weight_uom_id")
    def _compute_total_weight(self):
        for line in self:
            line.total_weight = 0
            if line.estimate_week_weight and line.unit:
                if line.weight_uom_id == self.env.ref("uom.product_uom_kgm"):
                    line.total_weight = line.estimate_week_weight * line.unit
                if line.weight_uom_id == self.env.ref("uom.product_uom_gram"):
                    line.total_weight = line.estimate_week_weight * line.unit / 1000
            elif line.estimate_weight and line.unit:
                if line.weight_uom_id == self.env.ref("uom.product_uom_kgm"):
                    line.total_weight = line.estimate_weight * line.unit
                if line.weight_uom_id == self.env.ref("uom.product_uom_gram"):
                    line.total_weight = line.estimate_weight * line.unit / 1000
            line.total_weight_uom_id = self.env.ref("uom.product_uom_kgm").id

    def write(self, values):
        result = super(EstimateWeight, self).write(values)
        cond = [("batch_id", "=", self.batch_id.id),
                ("day", ">", self.day)]
        lines = self.env["estimate.weight"].search(cond)
        if lines:
            for line in lines:
                if "real_weight" in values:
                    if values.get("real_weight") == 0:
                        self.estimate_week_weight = 0
                        line.estimate_week_weight = 0
                    real_vals = self.env["estimate.weight"].search(
                        [("batch_id", "=", self.batch_id.id),
                        ("day", "<", self.day),
                        ("real_weight", ">", self.real_weight)])
                    if real_vals:
                        raise ValidationError(
                            _("There is a other real weight that is greater than this one.")
                        )
                    else:
                        self.estimate_week_weight = self.real_weight
                        for line in self.env["estimate.weight"].search(cond):
                            cond = [
                                ("batch_id", "=", self.batch_id.id),
                                ("day", "=", line.day - 1)]
                            before_line = self.env["estimate.weight"].search(
                                cond, limit=1)
                            if before_line:
                                line.estimate_week_weight = (
                                    before_line.estimate_week_weight + line.growth)
                if "unit" in values and not line.casualities:
                    if line.unit != self.unit and (not line.unit or line.unit > self.unit):
                        line.unit = self.unit
                if "casualities" in values:
                    line.unit = self.unit - self.casualities
        return result
