# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, tools
from psycopg2.extensions import AsIs


class ResPartnerBirthdayReport(models.Model):
    _name = "res.partner.birthday.report"
    _inherit = "res.partner.birthdate.report"
    _description = "Contact's Birthday Report"
    _auto = False
    _rec_name = "partner_id"

    def _select(self):
        return super(ResPartnerBirthdayReport, self)._select()

    def _from(self):
        return super(ResPartnerBirthdayReport, self)._from()

    def _where(self):
        where_str = """
            AND
                DATE_PART('day', birthdate_date) = date_part('day',
                CURRENT_DATE)
            AND
                DATE_PART('month', birthdate_date) = date_part('month',
                CURRENT_DATE)
        """
        return super(ResPartnerBirthdayReport, self)._where() + where_str

    def _group_by(self):
        return super(ResPartnerBirthdayReport, self)._group_by()

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
