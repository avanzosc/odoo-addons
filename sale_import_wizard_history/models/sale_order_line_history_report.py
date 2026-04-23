# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SaleOrderLineHistoryReport(models.Model):
    _name = "sale.order.line.history.report"
    _description = "Sale Order Line History Report"
    _auto = False
    _rec_name = "order_name"
    _order = "date_order_missing asc, date_order desc, id desc"

    source = fields.Selection(
        selection=[("sale", "Sale"), ("historical", "Historical")],
        readonly=True,
    )
    historical = fields.Boolean(readonly=True)
    line_id = fields.Integer(readonly=True)
    order_id = fields.Many2one(comodel_name="sale.order", readonly=True)
    import_id = fields.Many2one(comodel_name="sale.order.import", readonly=True)
    order_name = fields.Char(readonly=True)
    client_order_ref = fields.Char(readonly=True)
    partner_id = fields.Many2one(comodel_name="res.partner", readonly=True)
    commercial_partner_id = fields.Many2one(comodel_name="res.partner", readonly=True)
    product_id = fields.Many2one(comodel_name="product.product", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", readonly=True)
    currency_id = fields.Many2one(comodel_name="res.currency", readonly=True)
    date_order = fields.Date(readonly=True)
    date_order_missing = fields.Integer(
        readonly=True,
        aggregator=False,
    )
    file_date = fields.Date(readonly=True)
    state = fields.Char(readonly=True)
    quantity = fields.Float(readonly=True)
    price_unit = fields.Float(readonly=True)
    discount = fields.Float(readonly=True)
    subtotal = fields.Float(readonly=True)
    total = fields.Float(readonly=True)

    def _select_sale_lines(self):
        return """
            SELECT
                sol.id AS id,
                'sale'::varchar AS source,
                FALSE AS historical,
                sol.id AS line_id,
                so.id AS order_id,
                so.sale_import_id AS import_id,
                so.name AS order_name,
                so.client_order_ref AS client_order_ref,
                so.partner_id AS partner_id,
                rp.commercial_partner_id AS commercial_partner_id,
                sol.product_id AS product_id,
                so.company_id AS company_id,
                so.currency_id AS currency_id,
                so.date_order::date AS date_order,
                CASE WHEN so.date_order IS NULL THEN 1 ELSE 0 END AS date_order_missing,
                soi.file_date AS file_date,
                so.state AS state,
                sol.product_uom_qty AS quantity,
                sol.price_unit AS price_unit,
                sol.discount AS discount,
                sol.price_subtotal AS subtotal,
                sol.price_total AS total
            FROM sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
            LEFT JOIN sale_order_import soi ON soi.id = so.sale_import_id
            LEFT JOIN res_partner rp ON rp.id = so.partner_id
        """

    def _select_historical_lines(self):
        return """
            SELECT
                -sil.id AS id,
                'historical'::varchar AS source,
                TRUE AS historical,
                sil.id AS line_id,
                NULL::integer AS order_id,
                si.id AS import_id,
                COALESCE(
                    NULLIF(sil.order_name, ''),
                    NULLIF(sil.client_order_ref, ''),
                    NULLIF(si.filename, ''),
                    ('IMPORT-' || si.id::varchar)
                ) AS order_name,
                sil.client_order_ref AS client_order_ref,
                sil.customer_id AS partner_id,
                rp.commercial_partner_id AS commercial_partner_id,
                sil.product_id AS product_id,
                si.company_id AS company_id,
                company.currency_id AS currency_id,
                sil.date_order AS date_order,
                CASE
                    WHEN sil.date_order IS NULL THEN 1
                    ELSE 0
                END AS date_order_missing,
                si.file_date AS file_date,
                sil.state AS state,
                sil.quantity AS quantity,
                sil.price_unit AS price_unit,
                sil.discount AS discount,
                COALESCE(
                    NULLIF(sil.line_subtotal_amount, 0),
                    (sil.quantity * sil.price_unit)
                ) AS subtotal,
                COALESCE(
                    NULLIF(sil.item_total_amount, 0),
                    NULLIF(sil.line_total_amount, 0),
                    NULLIF(sil.line_subtotal_amount, 0),
                    (sil.quantity * sil.price_unit)
                ) AS total
            FROM sale_order_import_line sil
            JOIN sale_order_import si ON si.id = sil.import_id
            JOIN res_company company ON company.id = si.company_id
            LEFT JOIN res_partner rp ON rp.id = sil.customer_id
            WHERE si.historical = TRUE
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                {self._select_sale_lines()}
                UNION ALL
                {self._select_historical_lines()}
            )
            """
        )
