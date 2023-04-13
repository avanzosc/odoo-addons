# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
import xlrd
import pytz


class StockPickingImport(models.Model):
    _name = "stock.picking.import"
    _inherit = "base.import"
    _description = "Wizard to import pickings"

    import_line_ids = fields.One2many(
        comodel_name="stock.picking.import.line",
    )
    picking_count = fields.Integer(
        string="# Pickings",
        compute="_compute_picking_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            picking_date = row_values.get("Date", "")
            if picking_date:
                timezone = pytz.timezone(self._context.get('tz') or 'UTC')
                picking_date = xlrd.xldate.xldate_as_datetime(
                    picking_date, 0)
                picking_date = timezone.localize(
                    picking_date).astimezone(pytz.UTC)
                picking_date = picking_date.replace(
                    tzinfo=None)
            if not picking_date:
                picking_date = False
            picking_location = row_values.get("Location", "")
            picking_location_dest = row_values.get("LocationDest", "")
            picking_product_code = row_values.get("ProductCode", "")
            picking_product_name = row_values.get("ProductName", "")
            picking_lot = row_values.get("Lot", "")
            picking_qty_done = row_values.get("QtyDone", "")
            log_info = ""
            if not picking_location_dest:
                return {}
            values.update(
                {
                    "picking_date": picking_date,
                    "picking_location": convert2str(picking_location),
                    "picking_location_dest": convert2str(
                        picking_location_dest),
                    "picking_product_code": convert2str(picking_product_code),
                    "picking_product_name": convert2str(picking_product_name),
                    "picking_lot": convert2str(picking_lot),
                    "picking_qty_done": picking_qty_done,
                    "log_info": log_info,
                }
            )
        return values

    def _compute_picking_count(self):
        for record in self:
            record.picking_count = len(
                record.mapped("import_line_ids.picking_id"))

    def button_open_picking(self):
        self.ensure_one()
        pickings = self.mapped("import_line_ids.picking_id")
        action = self.env.ref("stock.action_picking_tree_all")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", pickings.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class StockPickingImportLine(models.Model):
    _name = "stock.picking.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import pickings"

    @api.model
    def _get_selection_picking_type(self):
        return self.env["stock.picking"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_picking_type(self):
        default_dict = self.env["stock.picking"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="stock.picking.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking")
    picking_date = fields.Datetime(
        string="Date Done",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_location = fields.Char(
        string="Location",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    picking_location_dest = fields.Char(
        string="Location Dest",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    picking_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_lot = fields.Char(
        string="Lot",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_qty_done = fields.Float(
        string="Qty Done",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        states={"done": [("readonly", True)]},
    )
    picking_location_dest_id = fields.Many2one(
        string="Location Dest",
        comodel_name="stock.location",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_lot_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string="Lot/Serial Number",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Picking Type",
        states={"done": [("readonly", True)]},
        copy=False,
        )
    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking",
        readonly=True)
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="stock.move.line",
        readonly=True)

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            picking_type = product = lot = location = location_dest = False
            location, log_info_location = line._check_location()
            if log_info_location:
                log_info += log_info_location
            location_dest, log_info_location_dest = line._check_location_dest()
            if log_info_location_dest:
                log_info += log_info_location_dest
            if not log_info_location and not log_info_location_dest:
                picking_type, log_info_picking_type = (
                    line._check_picking_type(
                        location=location, location_dest=location_dest))
                if log_info_picking_type:
                    log_info += log_info_picking_type
            product, log_info_product = line._check_product()
            if log_info_product:
                log_info += log_info_product
            if not log_info_product and (
                line.picking_lot) and (
                    product.tracking != "none" and not log_info_picking_type):
                lot, log_info_lot = line._check_lot(
                    product=product, picking_type=picking_type)
                if log_info_lot:
                    log_info += log_info_lot
            state = "error" if log_info else "pass"
            action = "nothing"
            if state != "error":
                action = "create"
            update_values = {
                "picking_location_id": location and location.id,
                "picking_location_dest_id": (
                    location_dest and location_dest.id),
                "picking_type_id": picking_type and picking_type.id,
                "picking_product_id": product and product.id,
                "picking_lot_id": lot and lot.id,
                "log_info": log_info,
                "state": state,
                "action": action,
                }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        log_info = ""
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.action == "create":
                if self.import_id.import_line_ids.filtered(
                    lambda l: l.picking_type_id == (
                        line.picking_type_id) and (
                            l.picking_date == line.picking_date) and (
                                l.state == "error")):
                    log_info = _(
                        "Error: There is another line with the same" +
                        " picking type with some errors.")
                else:
                    if not line.picking_id:
                        picking = line._create_picking()
                        lines = self.import_id.import_line_ids.filtered(
                            lambda l: l.picking_type_id == (
                                line.picking_type_id) and (
                                    l.picking_date == line.picking_date) and (
                                        l.state not in ("error", "done")))
                        for record in lines:
                            record.picking_id = picking.id
                            if not record.move_line_id:
                                same_product = lines.filtered(
                                    lambda c: c.picking_product_id == (
                                        record.picking_product_id) and (
                                            c.picking_lot_id) == (
                                                record.picking_lot_id))
                                qty = sum(
                                    same_product.mapped("picking_qty_done"))
                                lot, log_info = record._check_lot(
                                    product=record.picking_product_id,
                                    picking_type=record.picking_type_id)
                                if not log_info and not lot and (
                                    record.picking_product_id.tracking != "none"
                                    ) and (
                                        record.picking_type_id.use_create_lots):
                                    lot = record._create_lot()
                                if lot:
                                    record.picking_lot_id = lot.id
                                moveline = record._create_movelines(qty=qty)
                                for l in same_product:
                                    l.move_line_id = moveline.id
                                    if lot:
                                        l.picking_lot_id = lot.id
                        picking.action_confirm()
            else:
                continue
            state = "error" if log_info else "done"
            line.write({
                "log_info": log_info,
                "state": state})
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_location(self):
        self.ensure_one()
        log_info = ""
        if self.picking_location_id:
            return self.picking_location_id, log_info
        location_obj = self.env["stock.location"]
        search_domain = ['|', ("name", "=", self.picking_location),
                         ("complete_name", "=", self.picking_location)]
        locations = location_obj.search(search_domain)
        if not locations:
            locations = False
            log_info = _("Error: No origin location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _("Error: More than one origin location found.")
        return locations and locations[:1], log_info

    def _check_location_dest(self):
        self.ensure_one()
        log_info = ""
        if self.picking_location_dest_id:
            return self.picking_location_dest_id, log_info
        location_obj = self.env["stock.location"]
        search_domain = ['|', ("name", "=", self.picking_location_dest),
                         ("complete_name", "=", self.picking_location_dest)]
        locations = location_obj.search(search_domain)
        if not locations:
            locations = False
            log_info = _("Error: No destination location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _("Error: More than one destination location found.")
        return locations and locations[:1], log_info

    def _check_picking_type(self, location=False, location_dest=False):
        self.ensure_one()
        log_info = ""
        if self.picking_type_id:
            return self.picking_type_id, log_info
        picking_type_obj = self.env["stock.picking.type"]
        search_domain = []
        if location:
            search_domain = expression.AND(
                [[("default_location_src_id", "=", location.id)],
                 search_domain])
        if location_dest:
            search_domain = expression.AND(
                [[("default_location_dest_id", "=", location_dest.id)],
                 search_domain])
        picking_types = picking_type_obj.search(search_domain)
        if not picking_types:
            picking_types = False
            log_info = _("Error: No picking type found.")
        elif len(picking_types) > 1:
            picking_types = False
            log_info = _("Error: More than one picking type found.")
        return picking_types and picking_types[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.picking_product_id:
            return self.picking_product_id, log_info
        product_obj = self.env["product.product"]
        if self.picking_product_code:
            search_domain = [
                ("default_code", "=", self.picking_product_code)]
        else:
            search_domain = [("name", "=", self.picking_product_name)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            products = False
            log_info = _("Error: More than one product found.")
        return products and products[:1], log_info

    def _check_lot(self, product=False, picking_type=False):
        self.ensure_one()
        log_info = ""
        lots = False
        if product and product.tracking == "none":
            return lots, log_info
        if self.picking_lot_id:
            return self.picking_lot_id, log_info
        lot_obj = self.env["stock.production.lot"]
        search_domain = [("name", "=", self.picking_lot)]
        if product:
            search_domain = expression.AND(
                [[("product_id", "=", product.id)], search_domain]
            )
        lots = lot_obj.search(search_domain)
        if not lots:
            lots = False
            log_info = _("Error: No lot found.")
            if picking_type and (
                picking_type.use_create_lots) and (
                    self.picking_lot):
                log_info = ""
        elif len(lots) > 1:
            lots = False
            log_info = _("Error: More than one lot found.")
        return lots and lots[:1], log_info

    def _create_picking(self):
        self.ensure_one()
        picking_obj = self.env["stock.picking"]
        values = self._picking_values()
        picking = picking_obj.create(values)
        return picking

    def _create_movelines(self, qty=0):
        self.ensure_one()
        moveline_obj = self.env["stock.move.line"]
        values = self._moveline_values(qty=qty)
        moveline = moveline_obj.create(values)
        return moveline

    def _create_lot(self):
        self.ensure_one()
        print('create lot')
        print(self.picking_product_id.name)
        lot = self.env["stock.production.lot"].create({
                "product_id": self.picking_product_id.id,
                "name": self.picking_lot,
                "company_id": self.import_id.company_id.id})
        return lot

    def _picking_values(self):
        return {
            "scheduled_date": self.picking_date,
            "picking_type_id": self.picking_type_id.id,
            "location_id": self.picking_type_id.default_location_src_id.id,
            "location_dest_id": self.picking_location_dest_id.id
            }

    def _moveline_values(self, qty=0):
        vals = {
                "product_id": self.picking_product_id.id,
                "qty_done": qty,
                "product_uom_id": self.picking_product_id.uom_id.id,
                "location_id": self.picking_type_id.default_location_src_id.id,
                "location_dest_id": (
                    self.picking_type_id.default_location_dest_id.id),
                "picking_id": self.picking_id.id}
        if self.picking_product_id.tracking != "none" and self.picking_lot_id:
            vals.update({
                "lot_id": self.picking_lot_id.id})
        return vals
