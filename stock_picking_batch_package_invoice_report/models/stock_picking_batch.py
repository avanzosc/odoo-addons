# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

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
    shipment_date = fields.Date(
        string="Shipment date", copy=False
        )
    incoterm_id = fields.Many2one(
        string="Incoterm", comodel_name="account.incoterms", copy=False
        )
    shipment_city = fields.Char(
        string="City", copy=False
        )
    shipment_state_id = fields.Many2one(
        string="State", comodel_name="res.country.state", copy=False
        )
    shipment_country_id = fields.Many2one(
        string="Country", comodel_name="res.country", copy=False
        )
    package_ids = fields.Many2many(
        string="Packages", comodel_name="stock.quant.package",
        compute="_compute_package_ids", column1="picking_batch_id",
        column2="package_id", store=True, copy=False,
        relation="rel_picking_batch_stock_quant_package"
        )
    count_packages = fields.Integer(
        string="Count packages", compute="_compute_count_packages")

    @api.depends("picking_ids", "picking_ids.move_line_ids_without_package",
                 "picking_ids.move_line_ids_without_package.result_package_id")
    def _compute_package_ids(self):
        for batch in self:
            packages = self.env["stock.quant.package"]
            for picking in batch.picking_ids:
                lines = picking.move_line_ids_without_package.filtered(
                    lambda x: x.result_package_id)
                packages += lines.mapped("result_package_id")
            if packages:
                batch.package_ids = [(6, 0, packages.ids)]
            else:
                batch.package_ids = [(6, 0, [])]

    def _compute_count_packages(self):
        for batch in self:
            batch.count_packages = len(batch.package_ids)

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
        return super(StockPickingBatch, self).action_confirm()

    def action_view_packages(self):
        action = self.env.ref("stock.action_package_view")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", self.package_ids.ids)],
             safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    def get_packing_list_number(self):
        number = ""
        for picking in self.picking_ids:
            num = len(picking.name)
            num -= 1
            for i in range(num, 0, -1):
                if not picking.name[i].isdigit():
                    if (not number == 0 or
                            int(picking.name[i+1:num+1]) > int(number)):
                        number = picking.name[i+1:num+1]
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
        for move_line in self.move_line_ids:
            for invoice_line in move_line.move_id.invoice_line_ids:
                if (invoice_line.move_id == invoice and
                        move_line.sale_order_id not in sale_orders):
                    sale_orders += move_line.sale_order_id
        return sale_orders

    def get_lines_to_print(self, invoice, sale, pack=False):
        lines = []
        invoice_lines = invoice.invoice_line_ids.sorted(
            key=lambda x: (x.sequence))
        for invoice_line in invoice_lines:
            move_lines = self.get_move_lines_to_print_package_inovice_report(
                sale, invoice_line, pack)
            if move_lines:
                move_lines = move_lines.sorted(key=lambda x: (
                    x.result_package_name))
                lines = move_lines.get_info_to_print_picking_batch(
                    lines, invoice_line)
        return lines

    def get_move_lines_to_print_package_inovice_report(self, sale,
                                                       invoice_line, pack):
        move_lines = self.env["stock.move.line"]
        for move in self.move_ids.filtered(
            lambda x: x.sale_line_id and
                x.sale_line_id.order_id == sale):
            for invl in move.invoice_line_ids:
                if invl == invoice_line:
                    for mline in move.move_line_ids:
                        move_lines += mline
        if move_lines and pack:
            move_lines = move_lines.filtered(
                lambda z: z.result_package_id == pack)
        return move_lines

    def get_package_total_info(self, pack):
        total_net_volume = 0
        total_net_weight = 0
        total_gross_volume = 0
        total_gross_weight = 0
        invoices = self.invoice_ids.sorted(key=lambda x: x.name)
        for invoice in invoices:
            sales = self.get_invoice_sales(invoice)
            for sale in sales:
                lines = self.get_lines_to_print(invoice, sale, pack=pack)
                for line in lines:
                    total_net_volume += line.get('volume_m3')
                    total_net_weight += line.get('weight_kg')
                    total_gross_volume += line.get('total_volume_m3')
                    total_gross_weight += line.get('total_weight_kg')
        return {"total_net_volume": total_net_volume,
                "total_net_weight": total_net_weight,
                "total_gross_volume": total_gross_volume,
                "total_gross_weight": total_gross_weight}
