# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizPickingBoxLabel(models.TransientModel):
    _name = "wiz.picking.box.label"
    _description = "Wizard For Box Label Report"

    picking_id = fields.Many2one(
        string="Picking", comodel_name="stock.picking", readonly=True
    )
    label_box_line_ids = fields.One2many(
        comodel_name="wiz.picking.box.label.line",
        inverse_name="wiz_picking_box_label_id",
    )
    product_ids = fields.Many2many(
        string="Products", comodel_name="product.product", readonly=True
    )
    lot_ids = fields.Many2many(string="Lots", comodel_name="stock.lot")
    number_of_labels_to_print = fields.Integer(
        string="Number of labels to print", required=True, default=1
    )

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        act_id = self.env.context.get("active_id")
        if act_id:
            picking = self.env["stock.picking"].browse(act_id)
            result["picking_id"] = picking.id
            result["product_ids"] = [x.product_id.id for x in picking.move_line_ids]
            lot_ids = [x.lot_id.id for x in picking.move_line_ids if x.lot_id]
            if lot_ids:
                result["lot_ids"] = lot_ids
        return result

    def print_box_labels(self):
        action = self.env.ref(
            "stock_picking_box_label_report.action_picking_box_label_report"
        )
        return action.report_action(self)


class WizPickingBoxLabelLine(models.TransientModel):
    _name = "wiz.picking.box.label.line"
    _description = "Lines For Wizard Box Label Report"

    wiz_picking_box_label_id = fields.Many2one(
        string="Wizard",
        comodel_name="wiz.picking.box.label",
    )
    product_id = fields.Many2one(string="Product", comodel_name="product.product")
    lot_id = fields.Many2one(string="Lot", comodel_name="stock.lot")
    product_qty = fields.Float(string="Quantity", default=0)
    customer_product_code = fields.Char(
        string="Customer product code", compute="_compute_customer_product_code"
    )

    def _compute_customer_product_code(self):
        for line in self:
            product_code = ""
            for customer in line.product_id.customer_ids:
                if (
                    customer.partner_id.id
                    == line.wiz_picking_box_label_id.picking_id.partner_id.id
                ):
                    product_code = customer.product_code
            if (
                not product_code
                and line.wiz_picking_box_label_id.picking_id.partner_id.parent_id
            ):
                partner = line.wiz_picking_box_label_id.picking_id.partner_id.parent_id
                for customer in line.product_id.customer_ids:
                    if customer.partner_id.id == partner.id:
                        product_code = customer.product_code
            line.customer_product_code = product_code
