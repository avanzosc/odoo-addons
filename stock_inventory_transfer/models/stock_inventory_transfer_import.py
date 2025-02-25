# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp
from odoo.addons.base_import_wizard.models.base_import import (
    check_number,
    convert2str,
    convert2date,
)


class StockInventoryTransfer(models.Model):
    _name = "stock.inventory.transfer"
    _inherit = "base.import"

    import_line_ids = fields.One2many(
        comodel_name="stock.inventory.transfer.line",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.user.company_id.id,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_src_id = fields.Many2one(
        string="Source Location",
        comodel_name="stock.location",
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_dst_id = fields.Many2one(
        string="Destination Location",
        comodel_name="stock.location",
        required=True,
        states={"done": [("readonly", True)]},
        copy=False,
    )
    stock_move_count = fields.Integer(
        compute="_compute_stock_count",
    )
    stock_picking_count = fields.Integer(
        compute="_compute_stock_count",
    )

    def _compute_stock_count(self):
        for record in self:
            moves = record.mapped("import_line_ids.stock_move_id")
            record.stock_move_count = len(moves)
            record.stock_picking_count = len(moves.mapped("picking_id"))

    @api.onchange("picking_type_id")
    def _onchange_picking_type(self):
        for record in self:
            record.update({
                "location_src_id": record.picking_type_id.default_location_src_id.id,
                "location_dst_id": record.picking_type_id.default_location_dest_id.id,
            })

    def _get_line_values(self, row_values=False, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values, datemode=datemode)
        if row_values:
            log_infos = []
            product_name = row_values.get("producto", "")
            product_code = row_values.get("lista", "")
            if not product_name and not product_code:
                return {}
            product_qty = row_values.get("cantidad", 0.0)
            values.update(
                {
                    "product_code": str(product_code),
                    "product_name": product_name or str(product_code),
                    "product_qty": check_number(product_qty),
                }
            )
            if not product_name:
                log_infos.append(_("Product Code added as Product Name"))
            values.update(
                {
                    "log_info": "\n".join(log_infos),
                    "state": "error" if log_infos else "2validate",
                }
            )
        return values

    def action_process(self):
        result = super().action_process()
        self.mapped("import_line_ids.stock_move_id")._assign_picking()
        return result

    def button_open_import_line(self):
        action = super().button_open_import_line()
        action['context'].update({'import_hide': False})
        return action

    def button_open_stock_move(self):
        self.ensure_one()
        stock_moves = self.mapped("import_line_ids.stock_move_id")
        action = self.env["ir.actions.act_window"].for_xml_id(
            "stock", "stock_move_action")
        action["domain"] = expression.AND(
            [[("id", "in", stock_moves.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action

    def button_open_stock_picking(self):
        self.ensure_one()
        pickings = self.mapped("import_line_ids.stock_move_id.picking_id")
        action = self.env["ir.actions.act_window"].for_xml_id(
            "stock", "action_picking_tree_all")
        action["domain"] = expression.AND(
            [[("id", "in", pickings.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action



class StockInventoryTransferLine(models.Model):
    _name = "stock.inventory.transfer.line"
    _inherit = "base.import.line"

    import_id = fields.Many2one(
        comodel_name="stock.inventory.transfer",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_barcode = fields.Char(
        string="Barcode",
        help="International Article Number used for product identification.",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_src_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_src_id = fields.Many2one(
        string="Source Location",
        comodel_name="stock.location",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_dst_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    location_dst_id = fields.Many2one(
        string="Destination Location",
        comodel_name="stock.location",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_qty = fields.Float(
        string="Quantity",
        digits=dp.get_precision('Product Unit of Measure'),
        states={"done": [("readonly", True)]},
        copy=False,
    )
    stock_move_id = fields.Many2one(
        comodel_name="stock.move",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        product_obj = self.env["product.product"].with_context(
            force_company_id=self.import_id.company_id.id)
        if self.product_id:
            return self.product_id, log_info
        if self.product_barcode:
            search_domain = [
                ("barcode", "=", self.product_barcode),
            ]
        else:
            search_domain = [
                ("default_code", "=", self.product_code),
            ]
        products = product_obj.search(search_domain)
        name_domain = [
            ("name", "=", self.product_name),
        ]
        if not products:
            search_domain = expression.OR(
                [
                    search_domain,
                    name_domain
                ]
            )
        elif len(products) > 1:
            search_domain = expression.OR(
                [
                    search_domain,
                    name_domain,
                ]
            )
        products = product_obj.search(search_domain)
        if not products:
            log_info = _("No product found.")
        elif len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products and products[:1], log_info

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "product_id": product and product.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        stock_move = self.env["stock.move"].create(self._stock_move_values())
        update_values.update(
            {
                "stock_move_id": stock_move and stock_move.id,
                "log_info": "",
                "state": "done",
            }
        )
        return update_values

    def button_process(self):
        result = super().button_process()
        self.stock_move_id._assign_picking()
        return result

    def _stock_move_values(self):
        self.ensure_one()
        qty = self.product_qty
        picking_type_id = self.import_id.picking_type_id.id
        location_id = self.import_id.location_src_id.id
        location_dest_id = self.import_id.location_dst_id.id
        return {
            'name': self.product_id.display_name,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'product_uom_qty': qty,
            'company_id': self.import_id.company_id.id,
            'picking_type_id': picking_type_id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
        }


    def action_open_form(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"].for_xml_id(
            "stock_inventory_transfer",
            "stock_inventory_transfer_line_action"
        )
        action['views'] = [(
            self.env.ref("stock_inventory_transfer."
                         "stock_inventory_transfer_line_view_form").id,
            "form")]
        action["res_id"] = self.id
        return action
