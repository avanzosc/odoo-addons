# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthdate_day = fields.Integer(
        string="Birthdate Day", compute="_compute_birthdate", store=True,
        index=True)
    birthdate_month = fields.Integer(
        string="Birthdate Month", compute="_compute_birthdate", store=True,
        index=True)
    birthday_today = fields.Boolean(
        string="Birthday's Today", compute="_compute_birthday",
        search="_search_birthday")

    @api.depends("birthdate_date")
    def _compute_birthdate(self):
        for record in self.filtered("birthdate_date"):
            record.birthdate_day = record.birthdate_date.day
            record.birthdate_month = record.birthdate_date.month

    @api.multi
    def _compute_birthday(self):
        today = fields.Date.context_today(self)
        for partner in self.filtered("birthdate_date"):
            partner.birthday_today = (
                partner.birthdate_day == today.day and
                partner.birthdate_month == today.month)

    @api.multi
    def _search_birthday(self, operator, value):
        today = fields.Date.context_today(self)
        if operator != '=':
            if operator == '!=' and isinstance(value, bool):
                value = not value
            else:
                raise NotImplementedError()
        partners = self.search_birthdate(today)
        if value:
            search_operator = "in"
        else:
            search_operator = "not in"
        return [('id', search_operator, partners.ids)]

    def next_week_birthday(self):
        today = fields.Date.context_today(self)
        partners = self.env["res.partner"]
        for days in range(1, 8):
            new_date = today + relativedelta(days=days)
            partners |= self.search_birthdate(new_date)
        return partners

    def search_birthdate(self, birthdate):
        return self.search([
            ("birthdate_day", "=", birthdate.day),
            ("birthdate_month", "=", birthdate.month),
        ])
