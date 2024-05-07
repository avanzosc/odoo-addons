# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    move_line_ids = fields.One2many(
        "stock.move.line",
        string="Stock move lines",
        compute="_compute_move_ids",
        inverse="_set_move_line_ids",
        readonly=False,
    )
    consignee_id = fields.Many2one(
        string="Consignee", comodel_name="res.partner", copy=False
    )
    contact_person1_id = fields.Many2one(
        string="Contact Person 1", comodel_name="res.partner", copy=False
    )
    contact_person2_id = fields.Many2one(
        string="Contact Person 2", comodel_name="res.partner", copy=False
    )
    forwarder_id = fields.Many2one(
        string="Forwarder", comodel_name="res.partner", copy=False
    )
    delivery_addrress_id = fields.Many2one(
        string="Delivery Address", comodel_name="res.partner", copy=False
    )
    shipment_date = fields.Date(string="Shipment date", copy=False)
    incoterm_id = fields.Many2one(
        string="Incoterm", comodel_name="account.incoterms", copy=False
    )
    shipment_city = fields.Char(string="City", copy=False)
    shipment_state_id = fields.Many2one(
        string="State", comodel_name="res.country.state", copy=False
    )
    shipment_country_id = fields.Many2one(
        string="Country", comodel_name="res.country", copy=False
    )
    package_ids = fields.Many2many(
        string="Packages",
        comodel_name="stock.quant.package",
        compute="_compute_package_ids",
        column1="picking_batch_id",
        column2="package_id",
        store=True,
        copy=False,
        relation="rel_picking_batch_stock_quant_package",
    )
    count_packages = fields.Integer(
        string="Count packages", compute="_compute_count_packages"
    )
    num_boxes = fields.Integer(
        string="Num. Boxes",
        compute="_compute_num_boxes",
    )
    stock_picking_batch_custom_package_ids = fields.One2many(
        string="Customized box name",
        inverse_name="picking_batch_id",
        comodel_name="stock.picking.batch.custom.package",
        copy=False,
    )
    stock_picking_batch_total_box_ids = fields.One2many(
        string="Total boxes customization",
        inverse_name="picking_batch_id",
        comodel_name="stock.picking.batch.total.box",
        copy=False,
    )
    total_gross_volume_m3 = fields.Float(
        string="Total Gross Volume (M3)",
        default=0.0,
        copy=False,
        digits=dp.get_precision("Product Price"),
    )
    total_gross_weight_kg = fields.Float(
        string="Total Weight Volume (KG)",
        default=0.0,
        copy=False,
        digits=dp.get_precision("Product Price"),
    )

    @api.depends(
        "picking_ids",
        "picking_ids.move_line_ids_without_package",
        "picking_ids.move_line_ids_without_package.result_package_id",
    )
    def _compute_package_ids(self):
        for batch in self:
            packages = self.env["stock.quant.package"]
            for picking in batch.picking_ids:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: x.result_package_id
                )
                packages += lines.mapped("result_package_id")
            if packages:
                batch.package_ids = [(6, 0, packages.ids)]
            else:
                batch.package_ids = [(6, 0, [])]

    def _compute_count_packages(self):
        for batch in self:
            batch.count_packages = len(batch.package_ids)

    def _compute_num_boxes(self):
        for batch in self:
            num_boxes = 0
            if not batch.stock_picking_batch_total_box_ids:
                for picking in batch.picking_ids:
                    move_lines = picking.move_line_ids_without_package
                    num_boxes += sum(move_lines.mapped("package_qty"))
            else:
                num_boxes = sum(
                    batch.stock_picking_batch_total_box_ids.mapped("boxes_number")
                )
            batch.num_boxes = num_boxes

    def button_num_boxes(self):
        return True

    def catch_boxes_to_customized(self):
        if self.stock_picking_batch_custom_package_ids:
            self.stock_picking_batch_custom_package_ids.unlink()
        packages = self.env["stock.quant.package"]
        for picking in self.picking_ids:
            lines = picking.move_line_ids_without_package.filtered(
                lambda x: x.result_package_id
            )
            packages += lines.mapped("result_package_id")
        if packages:
            for package in packages:
                vals = {"picking_batch_id": self.id, "name": package.name}
                self.env["stock.picking.batch.custom.package"].create(vals)

    def action_confirm(self):
        if not self.shipment_date:
            raise UserError(_("You must enter the shipment date."))
        if not self.incoterm_id:
            raise UserError(_("You must enter the incoterm."))
        if not self.consignee_id:
            raise UserError(_("You must enter the consignee."))
        if not self.contact_person1_id and not self.contact_person2_id:
            raise UserError(_("You must enter the contact person."))
        if not self.forwarder_id:
            raise UserError(_("You must enter the forwarder."))
        if not self.delivery_addrress_id:
            raise UserError(_("You must enter the delivery address."))
        return super().action_confirm()

    def action_view_packages(self):
        action = self.env.ref("stock.action_package_view")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", self.package_ids.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def get_packing_list_number(self):
        number = ""
        for picking in self.picking_ids:
            num = len(picking.name)
            num -= 1
            for i in range(num, 0, -1):
                if not picking.name[i].isdigit():
                    if not number == 0 or int(picking.name[i + 1 : num + 1]) > int(
                        number
                    ):
                        number = picking.name[i + 1 : num + 1]
                    break
        return number

    def get_invoice_numbers(self):
        literal = ""
        if self.invoice_ids:
            invoices = sorted(self.invoice_ids, key=lambda r: r.name)
            for invoice in invoices:
                if not literal:
                    literal = invoice.name
                else:
                    literal = "{} - {}".format(literal, invoice.name)
        return literal

    def get_invoice_sales(self, invoice):
        sale_orders = self.env["sale.order"]
        invoice_lines = invoice.invoice_line_ids.sorted(key=lambda x: (x.sequence))
        for invline in invoice_lines:
            for move_line in self.move_line_ids:
                for invoice_line in move_line.move_id.invoice_line_ids:
                    if (
                        invline == invoice_line
                        and invoice_line.move_id == invoice
                        and move_line.sale_order_id not in sale_orders
                    ):
                        sale_orders += move_line.sale_order_id
        return sale_orders

    def get_lines_to_print(self, invoice, sale, pack=False):
        lines = []
        invoice_lines = invoice.invoice_line_ids.sorted(key=lambda x: (x.sequence))
        for invoice_line in invoice_lines:
            move_lines = self.get_move_lines_to_print_package_inovice_report(
                sale, invoice_line, pack
            )
            if move_lines:
                move_lines = move_lines.sorted(key=lambda x: (x.result_package_name))
                lines = move_lines.get_info_to_print_picking_batch(lines, invoice_line)
                if self.stock_picking_batch_custom_package_ids and lines:
                    for line in lines:
                        customp = self.stock_picking_batch_custom_package_ids
                        custom = customp.filtered(
                            lambda x: x.name == line.get("result_package")
                        )
                        if custom:
                            line["result_package"] = custom.box_new_name
        return lines

    def get_move_lines_to_print_package_inovice_report(self, sale, invoice_line, pack):
        move_lines = self.env["stock.move.line"]
        for move in self.move_ids.filtered(
            lambda x: x.sale_line_id and x.sale_line_id.order_id == sale
        ):
            for invl in move.invoice_line_ids:
                if invl == invoice_line:
                    for mline in move.move_line_ids:
                        move_lines += mline
        if move_lines and pack:
            move_lines = move_lines.filtered(lambda z: z.result_package_id == pack)
        return move_lines

    def get_package_total_info(self):
        my_dimensions = []
        for picking in self.picking_ids:
            for line in picking.move_line_ids_without_package.filtered(
                lambda x: x.result_package_id
            ):
                dimensions = "{} x {} x {}".format(
                    line.result_package_id.height,
                    line.result_package_id.width,
                    line.result_package_id.pack_length,
                )
                if dimensions not in my_dimensions:
                    my_dimensions.append(dimensions)
        lines = []
        for dimension in my_dimensions:
            packages = ""
            boxes = 0
            for picking in self.picking_ids:
                for line in picking.move_line_ids_without_package.filtered(
                    lambda x: x.result_package_id
                ):
                    d = "{} x {} x {}".format(
                        line.result_package_id.height,
                        line.result_package_id.width,
                        line.result_package_id.pack_length,
                    )
                    if dimension == d:
                        boxes += line.package_qty
                        if packages:
                            packages = "{}, {}".format(
                                packages, line.result_package_id.name
                            )
                        else:
                            packages = line.result_package_id.name
            lines.append(
                {"boxes": boxes, "dimensions": dimension, "packages": packages}
            )
        return lines

    def get_totals_to_print(self):
        tnv = 0
        tgv = 0
        tnw = 0
        tgw = 0
        for invoice in self.invoice_ids:
            sale_orders = self.get_invoice_sales(invoice)
            for sale in sale_orders:
                invoice_lines = invoice.invoice_line_ids.sorted(
                    key=lambda x: (x.sequence)
                )
                for invoice_line in invoice_lines:
                    mls = self.get_move_lines_to_print_package_inovice_report(
                        sale, invoice_line, False
                    )
                    if mls:
                        move_lines = mls.sorted(key=lambda x: (x.result_package_name))
                        (
                            tnv,
                            tgv,
                            tnw,
                            tgw,
                        ) = move_lines.get_total_to_print_picking_batch(
                            tnv, tgv, tnw, tgw
                        )
        return {
            "total_net_volume": tnv,
            "total_gross_volume": tgv,
            "total_net_weight": tnw,
            "total_gross_weight": tgw,
        }
