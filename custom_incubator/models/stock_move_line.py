# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import datetime
from dateutil import rrule


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    batch_id = fields.Many2one(
        string="Batch",
        comodel_name="stock.picking.batch")
    broken = fields.Integer(string="Broken")
    waste = fields.Integer(string="Waste")

    @api.onchange("batch_id")
    def onchange_lot(self):
        if self.batch_id:
            today = fields.Date.today()
            start_date = datetime(today.year, 1, 1, 0, 0).date()
            weeks = self.weeks_between(start_date, today)
            lot = self.env["stock.production.lot"].create({
                "name": u'{}{}{}'.format(
                    self.batch_id.name, weeks, u'{}'.format(today.year)[2:]),
                "product_id": self.product_id.id,
                "company_id": self.company_id.id,
                "batch_id": self.batch_id.id})
            self.lot_id = lot.id

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()
