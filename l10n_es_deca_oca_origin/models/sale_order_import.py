# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2date, convert2str


class SaleOrderImport(models.Model):
    _name = "sale.order.import"
    _inherit = "base.import"
    _description = "Wizard to import sale orders"

    import_line_ids = fields.One2many(
        comodel_name="sale.order.import.line",
    )
    sale_order_count = fields.Integer(
        string="# Sale Orders",
        compute="_compute_sale_order_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
    )
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            line_vals = self._get_line_fields_values(row_values)
            values.update(line_vals)
        return values

    def _get_line_fields_values(self, row_values):
        date_order = row_values.get("FechaViaje", "")
        upload_date = row_values.get("FechaCarga", "")
        carrier_name = row_values.get("Transportista", "")
        tractor_licence_plate = row_values.get("MatTractor", "")
        remolque_licence_plate = row_values.get("MatRemolque", "")
        autorizacion_especial = row_values.get("AutorizacionEspecial", "")
        customer_name = row_values.get("Pagador", "")
        charging_point_name = row_values.get("PuntoCarga", "")
        client_order_ref = row_values.get("RefFactura", "")
        product_name = row_values.get("Producto", "")
        addressee_name = row_values.get("Destinatario", "")
        deca_notes = row_values.get("DecaNotas", "")
        charging_city = row_values.get("LocalidadCarga", "")
        addressee_city = row_values.get("LocalidadDescarga", "")
        line_vals = {
            "date_order": convert2date(date_order) if date_order else False,
            "upload_date": convert2date(upload_date) if upload_date else False,
            "carrier_name": convert2str(carrier_name),
            "tractor_licence_plate": convert2str(tractor_licence_plate),
            "remolque_licence_plate": convert2str(remolque_licence_plate),
            "customer_name": convert2str(customer_name),
            "charging_point_name": convert2str(charging_point_name),
            "client_order_ref": convert2str(client_order_ref),
            "product_name": convert2str(product_name),
            "quantity": row_values.get("Cantidad", ""),
            "weight": row_values.get("Peso", ""),
            "addressee_name": convert2str(addressee_name),
            "price_unit": row_values.get("PrecioUnitario", ""),
            "special_authorization": convert2str(autorizacion_especial),
            "deca_notes": convert2str(deca_notes),
            "charging_city": convert2str(charging_city),
            "addressee_city": convert2str(addressee_city),
            "occupation": row_values.get("Ocupacion", ""),
            "log_info": "",
        }
        return line_vals

    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(
                record.mapped("import_line_ids.sale_order_id")
            )

    def button_open_sale_order(self):
        self.ensure_one()
        orders = self.mapped("import_line_ids.sale_order_id")
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        action["domain"] = expression.AND(
            [[("id", "in", orders.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action
