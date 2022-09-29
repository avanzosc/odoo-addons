# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil import rrule


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    batch_id = fields.Many2one(
        string="Batch",
        comodel_name="stock.picking.batch")
    accounting_date_week = fields.Integer(
        string="Date Weeks",
        compute="_compute_date_week",
        store=True)
    accounting_date = fields.Date(
        string="Date",
        default=fields.Date.today())

    def calculate_weeks_start(self, start_date):
        self.ensure_one()
        weekday = start_date.weekday()
        if weekday <= 3:
            return start_date - timedelta(days=weekday)
        else:
            return start_date + timedelta(days=(7-weekday))

    @api.depends("accounting_date")
    def _compute_date_week(self):
        for line in self:
            line.accounting_date_week = 0
            if line.accounting_date:
                start_date = datetime(
                    line.accounting_date.year, 1, 1, 0, 0).date()
                start_date = line.calculate_weeks_start(start_date)
                end_date = line.accounting_date
                if end_date < start_date:
                    start_date = datetime(
                        line.accounting_date.year - 1, 1, 1, 0, 0).date()
                    start_date = line.calculate_weeks_start(start_date)
                    end_date = datetime(
                        line.accounting_date.year, 1, 1, 0, 0).date()
                week = line.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                line.accounting_date_week = week

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    def action_validate(self):
        result = super(StockInventory, self).action_validate()
        if self.accounting_date:
            for move in self.move_ids:
                move.date = self.accounting_date
                for line in move.move_line_ids:
                    line.date = self.accounting_date
        if self.batch_id and self.move_ids:
            for move in self.move_ids:
                for line in move.move_line_ids:
                    line.mother_id = self.batch_id.id
                    ml = self.batch_id.move_line_ids.filtered(
                        lambda c: c.lot_id == line.lot_id and (
                            c.product_id == line.product_id) and (
                                c.location_dest_id == line.location_id))
                    if ml:
                        ml = max(ml, key=lambda x: x.date)
                        line.standard_price = ml.standard_price
                        line.onchange_standard_price()
        return result

    def action_open_inventory_lines(self):
        result = super(StockInventory, self).action_open_inventory_lines()
        if self.accounting_date:
            self.date = self.accounting_date
            for line in self.line_ids:
                line.inventory_date = self.accounting_date
        return result
