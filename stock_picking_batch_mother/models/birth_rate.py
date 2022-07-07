# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class BirthRate(models.Model):
    _name = "birth.rate"
    _description = "Birth Rate"

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    mother_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.picking.batch')
    week = fields.Integer(string='Week')
    percentage_birth = fields.Float(string='% of Birth Over Total')
    birth_start_date = fields.Date(string="Birth Start Date")
    estimate_birth = fields.Integer(
        string="Estimate Birth",
        compute="_compute_estimate_birth",
        store=True)
    real_birth = fields.Float(
        string="Real Birth")

    @api.depends("mother_id", "mother_id.hen_unit",
                 "percentage_birth")
    def _compute_estimate_birth(self):
        for line in self:
            line.estimate_birth = 7 * line.mother_id.hen_unit * (
                line.percentage_birth) / 100
