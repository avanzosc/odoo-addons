# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MotherLineageRelation(models.Model):
    _inherit = "mother.lineage.relation"

    entry_date = fields.Date(
        string="Entry Date", related="breeding_id.entry_date", store=True
    )
    cleaned_date = fields.Date(
        string="Cleaned Date", related="breeding_id.cleaned_date", store=True
    )
    warehouse_id = fields.Many2one(
        string="Farm",
        comodel_name="stock.warehouse",
        related="breeding_id.warehouse_id",
        store=True,
    )
    city = fields.Char(string="City", related="breeding_id.city", store=True)
    chick_entry_qty = fields.Float(
        string="Chick Entry Qty", compute="_compute_chick_entry_qty", store=True
    )
    output_units = fields.Float(
        string="Output Units", compute="_compute_output_units", store=True
    )
    cancellation_percentage = fields.Float(
        string="Cancellation Percentage",
        related="breeding_id.cancellation_percentage",
        store=True,
    )
    density = fields.Float(string="Density", related="breeding_id.density", store=True)
    growth_speed = fields.Float(
        string="Growth Speed", related="breeding_id.growth_speed", store=True
    )
    feed = fields.Integer(string="Feep", related="breeding_id.feed", store=True)
    meat_kilos = fields.Float(
        string="Meat Kilos", compute="_compute_meat_kilos", store=True
    )
    consume_feed = fields.Float(
        string="Consume Feed", compute="_compute_consume_feed", store=True
    )
    feed_family = fields.Many2one(
        string="Feed Family",
        comodel_name="breeding.feed",
        related="breeding_id.feed_family",
        store=True,
    )
    average_age = fields.Float(
        string="Average Age", related="breeding_id.average_age", store=True
    )
    farm_day = fields.Integer(
        string="Farm Day", related="breeding_id.farm_day", store=True
    )
    average_weight = fields.Float(
        string="Average Weight", related="breeding_id.average_weight", store=True
    )
    conversion = fields.Float(
        string="Conversion", related="breeding_id.conversion", store=True
    )
    dif_weight = fields.Float(
        string="Dif.", related="breeding_id.dif_weight", store=True
    )
    liquidation_amount = fields.Float(
        string="Liquidation Amount", compute="_compute_liquidation_amount", store=True
    )
    chick_liquidation = fields.Float(
        string="Chick Liquidation", related="breeding_id.chick_liquidation", store=True
    )
    liquidation_area = fields.Float(
        string="Liquidation Area", related="breeding_id.liquidation_area", store=True
    )
    cost_kilo = fields.Float(
        string="Cost Kilo", related="breeding_id.cost_kilo", store=True
    )
    liquidated = fields.Boolean(
        string="Liquidated", related="breeding_id.liquidated", store=True
    )
    billed = fields.Boolean(string="Billed", related="breeding_id.billed", store=True)
    closed = fields.Boolean(string="Closed", related="breeding_id.closed", store=True)
    output_amount_days = fields.Float(
        string="Output Amount Days", compute="_compute_output_amount_days", store=True
    )
    output_feed_amount = fields.Float(
        string="Output Feed Amount", compute="_compute_output_feed_amount", store=True
    )
    medicine_amount = fields.Float(
        string="Medicine Amount", compute="_compute_medicine_amount", store=True
    )
    warehouse_area = fields.Float(
        string="Warehouse Area", compute="_compute_warehouse_area", store=True
    )
    age_output = fields.Float(
        string="Age Output", compute="_compute_age_output", store=True
    )

    @api.depends("breeding_id", "breeding_id.age_output", "percentage")
    def _compute_age_output(self):
        for line in self:
            age_output = 0
            if line.breeding_id:
                age_output = (line.breeding_id.age_output * line.percentage) / 100
            line.age_output = age_output

    @api.depends("breeding_id", "breeding_id.warehouse_area", "percentage")
    def _compute_warehouse_area(self):
        for line in self:
            warehouse_area = 0
            if line.breeding_id:
                warehouse_area = (
                    line.breeding_id.warehouse_area * line.percentage
                ) / 100
            line.warehouse_area = warehouse_area

    @api.depends("breeding_id", "breeding_id.output_feed_amount", "percentage")
    def _compute_output_feed_amount(self):
        for line in self:
            qty = 0
            if line.breeding_id:
                qty = (line.breeding_id.output_feed_amount * line.percentage) / 100
            line.output_feed_amount = qty

    @api.depends("breeding_id", "breeding_id.chick_entry_qty", "percentage")
    def _compute_chick_entry_qty(self):
        for line in self:
            qty = 0
            if line.breeding_id:
                qty = line.breeding_id.chick_entry_qty * line.percentage / 100
            line.chick_entry_qty = qty

    @api.depends("breeding_id", "breeding_id.output_units", "percentage")
    def _compute_output_units(self):
        for line in self:
            unit = 0
            if line.breeding_id:
                unit = line.breeding_id.output_units * line.percentage / 100
            line.output_units = unit

    @api.depends("breeding_id", "breeding_id.meat_kilos", "percentage")
    def _compute_meat_kilos(self):
        for line in self:
            meat = 0
            if line.breeding_id:
                meat = (line.breeding_id.meat_kilos * line.percentage) / 100
            line.meat_kilos = meat

    @api.depends("breeding_id", "breeding_id.output_amount_days", "percentage")
    def _compute_output_amount_days(self):
        for line in self:
            amount = 0
            if line.breeding_id:
                amount = (line.breeding_id.output_amount_days * line.percentage) / 100
            line.output_amount_days = amount

    @api.depends("breeding_id", "breeding_id.consume_feed", "percentage")
    def _compute_consume_feed(self):
        for line in self:
            feed = 0
            if line.breeding_id:
                feed = (line.breeding_id.consume_feed * line.percentage) / 100
            line.consume_feed = feed

    @api.depends("breeding_id", "breeding_id.medicine_qty", "percentage")
    def _compute_medicine_amount(self):
        for line in self:
            medicine = 0
            if line.breeding_id:
                medicine = (
                    line.breeding_id.output_medicine_amount * line.percentage
                ) / 100
            line.medicine_amount = medicine

    @api.depends("breeding_id", "breeding_id.liquidation_amount", "percentage")
    def _compute_liquidation_amount(self):
        for line in self:
            amount = 0
            if line.breeding_id:
                amount = (line.breeding_id.liquidation_amount * line.percentage) / 100
            line.liquidation_amount = amount

    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        result = super().read_group(
            domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
        )
        for line in result:
            if "__domain" in line:
                cancellation = 0
                density = 0
                growth_spped = 0
                feed = 0
                age = 0
                day = 0
                avg_wight = 0
                conversion = 0
                dif = 0
                chick_liq = 0
                liq_area = 0
                cost_kilo = 0
                aux = 0
                lines = self.search(line["__domain"])
                for x in lines:
                    cancellation += x.cancellation_percentage
                    density += x.density
                    growth_spped += x.growth_speed
                    feed += x.feed
                    age += x.average_age
                    day += x.farm_day
                    avg_wight += x.average_weight
                    conversion += x.conversion
                    dif += x.dif_weight
                    chick_liq += x.chick_liquidation
                    liq_area += x.liquidation_area
                    cost_kilo += x.cost_kilo
                    aux += 1
                total_cancellation = cancellation / aux
                total_density = density / aux
                total_growth_speed = growth_spped / aux
                total_feed = feed / aux
                total_age = age / aux
                total_day = day / aux
                total_avg_weight = avg_wight / aux
                total_conversion = conversion / aux
                total_dif = dif / aux
                total_liq_area = liq_area / aux
                total_chick_liq = chick_liq / aux
                total_cost_kilo = cost_kilo / aux
                line["cancellation_percentage"] = total_cancellation
                line["density"] = total_density
                line["growth_speed"] = total_growth_speed
                line["feed"] = total_feed
                line["average_age"] = total_age
                line["farm_day"] = total_day
                line["average_weight"] = total_avg_weight
                line["conversion"] = total_conversion
                line["dif_weight"] = total_dif
                line["chick_liquidation"] = total_chick_liq
                line["liquidation_area"] = total_liq_area
                line["cost_kilo"] = total_cost_kilo
            else:
                fields.remove("cancellation_percentage")
                fields.remove("density")
        return result
