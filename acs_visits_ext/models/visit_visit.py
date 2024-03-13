# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class VisitVisit(models.Model):
    _inherit = "visit.visit"

    visit_type_id = fields.Many2one(
        string="Visit Type", comodel_name="visit.type", copy=False
    )
    person_id = fields.Many2one(
        string="Person", comodel_name="res.partner", copy=False
    )
    title_id = fields.Many2one(
        string="title", comodel_name="res.partner.title",
        related="person_id.title", store=True, copy=False
    )
    email = fields.Char(
        string="Email", related="person_id.email", store=True, copy=False
    )
    phone = fields.Char(
        string="Phone", related="person_id.phone", store=True, copy=False
    )
    mobile = fields.Char(
        string="Mobile", related="person_id.mobile", store=True, copy=False
    )
    comment = fields.Text(
        string="Notes", related="person_id.comment", store=True, copy=False)

    @api.model
    def create(self, values):
        
        return super(VisitVisit, self).create(values)
