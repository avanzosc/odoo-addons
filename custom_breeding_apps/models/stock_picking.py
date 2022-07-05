# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from datetime import datetime
from dateutil import rrule
from dateutil.relativedelta import relativedelta


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_incubator = fields.Boolean(
        string="Incubator", compute="_compute_type", store=True)
    is_integration = fields.Boolean(
        string="Integration", compute="_compute_type", store=True)
    is_reproductor = fields.Boolean(
        string="Reproductor", compute="_compute_type", store=True)
    is_feed_flour = fields.Boolean(
        string="Feed/Flour", compute="_compute_type", store=True)
    is_medicine = fields.Boolean(
        string="Medicine", compute="_compute_type", store=True)
    egg_production = fields.Boolean(
        string="Is Egg Production",
        related="picking_type_id.egg_production",
        store=True)
    burden_to_incubator = fields.Boolean(
        string="Is Burden to Incubator",
        related="picking_type_id.burden_to_incubator",
        store=True)
    birth_estimate_date = fields.Date(string="Birth Estimate Date")
    date_done_week = fields.Integer(
        string="Date Done Weeks",
        compute="_compute_date_done_week",
        store=True)
    date_birth_week = fields.Integer(
        string="Date Birth Weeks",
        compute="_compute_date_birth_week",
        store=True)
    distribution_ids = fields.One2many(
        string="Distribution",
        comodel_name="distribution.line",
        inverse_name="picking_id")
    pending_qty = fields.Float(
        string="Pending Qty",
        compute="_compute_pending_qty",
        store=True)
    birth_estimate_qty = fields.Float(
        string="Birth Estimate Qty",
        compute="_compute_birth_estimate_qty",
        store=True)
    distribution_count = fields.Integer(
        string="Distributions",
        compute="_compute_distribution_count",
        store=True)

    @api.depends("distribution_ids")
    def _compute_distribution_count(self):
        for line in self:
            line.distribution_count = len(line.distribution_ids)

    @api.depends("move_line_ids_without_package",
                 "move_line_ids_without_package.birth_estimate_qty")
    def _compute_birth_estimate_qty(self):
        for line in self:
            line.birth_estimate_qty = (
                sum(line.move_line_ids_without_package.mapped(
                    "birth_estimate_qty")))

    @api.depends("move_line_ids_without_package",
                 "move_line_ids_without_package.birth_estimate_qty",
                 "distribution_ids", "distribution_ids.distribute_qty")
    def _compute_pending_qty(self):
        for line in self:
            line.pending_qty = (line.birth_estimate_qty - (
                sum(line.distribution_ids.mapped("distribute_qty"))))

    @api.depends("birth_estimate_date")
    def _compute_date_birth_week(self):
        for line in self:
            line.date_birth_week = 0
            if line.birth_estimate_date:
                start_date = datetime(
                    line.birth_estimate_date.year, 1, 1, 0, 0)
                end_date = line.birth_estimate_date
                line.date_birth_week = (
                    line.weeks_between(start_date, end_date))

    @api.depends("custom_date_done")
    def _compute_date_done_week(self):
        for line in self:
            line.date_done_week = 0
            if line.custom_date_done:
                start_date = datetime(
                    line.custom_date_done.year, 1, 1, 0, 0)
                end_date = line.custom_date_done
                line.date_done_week = (
                    line.weeks_between(start_date, end_date))

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.depends("category_type_id", "dest_category_type_id")
    def _compute_type(self):
        for line in self:
            line.is_incubator = False
            line.is_integration = False
            line.is_reproductor = False
            line.is_feed_flour = False
            line.is_medicine = False
            reproductor = self.env.ref("stock_warehouse_farm.categ_type1")
            integration = self.env.ref("stock_warehouse_farm.categ_type2")
            medicine = self.env.ref("stock_warehouse_farm.categ_type3")
            feed = self.env.ref("stock_warehouse_farm.categ_type4")
            flour = self.env.ref("stock_warehouse_farm.categ_type5")
            incubator = self.env.ref("stock_warehouse_farm.categ_type6")
            if (
                line.category_type_id == reproductor) or (
                    line.dest_category_type_id == reproductor):
                line.is_reproductor = True
            if (
                line.category_type_id == integration) or (
                    line.dest_category_type_id == integration):
                line.is_integration = True
            if (
                line.category_type_id == medicine) or (
                    line.dest_category_type_id == medicine):
                line.is_medicine = True
            if (
                line.category_type_id in (feed, flour)) or (
                    line.dest_category_type_id in (feed, flour)):
                line.is_feed_flour = True
            if (
                line.category_type_id == incubator) or (
                    line.dest_category_type_id == incubator):
                line.is_incubator = True

    @api.onchange("custom_date_done")
    def onchange_custom_date_done(self):
        if self.custom_date_done:
            self.birth_estimate_date = (
                self.custom_date_done.date() + relativedelta(days=21))

    def action_view_distribution(self):
        context = self.env.context.copy()
        context.update({'default_picking_id': self.id})
        return {
            "name": _("Distributions"),
            "view_mode": "tree",
            "res_model": "distribution.line",
            "domain": [("id", "in", self.distribution_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }
