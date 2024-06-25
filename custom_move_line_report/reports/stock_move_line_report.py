# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, tools


class StockMoveLineReport(models.Model):
    _name = "stock.move.line.report"
    _description = "Stock Move Line Report"
    _auto = False

    date = fields.Datetime(string="Date", readonly=True)
    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", readonly=True
    )
    lot_id = fields.Many2one(
        string="Lot/Serial Number", comodel_name="stock.production.lot", readonly=True
    )
    location_id = fields.Many2one(
        string="Location", comodel_name="stock.location", readonly=True
    )
    type_id = fields.Many2one(
        string="Location Section", comodel_name="category.type", readonly=True
    )
    product_category_type_id = fields.Many2one(
        string="Product Category Section", comodel_name="category.type", readonly=True
    )
    move_type_id = fields.Many2one(
        string="Move Type", comodel_name="move.type", readonly=True
    )
    type_category_id = fields.Many2one(
        string="Type Category",
        comodel_name="stock.picking.type.category",
        readonly=True,
    )
    batch_id = fields.Many2one(
        string="Egg Mother", comodel_name="stock.picking.batch", readonly=True
    )
    mother_id = fields.Many2one(
        string="Mother", comodel_name="stock.picking.batch", readonly=True
    )
    warehouse_id = fields.Many2one(
        string="Warehouse", comodel_name="stock.warehouse", readonly=True
    )
    company_id = fields.Many2one(
        string="Company", comodel_name="res.company", readonly=True
    )
    qty_done = fields.Float(string="Difference", readonly=True)
    entry_qty = fields.Float(string="Entries", readonly=True)
    output_qty = fields.Float(string="Outputs", readonly=True)
    amount = fields.Float(string="Amount Difference", readonly=True)
    entry_amount = fields.Float(string="Entries Amount", readonly=True)
    output_amount = fields.Float(string="Outputs Amount", readonly=True)
    owner_id = fields.Many2one(
        string="Owner", comodel_name="res.partner", readonly=True
    )
    move_line_id = fields.Many2one(
        string="Move Line", comodel_name="stock.move.line", readonly=True
    )
    move_id = fields.Many2one(string="Move", comodel_name="stock.move", readonly=True)
    picking_id = fields.Many2one(
        string="Picking", comodel_name="stock.picking", readonly=True
    )
    production_id = fields.Many2one(
        string="Production", comodel_name="mrp.production", readonly=True
    )
    egg = fields.Boolean(string="Egg", readonly=True)
    batch_location_id = fields.Many2one(
        string="Mother Location", comodel_name="stock.location", readonly=True
    )
    batch_category_type_id = fields.Many2one(
        string="Batch Section", comodel_name="category.type", readonly=True
    )
    usage = fields.Selection(
        string="Usage", selection="_get_usage_selection", readonly=True
    )
    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", readonly=True
    )
    picking_type_id = fields.Many2one(
        string="Picking Type", comodel_name="stock.picking.type", readonly=True
    )
    ref = fields.Char(string="Reference", readonly=True)

    @api.model
    def _get_usage_selection(self):
        return self.env["stock.location"].fields_get(allfields=["usage"])["usage"][
            "selection"
        ]

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "stock_move_line_report")
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW stock_move_line_report AS (
                SELECT
                    row_number() OVER () AS id,
                    line.move_line_id,
                    line.move_id,
                    line.picking_id,
                    line.picking_type_id,
                    line.ref,
                    line.production_id,
                    line.partner_id,
                    line.product_id,
                    line.product_category_type_id,
                    line.egg,
                    line.lot_id,
                    line.location_id,
                    line.usage,
                    line.type_id,
                    line.move_type_id,
                    line.type_category_id,
                    line.batch_id,
                    line.mother_id,
                    line.batch_location_id,
                    line.batch_category_type_id,
                    line.warehouse_id,
                    line.owner_id,
                    line.date,
                    line.entry_qty,
                    line.output_qty,
                    line.qty_done,
                    line.entry_amount,
                    line.output_amount,
                    line.amount,
                    line.company_id
                    FROM (
                        SELECT
                            stock_move_line.id AS move_line_id,
                            stock_move_line.move_id AS move_id,
                            stock_move_line.picking_id AS picking_id,
                            stock_move_line.picking_type_id AS picking_type_id,
                            stock_move_line.picking_partner_id AS partner_id,
                            stock_move_line.production_id AS production_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.product_category_type_id AS product_category_type_id,
                            stock_move_line.reference AS ref,
                            stock_move_line.egg AS egg,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            location_id.warehouse_id AS warehouse_id,
                            location_origin_id.id AS location_origin_id,
                            location_origin_id.usage AS usage,
                            stock_move_line.move_type_id AS move_type_id,
                            stock_move_line.type_category_id AS type_category_id,
                            stock_move_line.batch_id AS batch_id,
                            stock_move_line.mother_id AS mother_id,
                            stock_move_line.batch_location_id AS batch_location_id,
                            stock_move_line.batch_category_type_id AS batch_category_type_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done * (-1) AS qty_done,
                            0 AS entry_qty,
                            stock_move_line.qty_done * (-1) AS output_qty,
                            stock_move_line.amount * (-1) AS amount,
                            0 AS entry_amount,
                            stock_move_line.amount * (-1) AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.show_in_report AS show_in_report,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN stock_location AS location_origin_id ON
                                stock_move_line.location_id = location_origin_id.id
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.location_id = location_id.id
                        UNION
                        SELECT
                            stock_move_line.id AS move_line_id,
                            stock_move_line.move_id AS move_id,
                            stock_move_line.picking_id AS picking_id,
                            stock_move_line.picking_type_id AS picking_type_id,
                            stock_move_line.picking_partner_id AS partner_id,
                            stock_move_line.production_id AS production_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.product_category_type_id AS product_category_type_id,
                            stock_move_line.reference AS ref,
                            stock_move_line.egg AS egg,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            location_id.warehouse_id AS warehouse_id,
                            location_origin_id.id AS location_origin_id,
                            location_origin_id.usage AS usage,
                            stock_move_line.move_type_id AS move_type_id,
                            stock_move_line.type_category_id AS type_category_id,
                            stock_move_line.batch_id AS batch_id,
                            stock_move_line.mother_id AS mother_id,
                            stock_move_line.batch_location_id AS batch_location_id,
                            stock_move_line.batch_category_type_id AS batch_category_type_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done AS qty_done,
                            stock_move_line.qty_done AS entry_qty,
                            0 AS output_qty,
                            stock_move_line.amount AS amount,
                            stock_move_line.amount AS entry_amount,
                            0 AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.show_in_report AS show_in_report,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN stock_location AS location_origin_id ON
                                stock_move_line.location_id = location_origin_id.id
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.location_dest_id = location_id.id
                        UNION
                        SELECT
                            stock_move_line.id AS move_line_id,
                            stock_move_line.move_id AS move_id,
                            stock_move_line.picking_id AS picking_id,
                            stock_move_line.picking_type_id AS picking_type_id,
                            stock_move_line.picking_partner_id AS partner_id,
                            stock_move_line.production_id AS production_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.product_category_type_id AS product_category_type_id,
                            stock_move_line.reference AS ref,
                            stock_move_line.egg AS egg,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            location_id.warehouse_id AS warehouse_id,
                            location_origin_id.id AS location_origin_id,
                            location_origin_id.usage AS usage,
                            stock_move_line.move_type_id AS move_type_id,
                            '2' AS type_category_id,
                            stock_move_line.batch_id AS batch_id,
                            stock_move_line.mother_id AS mother_id,
                            stock_move_line.batch_location_id AS batch_location_id,
                            stock_move_line.batch_category_type_id AS batch_category_type_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done * (-1) AS qty_done,
                            0 AS entry_qty,
                            stock_move_line.qty_done * (-1) AS output_qty,
                            stock_move_line.amount * (-1) AS amount,
                            0 AS entry_amount,
                            stock_move_line.amount * (-1) AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.show_in_report AS show_in_report,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.batch_location_id = location_id.id
                        JOIN stock_location AS location_origin_id ON
                                stock_move_line.location_id = location_origin_id.id
                        WHERE
                            location_origin_id.usage = 'production' AND
                            stock_move_line.batch_id IS NOT NULL
                        UNION
                        SELECT
                            stock_move_line.id AS move_line_id,
                            stock_move_line.move_id AS move_id,
                            stock_move_line.picking_id AS picking_id,
                            stock_move_line.picking_type_id AS picking_type_id,
                            stock_move_line.production_id AS production_id,
                            stock_move_line.picking_partner_id AS partner_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.product_category_type_id AS product_category_type_id,
                            stock_move_line.reference AS ref,
                            stock_move_line.egg AS egg,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            location_id.warehouse_id AS warehouse_id,
                            location_origin_id.id AS location_origin_id,
                            location_origin_id.usage AS usage,
                            stock_move_line.move_type_id AS move_type_id,
                            '8' AS type_category_id,
                            stock_move_line.batch_id AS batch_id,
                            stock_move_line.mother_id AS mother_id,
                            stock_move_line.batch_location_id AS batch_location_id,
                            stock_move_line.batch_category_type_id AS batch_category_type_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done AS qty_done,
                            stock_move_line.qty_done AS entry_qty,
                            0 AS output_qty,
                            stock_move_line.amount AS amount,
                            stock_move_line.amount AS entry_amount,
                            0 AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.show_in_report AS show_in_report,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.batch_location_id = location_id.id
                        JOIN stock_location AS location_origin_id ON
                                stock_move_line.location_id = location_origin_id.id
                        WHERE
                            location_origin_id.usage = 'production' AND
                            stock_move_line.batch_id IS NOT NULL
                    ) AS line
                    WHERE
                        line.state = 'done' AND
                        line.qty_done IS NOT NULL AND
                        (line.show_in_report IS TRUE OR line.picking_id IS NULL)
            )
        """
        )
