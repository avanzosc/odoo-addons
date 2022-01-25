# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools
from psycopg2.extensions import AsIs

MONTH_SELECTION = [(1, 'January'),
                   (2, 'February'),
                   (3, 'March'),
                   (4, 'April'),
                   (5, 'May'),
                   (6, 'June'),
                   (7, 'July'),
                   (8, 'August'),
                   (9, 'September'),
                   (10, 'October'),
                   (11, 'November'),
                   (12, 'December')]


class ResPartnerBirthdayReport(models.Model):
    _name = "res.partner.birthdate.report"
    _description = "Contact's Birthdate Report"
    _auto = False
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name="res.partner")
    birthdate = fields.Date()
    birthdate_day = fields.Integer()
    birthdate_month = fields.Selection(selection=MONTH_SELECTION)
    birthdate_year = fields.Integer()

    _depends = {
        "res.partner": [
            "birthdate_date",
        ],
    }

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER () as id,
                p.id as partner_id,
                p.birthdate_date as birthdate,
                EXTRACT (YEAR FROM p.birthdate_date) AS birthdate_year,
                EXTRACT (MONTH FROM p.birthdate_date) AS birthdate_month,
                EXTRACT (DAY FROM p.birthdate_date) AS birthdate_day
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
                res_partner p
        """
        return from_str

    def _where(self):
        where_str = """
            WHERE
                p.birthdate_date IS NOT NULL
            AND
                active = True
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                p.id, p.birthdate_date
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()),
                AsIs(self._from()), AsIs(self._where()),
                AsIs(self._group_by()),))
