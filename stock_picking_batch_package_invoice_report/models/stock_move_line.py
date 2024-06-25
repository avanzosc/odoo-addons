# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_order_id = fields.Many2one(
        string="Sale order",
        compute="_compute_sale_order_id",
        comodel_name="sale.order",
        copy=False,
        store=True,
    )
    result_package_name = fields.Char(
        string="Package Referece",
        related="result_package_id.name",
        store=True,
        copy=False,
    )
    parcel_number = fields.Char(string="Parcel number", copy=False)

    @api.depends("move_id", "move_id.sale_line_id", "move_id.sale_line_id.order_id")
    def _compute_sale_order_id(self):
        for line in self:
            sale = False
            if (
                line.move_id
                and line.move_id.sale_line_id
                and line.move_id.sale_line_id.order_id
            ):
                sale = line.move_id.sale_line_id.order_id.id
            line.sale_order_id = sale

    def get_info_to_print_picking_batch(self, lines, invoice_line):
        for line in self:
            qty = (
                line.qty_done
                if line.picking_id.state == "done"
                else line.product_uom_qty
            )
            packaging_format = ""
            container = 0
            package_qty = 0
            product_weight = 0
            weight_kg = 0
            volume_m3 = 0
            total_weight_kg = 0
            total_volume_m3 = 0
            result_package_dimensions = ""
            if line.packaging_id:
                packaging_format = line.packaging_id.name
            container = line.container
            package_qty = line.package_qty
            if line.result_package_id:
                result_package_dimensions = "{}x{}x{}".format(
                    line.result_package_id.pack_length,
                    line.result_package_id.width,
                    line.result_package_id.height,
                )
                volume_m3 = line.result_package_id.volume
            product_weight = line.product_id.weight
            weight_kg = product_weight * container
            total_weight_kg = round(container * package_qty * product_weight, 4)
            total_volume_m3 = round(volume_m3 * package_qty, 4)
            data = {
                "result_package": line.result_package_name,
                "parcel_number": line.parcel_number,
                "part_number": line.product_id.default_code,
                "product_name": line.product_id.name,
                "ean13_code": line.product_id.barcode,
                "qty": qty,
                "packaging_format": packaging_format,
                "items_per_master_box_o_pack": container,
                "master_boxes_and_packs_qty": package_qty,
                "product_weight": product_weight,
                "result_package_dimensions": result_package_dimensions,
                "weight_kg": weight_kg,
                "volume_m3": volume_m3,
                "total_weight_kg": total_weight_kg,
                "total_volume_m3": total_volume_m3,
            }
            if invoice_line:
                data["invoice_line_number"] = invoice_line.sequence_related_invoice
            lines.append(data)
        return lines

    def get_total_to_print_picking_batch(
        self, total_net_volume, total_gross_volume, total_net_weight, total_gross_weight
    ):
        for line in self:
            volume_m3 = 0
            container = line.container
            package_qty = line.package_qty
            if line.result_package_id:
                volume_m3 = line.result_package_id.volume
            product_weight = line.product_id.weight
            total_weight_kg = round(container * package_qty * product_weight, 4)
            total_volume_m3 = round(volume_m3 * package_qty, 4)
            total_net_volume = total_net_volume + total_volume_m3
            total_gross_volume = total_gross_volume + total_volume_m3
            total_net_weight = total_net_weight + total_weight_kg
            total_gross_weight = total_gross_weight + total_weight_kg
        return (
            total_net_volume,
            total_gross_volume,
            total_net_weight,
            total_gross_weight,
        )
