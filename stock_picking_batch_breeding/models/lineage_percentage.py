# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LineagePercentage(models.Model):
    _name = "lineage.percentage"
    _description = "Lineage Percentage"

    lineage_id = fields.Many2one(string="Lineage", comodel_name="lineage")
    percentage = fields.Float(string="Lineage %")
    batch_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch",
        domain="[('batch_type', '=', 'breeding')]",
    )

    @api.constrains("percentage", "batch_id")
    def _check_percentage(self):
        for line in self.filtered("batch_id"):
            total = sum(line.batch_id.lineage_percentage_ids.mapped("percentage"))
            if total != 100:
                raise ValidationError(_("The sum of the percentages is not 100."))
