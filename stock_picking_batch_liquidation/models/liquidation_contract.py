# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class LiquidationContract(models.Model):
    _name = "liquidation.contract"
    _description = "Liquidation Contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True)
    chicken_load = fields.Float(
        string="Chicken Load", digits="Chicken Load Decimal Precision"
    )
    correction_factor = fields.Float(string="Correction Factor")
    initial_feed = fields.Integer(string="Initial FEEP")
    final_feed = fields.Integer(string="Final FEEP")
    feed_ratio = fields.Float(string="FEEP Ratio", digits="Feep Decimal Precision")
    feed_inital_price = fields.Float(
        string="FEEP Initial Price", digits="Feep Decimal Precision"
    )
    feed_rate_ids = fields.One2many(
        string="FEEP Rate", comodel_name="feed.rate", inverse_name="contract_id"
    )
    contract_line_ids = fields.One2many(
        string="Contract Lines",
        comodel_name="liquidation.contract.line",
        inverse_name="contract_id",
        copy=True,
    )
    liquidation_min = fields.Float(string="Min. to be Liquidated per Chicken")
    liquidation_max = fields.Float(string="Max. to be Liquidated per Chicken")
    invoice_product_id = fields.Many2one(
        string="Product to Invoice", comodel_name="product.product"
    )
    overhead = fields.Float(string="Overhead")

    def action_create_feed_rate(self):
        self.ensure_one()
        self.feed_rate_ids.unlink()
        if (
            not self.initial_feed
            or not (self.final_feed)
            or not self.feed_ratio
            or not (self.feed_inital_price)
        ):
            raise ValidationError(
                _(
                    "some of the data required for the calculation of "
                    + "the FEEP ratio are missing."
                )
            )
        else:
            start = self.initial_feed
            end = self.final_feed
            ratio = self.feed_ratio
            price = self.feed_inital_price
            while start <= end:
                self.feed_rate_ids.create(
                    {"feed": start, "price": price, "contract_id": self.id}
                )
                start += 1
                price += ratio
