# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventAcademicYear(models.Model):
    _name = "event.academic.year"
    _description = "Event academic year"

    name = fields.Char(string="Description")
    begin_date = fields.Date(string="Begin date")
    end_date = fields.Date(string="End date")
