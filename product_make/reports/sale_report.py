# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    make_id = fields.Many2one(string="Make", comodel_name="product.make")

    def _select_sale(self):
        select_ = super()._select_sale()
        select_ += """,
            l.make_id AS make_id"""
        return select_

    def _group_by_sale(self):
        return (
            super()._group_by_sale()
            + """,
            l.make_id
        """
        )
