# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import tools
from odoo import api, fields, models


class StockMoveLineReport(models.Model):
    _name = "stock.move.line.report"
    _description = "Stock Move Line Report"
    _auto = False

    date = fields.Datetime(
        string="Date")
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product")
    lot_id = fields.Many2one(
        string="Lot/Serial Number",
        comodel_name="stock.production.lot")
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location")
    type_id = fields.Many2one(
        string="Section",
        comodel_name="category.type")
    move_type_id = fields.Many2one(
        string="Move Type",
        comodel_name="move.type")
    type_category_id = fields.Many2one(
        string="Type Category",
        comodel_name="stock.picking.type.category")
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse")
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company")
    qty_done = fields.Float(
        string="Difference")
    entry_qty = fields.Float(
        string="Entries")
    output_qty = fields.Float(
        string="Outputs")
    amount = fields.Float(
        string="Amount Difference")
    entry_amount = fields.Float(
        string="Entries Amount")
    output_amount = fields.Float(
        string="Outputs Amount")
    owner_id = fields.Many2one(
        string="Owner",
        comodel_name="res.partner")
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="stock.move.line")
    move_id = fields.Many2one(
        string="Move",
        comodel_name="stock.move")
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking")
    production_id = fields.Many2one(
        string="Production",
        comodel_name="mrp.production")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'stock_move_line_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW stock_move_line_report AS (
                SELECT
                    row_number() OVER () AS id,
                    line.move_line_id,
                    line.move_id,
                    line.picking_id,
                    line.production_id,
                    line.product_id,
                    line.lot_id,
                    line.location_id,
                    line.type_id,
                    line.move_type_id,
                    line.type_category_id,
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
                            stock_move_line.production_id AS production_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            stock_move_line.move_type_id AS move_type_id,
                            stock_move_line.type_category_id AS type_category_id,
                            location_id.warehouse_id AS warehouse_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done * (-1) AS qty_done,
                            0 AS entry_qty,
                            stock_move_line.qty_done * (-1) AS output_qty,
                            stock_move_line.amount * (-1) AS amount,
                            0 AS entry_amount,
                            stock_move_line.amount * (-1) AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.location_id = location_id.id
                        UNION
                        SELECT
                            stock_move_line.id AS move_line_id,
                            stock_move_line.move_id AS move_id,
                            stock_move_line.picking_id AS picking_id,
                            stock_move_line.production_id AS production_id,
                            stock_move_line.product_id AS product_id,
                            stock_move_line.date AS date,
                            stock_move_line.lot_id AS lot_id,
                            location_id.id AS location_id,
                            location_id.type_id AS type_id,
                            stock_move_line.move_type_id AS move_type_id,
                            stock_move_line.type_category_id AS type_category_id,
                            location_id.warehouse_id AS warehouse_id,
                            stock_move_line.owner_id AS owner_id,
                            stock_move_line.qty_done AS qty_done,
                            stock_move_line.qty_done AS entry_qty,
                            0 AS output_qty,
                            stock_move_line.amount AS amount,
                            stock_move_line.amount AS entry_amount,
                            0 AS output_amount,
                            stock_move_line.state AS state,
                            stock_move_line.company_id AS company_id
                        FROM
                        stock_move_line
                        JOIN
                            stock_location AS location_id ON
                               stock_move_line.location_dest_id = location_id.id
                    ) AS line
                    WHERE
                        line.state = 'done' AND
                        line.qty_done IS NOT NULL
            )
        """)

