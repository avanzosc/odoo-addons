# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools
from odoo.addons import decimal_precision as dp
from psycopg2.extensions import AsIs


class StockReport(models.Model):
    _name = "stock.data.report"
    _description = "Report for Stock Data"
    _auto = False

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product", index=True)
    lot_id = fields.Many2one(
        comodel_name="stock.production.lot", string="Lot", index=True)
    package_id = fields.Many2one(
        comodel_name="stock.quant.package", string="Package", index=True)
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="Unit of Measure", index=True)
    product_uom_qty = fields.Float(
        string="Reserved", default=0.0,
        digits=dp.get_precision("Product Unit of Measure"))
    location_id = fields.Many2one(
        comodel_name="stock.location", string="From")
    location_dest_id = fields.Many2one(
        comodel_name="stock.location", string="To")
    state = fields.Selection([
        ("draft", "New"), ("cancel", "Cancelled"),
        ("waiting", "Waiting Another Move"),
        ("confirmed", "Waiting Availability"),
        ("partially_available", "Partially Available"),
        ("assigned", "Available"),
        ("done", "Done")], string="Status")
    commercial_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Commercial Entity", index=True)
    sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Sale Order", index=True)
    sale_price_unit = fields.Float(
        string="Sale Unit Price", digits=dp.get_precision("Product Price"),
        default=0.0)
    sale_discount = fields.Float(
        string="Sale Discount (%)", digits=dp.get_precision('Discount'),
        default=0.0)
    sale_amount = fields.Float()
    sale_discount_amount = fields.Float()
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order", string="Purchase Order", index=True)
    purchase_price_unit = fields.Float(
        string="Purchase Unit Price", digits=dp.get_precision('Product Price'),
        default=0.0)
    purchase_discount = fields.Float(
        string="Purchase Discount (%)", digits=dp.get_precision('Discount'),
        default=0.0)
    purchase_amount = fields.Float()
    purchase_discount_amount = fields.Float()
    margin_amount = fields.Float()
    margin_discount_amount = fields.Float()

    def _select(self):
        select_str = """
            SELECT
                row_number() OVER () as id,
                ml.product_id as product_id,
                ml.lot_id as lot_id,
                ml.package_id as package_id,
                ml.product_uom_id as product_uom_id,
                sum(ml.product_uom_qty + ml.qty_done) as product_uom_qty,
                ml.location_id as location_id,
                ml.location_dest_id as location_dest_id,
                m.state as state,
                p.commercial_partner_id as commercial_partner_id,
                sl.order_id as sale_order_id,
                sl.price_unit as sale_price_unit,
                sl.discount as sale_discount,
                (sl.price_unit * sum(ml.product_uom_qty + ml.qty_done))
                    as sale_amount,
                ((1 - (sl.discount/100)) *
                 (sl.price_unit * sum(ml.product_uom_qty + ml.qty_done)))
                    as sale_discount_amount,
                pl.order_id as purchase_order_id,
                pl.price_unit as purchase_price_unit,
                pl.discount as purchase_discount,
                (pl.price_unit * sum(ml.product_uom_qty + ml.qty_done))
                    as purchase_amount,
                ((1 - (pl.discount/100)) *
                 (pl.price_unit * sum(ml.product_uom_qty + ml.qty_done)))
                    as purchase_discount_amount,
                ((sl.price_unit - pl.price_unit) *
                 sum(ml.product_uom_qty + ml.qty_done)) as margin_amount,
                ((((1 - (sl.discount/100)) * sl.price_unit) -
                  ((1 - (pl.discount/100)) * pl.price_unit)) *
                 sum(ml.product_uom_qty + ml.qty_done))
                    as margin_discount_amount
        """
        return select_str

    def _from(self):
        from_str = """
            FROM stock_move_line ml
            JOIN stock_move m ON m.id = ml.move_id
            JOIN stock_picking sp ON sp.id = m.picking_id
            JOIN res_partner p ON p.id = sp.partner_id
            LEFT JOIN sale_order_line sl ON sl.id = m.sale_line_id
            LEFT JOIN purchase_order_line pl ON pl.id = m.purchase_line_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                ml.id,
                ml.product_id,
                ml.lot_id,
                ml.package_id,
                ml.product_uom_id,
                ml.move_id,
                ml.location_id,
                ml.location_dest_id,
                m.state,
                m.picking_id,
                sp.partner_id,
                p.commercial_partner_id,
                sl.order_id,
                sl.price_unit,
                sl.discount,
                pl.order_id,
                pl.price_unit,
                pl.discount
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s
                %s
                %s
                )""", (
                AsIs(self._table), AsIs(self._select()),
                AsIs(self._from()), AsIs(self._group_by())))
