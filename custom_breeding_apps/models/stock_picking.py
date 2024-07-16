# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from dateutil import rrule
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _default_custom_date_done(self):
        result = False
        if "default_company_id" in self.env.context and not (
            self.env["res.company"]
            .search([("id", "=", self.env.context["default_company_id"])], limit=1)
            .tolvasa
        ):
            result = fields.Datetime.now()
        return result

    is_incubator = fields.Boolean(
        string="Incubator", compute="_compute_type", store=True
    )
    is_integration = fields.Boolean(
        string="Integration", compute="_compute_type", store=True
    )
    is_reproductor = fields.Boolean(
        string="Reproductor", compute="_compute_type", store=True
    )
    is_feed_flour = fields.Boolean(
        string="Feed/Flour", compute="_compute_type", store=True
    )
    is_medicine = fields.Boolean(string="Medicine", compute="_compute_type", store=True)
    egg_production = fields.Boolean(
        string="Is Egg Production", related="picking_type_id.egg_production", store=True
    )
    burden_to_incubator = fields.Boolean(
        string="Is Burden to Incubator",
        related="picking_type_id.burden_to_incubator",
        store=True,
    )
    incubator_hatcher = fields.Boolean(
        string="Form Incubator to Hatchers",
        related="picking_type_id.incubator_hatcher",
        store=True,
    )
    birth_estimate_date = fields.Date(string="Birth Estimate Date")
    date_done_week = fields.Integer(
        string="Date Done Weeks", compute="_compute_date_done_week", store=True
    )
    date_birth_week = fields.Integer(
        string="Date Birth Weeks", compute="_compute_date_birth_week", store=True
    )
    distribution_ids = fields.One2many(
        string="Distribution",
        comodel_name="distribution.line",
        inverse_name="picking_id",
    )
    pending_qty = fields.Integer(
        string="Pending Qty", compute="_compute_pending_qty", store=True
    )
    birth_estimate_qty = fields.Integer(
        string="Birth Estimate Qty", compute="_compute_birth_estimate_qty", store=True
    )
    distribution_count = fields.Integer(
        string="Distributions", compute="_compute_distribution_count", store=True
    )
    custom_date_done = fields.Datetime(default=_default_custom_date_done)

    @api.depends("distribution_ids")
    def _compute_distribution_count(self):
        for line in self:
            line.distribution_count = len(line.distribution_ids)

    @api.depends(
        "move_line_ids_without_package",
        "move_line_ids_without_package.birth_estimate_qty",
    )
    def _compute_birth_estimate_qty(self):
        for line in self:
            line.birth_estimate_qty = sum(
                line.move_line_ids_without_package.mapped("birth_estimate_qty")
            )

    @api.depends(
        "move_line_ids_without_package",
        "move_line_ids_without_package.birth_estimate_qty",
        "distribution_ids",
        "distribution_ids.distribute_qty",
    )
    def _compute_pending_qty(self):
        for line in self:
            line.pending_qty = line.birth_estimate_qty - (
                sum(line.distribution_ids.mapped("distribute_qty"))
            )

    @api.depends("birth_estimate_date")
    def _compute_date_birth_week(self):
        for line in self:
            date_birth_week = 0
            if line.birth_estimate_date:
                start_date = datetime(line.birth_estimate_date.year, 1, 1, 0, 0).date()
                start_date = line.calculate_weeks_start(start_date)
                end_date = line.birth_estimate_date
                if end_date < start_date:
                    start_date = datetime(
                        line.birth_estimate_date.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = line.calculate_weeks_start(start_date)
                    end_date = datetime(
                        line.birth_estimate_date.year, 1, 1, 0, 0
                    ).date()
                week = line.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                date_birth_week = week
            line.date_birth_week = date_birth_week

    @api.depends("custom_date_done")
    def _compute_date_done_week(self):
        for line in self:
            date_done_week = 0
            if line.custom_date_done:
                start_date = datetime(line.custom_date_done.year, 1, 1, 0, 0)
                start_date = line.calculate_weeks_start(start_date)
                end_date = line.custom_date_done
                if end_date < start_date:
                    start_date = datetime(
                        line.custom_date_done.year - 1, 1, 1, 0, 0
                    ).date()
                    start_date = line.calculate_weeks_start(start_date)
                    end_date = datetime(line.custom_date_done.year, 1, 1, 0, 0).date()
                week = line.weeks_between(start_date, end_date)
                if week == 53:
                    week = 1
                date_done_week = week
            line.date_done_week = date_done_week

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()

    @api.depends("category_type_id", "dest_category_type_id")
    def _compute_type(self):
        for line in self:
            is_incubator = False
            is_integration = False
            is_reproductor = False
            is_feed_flour = False
            is_medicine = False
            reproductor = self.env.ref("stock_warehouse_farm.categ_type1")
            integration = self.env.ref("stock_warehouse_farm.categ_type2")
            medicine = self.env.ref("stock_warehouse_farm.categ_type3")
            feed = self.env.ref("stock_warehouse_farm.categ_type4")
            flour = self.env.ref("stock_warehouse_farm.categ_type5")
            incubator = self.env.ref("stock_warehouse_farm.categ_type6")
            if (line.category_type_id == reproductor) or (
                line.dest_category_type_id == reproductor
            ):
                is_reproductor = True
            if (line.category_type_id == integration) or (
                line.dest_category_type_id == integration
            ):
                is_integration = True
            if (line.category_type_id == medicine) or (
                line.dest_category_type_id == medicine
            ):
                is_medicine = True
            if (line.category_type_id in (feed, flour)) or (
                line.dest_category_type_id in (feed, flour)
            ):
                is_feed_flour = True
            if (line.category_type_id == incubator) or (
                line.dest_category_type_id == incubator
            ):
                is_incubator = True
            line.is_incubator = is_incubator
            line.is_integration = is_integration
            line.is_reproductor = is_reproductor
            line.is_feed_flour = is_feed_flour
            line.is_medicine = is_medicine

    @api.onchange("custom_date_done")
    def onchange_custom_date_done(self):
        if self.custom_date_done:
            self.birth_estimate_date = self.custom_date_done.date() + relativedelta(
                days=21
            )

    @api.onchange("location_id")
    def _onchange_location_id(self):
        if self.location_id and self.move_line_ids_without_package:
            for move in self.move_ids_without_package:
                move.location_id = self.location_id.id
            for line in self.move_line_ids_without_package:
                line.location_id = self.location_id.id

    @api.onchange("location_dest_id")
    def _onchange_location_dest_id(self):
        if self.location_dest_id and self.move_line_ids_without_package:
            for move in self.move_ids_without_package:
                move.location_dest_id = self.location_dest_id.id
            for line in self.move_line_ids_without_package:
                line.location_dest_id = self.location_dest_id.id

    def action_view_distribution(self):
        context = self.env.context.copy()
        context.update({"default_picking_id": self.id})
        return {
            "name": _("Distributions"),
            "view_mode": "tree",
            "res_model": "distribution.line",
            "domain": [("id", "in", self.distribution_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }

    def calculate_weeks_start(self, start_date):
        self.ensure_one()
        weekday = start_date.weekday()
        if weekday <= 3:
            return start_date - timedelta(days=weekday)
        else:
            return start_date + timedelta(days=(7 - weekday))

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        unit = self.env.ref("uom.product_uom_unit")
        for picking in self:
            for line in picking.move_line_ids_without_package:
                if line.product_uom_id == unit:
                    line.download_unit = line.qty_done
        return result

    def button_validate(self):
        for picking in self:
            if not picking.company_id.tolvasa and not picking.custom_date_done:
                picking.custom_date_done = fields.Datetime.now()
            if picking.picking_type_id.burden_to_incubator and (
                picking.pending_qty != 0
                or (picking.pending_qty == 0 and not picking.distribution_ids)
            ):
                raise ValidationError(
                    _(
                        "The distribution is not complete, there are "
                        + "still pending amounts."
                    )
                )
        return super().button_validate()
