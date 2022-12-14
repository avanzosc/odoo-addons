# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class LayingRate(models.Model):
    _name = "laying.rate"
    _description = "Laying Rate"

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    mother_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.picking.batch')
    week = fields.Integer(string='Week')
    percentage_laying = fields.Float(string='% of Laying')
    laying_start_date = fields.Date(string="Laying Start Date")
    estimate_laying = fields.Integer(
        string="Estimate Laying",
        compute="_compute_estimate_laying",
        store=True)
    real_laying = fields.Float(
        string="Real Laying")

    @api.depends("mother_id", "mother_id.hen_unit",
                 "percentage_laying")
    def _compute_estimate_laying(self):
        for line in self:
            line.estimate_laying = 7 * line.mother_id.hen_unit * (
                line.percentage_laying) / 100
