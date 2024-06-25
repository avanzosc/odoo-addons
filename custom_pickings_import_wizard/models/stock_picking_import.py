# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytz
import xlrd

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str


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
        default=lambda self: self.env.company.id,
    )
    lot_create = fields.Boolean(string="Create Lot", default=True)

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            picking_custom_date_done = row_values.get("Fecha", "")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            picking_custom_date_done = xlrd.xldate.xldate_as_datetime(
                picking_custom_date_done, 0
            )
            picking_custom_date_done = timezone.localize(
                picking_custom_date_done
            ).astimezone(pytz.UTC)
            picking_custom_date_done = picking_custom_date_done.replace(tzinfo=None)
            picking_origin = row_values.get("DocumentoOrigen", "")
            picking_location = row_values.get("UbicacionOrigen", "")
            picking_location_dest = row_values.get("UbicacionDestino", "")
            picking_partner = row_values.get("NombreUbicacionDestino", "")
            picking_product_code = row_values.get("CodigoProducto", "")
            mother = row_values.get("Mother", "")
            picking_description = row_values.get("DescripcionProducto", "")
            picking_lot = row_values.get("Lote", "")
            picking_qty_done = row_values.get("Cantidad", "")
            picking_transporter_code = row_values.get("CodigoTransportista", "")
            picking_transporter = row_values.get("NombreTransportista", "")
            picking_license_plate = row_values.get("Matricula", "")
            picking_cost = row_values.get("CosteEnvio", "")
            log_info = ""
            if not picking_location_dest:
                return {}
            values.update(
                {
                    "picking_custom_date_done": picking_custom_date_done,
                    "picking_origin": convert2str(picking_origin),
                    "picking_location": convert2str(picking_location),
                    "picking_location_dest": convert2str(picking_location_dest),
                    "picking_partner": picking_partner.title(),
                    "mother": convert2str(mother),
                    "picking_product_code": convert2str(picking_product_code),
                    "picking_description": picking_description,
                    "picking_lot": convert2str(picking_lot),
                    "picking_qty_done": picking_qty_done,
                    "picking_transporter_code": convert2str(picking_transporter_code),
                    "picking_transporter": picking_transporter.title(),
                    "picking_license_plate": convert2str(picking_license_plate),
                    "picking_cost": picking_cost,
                    "log_info": log_info,
                }
            )
        return values

    def _compute_picking_count(self):
        for record in self:
            record.picking_count = len(record.mapped("import_line_ids.picking_id"))

    def button_open_picking(self):
        self.ensure_one()
        pickings = self.mapped("import_line_ids.picking_id")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        action["domain"] = expression.AND(
            [[("id", "in", pickings.ids)], safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action


class StockPickingImportLine(models.Model):
    _name = "stock.picking.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import pickings"

    import_id = fields.Many2one(
        comodel_name="stock.picking.import",
    )
    action = fields.Selection(
        string="Action",
        selection_add=[
            ("create", "Create"),
            ("update", "Update"),
        ],
        ondelete={"update": "set default", "create": "set default"},
    )
    picking_id = fields.Many2one(string="Picking", comodel_name="stock.picking")
    picking_custom_date_done = fields.Datetime(
        string="Date",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_origin = fields.Char(
        string="Origin Document",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_location = fields.Char(
        string="Location Src",
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
    picking_partner = fields.Char(
        string="Location Dest Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_description = fields.Text(
        string="Product Description",
    )
    mother = fields.Char(
        string="Mother",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    mother_id = fields.Many2one(
        string="Mother",
        comodel_name="stock.picking.batch",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_lot = fields.Char(
        string="Lot",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_qty_done = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_transporter_code = fields.Char(
        string="Transporter Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_transporter = fields.Char(
        string="Transporter",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_license_plate = fields.Char(
        string="License Plate",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_cost = fields.Float(
        string="Shipping Cost",
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
    picking_carrier_id = fields.Many2one(
        comodel_name="delivery.carrier",
        string="Carrier",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Picking Type",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    picking_batch_id = fields.Many2one(
        comodel_name="stock.picking.batch",
        string="Breeding",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            origin = picking_type = batch = carrier = product = lot = mother = False
            if line.picking_origin:
                origin, log_info = line._check_origin()
                if log_info:
                    update_values = {
                        "picking_origin": origin,
                        "log_info": log_info,
                        "state": "error",
                        "action": "nothing",
                    }
            if not log_info:
                location, log_info_location = line._check_location()
                if log_info_location:
                    log_info += log_info_location
                location_dest, log_info_location_dest = line._check_location_dest()
                if log_info_location_dest:
                    log_info += log_info_location_dest
                if not log_info_location and not log_info_location_dest:
                    picking_type, log_info_picking_type = line._check_picking_type(
                        location=location, location_dest=location_dest
                    )
                    if log_info_picking_type:
                        log_info += log_info_picking_type
                    if location and location.usage == "internal":
                        batch, log_info_batch = line._check_batch(
                            location=location_dest
                        )
                        if log_info_batch:
                            log_info += log_info_batch
                if line.picking_transporter_code:
                    carrier, log_info_carrier = line._check_carrier()
                    if log_info_carrier:
                        log_info += log_info_carrier
                if line.picking_product_code:
                    product, log_info_product = line._check_product()
                    if log_info_product:
                        log_info += log_info_product
                if not log_info_product and line.picking_lot:
                    lot, log_info_lot = line._check_lot(product=product)
                    if log_info_lot:
                        log_info += log_info_lot
                if line.mother:
                    mother, log_info_mother = line._check_mother()
                    if log_info_mother:
                        log_info += log_info_mother
                state = "error" if log_info else "pass"
                action = "nothing"
                if state != "error":
                    action = "create"
                update_values = {
                    "picking_origin": origin,
                    "picking_location_id": location and location.id,
                    "picking_location_dest_id": (location_dest and location_dest.id),
                    "picking_type_id": picking_type and picking_type.id,
                    "picking_batch_id": batch and batch.id,
                    "picking_carrier_id": carrier and carrier.id,
                    "picking_product_id": product and product.id,
                    "picking_lot_id": lot and lot.id,
                    "mother_id": mother and mother.id,
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
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            if line.picking_origin:
                origin, log_info = line._check_origin()
                if log_info:
                    state = "error"
                    action = "nothing"
                    lot = picking = False
                    same_origin = line.import_id.import_line_ids.filtered(
                        lambda c: c.picking_origin == line.picking_origin
                        and (c.picking_id)
                    )[:1]
                    if (
                        same_origin
                        and line.picking_product_id == (same_origin.picking_product_id)
                        and (same_origin.picking_type_id) == (line.picking_type_id)
                        and (same_origin.picking_carrier_id)
                        == (line.picking_carrier_id)
                    ):
                        log_info = ""
                        picking = same_origin.picking_id
                        lot, log_info = line._check_lot(product=line.picking_product_id)
                        if not lot and line.import_id.lot_create:
                            log_info = ""
                            lot = self.env["stock.production.lot"].create(
                                {
                                    "product_id": line.picking_product_id.id,
                                    "name": line.picking_lot,
                                    "company_id": line.import_id.company_id.id,
                                }
                            )
                        if lot:
                            if line.mother_id:
                                lot.batch_id = line.mother_id.id
                            line.write(
                                {"picking_lot_id": lot.id, "picking_id": picking.id}
                            )
                            self.env["stock.move.line"].create(
                                {
                                    "product_id": line.picking_product_id.id,
                                    "lot_id": line.picking_lot_id.id,
                                    "qty_done": line.picking_qty_done,
                                    "product_uom_id": (
                                        line.picking_product_id.uom_id.id
                                    ),
                                    "location_id": line.picking_type_id.default_location_src_id.id,
                                    "location_dest_id": line.picking_type_id.default_location_dest_id.id,
                                    "standard_price": (
                                        line.picking_product_id.standard_price
                                    ),
                                    "amount": (line.picking_product_id.standard_price)
                                    * (line.picking_qty_done),
                                    "picking_id": picking.id,
                                }
                            )
                            log_info = ""
                            state = "done"
                            action = "update"
                    line.write(
                        {
                            "picking_origin": origin,
                            "log_info": log_info,
                            "state": state,
                            "action": action,
                        }
                    )
            if line.action == "create":
                picking, log_info = line._create_picking()
            else:
                continue
            state = "error" if log_info else "done"
            line.write(
                {
                    "picking_id": picking and picking.id,
                    "log_info": log_info,
                    "state": state,
                }
            )
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "picking_id": picking and picking.id,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_origin(self):
        self.ensure_one()
        picking_obj = self.env["stock.picking"]
        search_domain = [("origin", "=", self.picking_origin)]
        log_info = ""
        pickings = picking_obj.search(search_domain)
        if pickings:
            log_info = _("Error: Previously uploaded picking.")
        return self.picking_origin, log_info

    def _check_location(self):
        self.ensure_one()
        log_info = ""
        if self.picking_location_id:
            return self.picking_location_id, log_info
        location_obj = self.env["stock.location"]
        search_domain = [
            "|",
            ("name", "=", self.picking_location),
            ("complete_name", "=", self.picking_location),
            ("usage", "!=", "view"),
        ]
        locations = location_obj.search(search_domain)
        if not locations:
            locations = False
            log_info = _("Error: No origin location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _(
                "Error: More than one origin location with name {} found."
            ).format(self.picking_location)
        return locations and locations[:1], log_info

    def _check_location_dest(self):
        self.ensure_one()
        log_info = ""
        if self.picking_location_dest_id:
            return self.picking_location_dest_id, log_info
        location_obj = self.env["stock.location"]
        search_domain = [
            "|",
            ("name", "=", self.picking_location_dest),
            ("complete_name", "=", self.picking_location_dest),
            ("usage", "!=", "view"),
        ]
        locations = location_obj.search(search_domain)
        if not locations:
            locations = False
            log_info = _("Error: No destination location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _(
                "Error: More than one destination location with name {} found."
            ).format(self.picking_location_dest)
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
                [[("default_location_src_id", "=", location.id)], search_domain]
            )
        if location_dest:
            search_domain = expression.AND(
                [[("default_location_dest_id", "=", location_dest.id)], search_domain]
            )
        picking_types = picking_type_obj.search(search_domain)
        if not picking_types:
            picking_types = False
            log_info = _("Error: No picking type found.")
        elif len(picking_types) > 1:
            picking_types = False
            log_info = _(
                "Error: More than one picking type with location origin "
                "{} and location destination {} found."
            ).format(location.name, location_dest.name)
        return picking_types and picking_types[:1], log_info

    def _check_batch(self, location=False):
        self.ensure_one()
        log_info = ""
        if self.picking_batch_id:
            return self.picking_batch_id, log_info
        batch_obj = self.env["stock.picking.batch"]
        cancel_breeding = self.env.ref("stock_warehouse_farm.batch_stage3")
        liquidated_breeding = self.env.ref("stock_picking_batch_breeding.batch_stage5")
        billed_breeding = self.env.ref("stock_picking_batch_breeding.batch_stage6")
        search_domain = []
        breeding = False
        mother = False
        if cancel_breeding and liquidated_breeding and billed_breeding:
            search_domain = expression.AND(
                [
                    [
                        (
                            "stage_id",
                            "not in",
                            (
                                cancel_breeding.id,
                                liquidated_breeding.id,
                                billed_breeding.id,
                            ),
                        )
                    ],
                    search_domain,
                ]
            )
        if location:
            search_domain = expression.AND(
                [[("location_id", "=", location.id)], search_domain]
            )
            if location.warehouse_id and (location.warehouse_id.activity) == (
                "fattening"
            ):
                search_domain = expression.AND(
                    [[("batch_type", "=", "breeding")], search_domain]
                )
                breeding = True
            elif location.warehouse_id and (location.warehouse_id.activity) in (
                "recry",
                "reproduction",
            ):
                search_domain = expression.AND(
                    [[("batch_type", "=", "mother")], search_domain]
                )
                mother = True
        breedings = batch_obj.search(search_domain)
        if not breedings:
            if breeding:
                new_stage = self.env.ref("stock_warehouse_farm.batch_stage1")
                breedings = self.env["stock.picking.batch"].create(
                    {
                        "name": "TEMP-{}".format(location.name),
                        "location_id": location.id,
                        "batch_type": "breeding",
                        "stage_id": new_stage.id,
                    }
                )
            elif mother:
                breedings = False
                log_info = _("No mothers in this location.")
        elif len(breedings) > 1:
            breedings = False
            log_info = _(
                "Error: More than one active breeding/mother with location "
                + "{} already exist."
            ).format(location.name)
        return breedings and breedings[:1], log_info

    def _check_mother(self):
        self.ensure_one()
        log_info = ""
        if self.mother_id:
            return self.mother_id, log_info
        mother_obj = self.env["stock.picking.batch"]
        search_domain = [("name", "=", self.mother), ("batch_type", "=", "mother")]
        mothers = mother_obj.search(search_domain)
        if not mothers:
            mothers = False
            log_info = _("Error: No mother found.")
        elif len(mothers) > 1:
            mothers = False
            log_info = _("Error: More than one mother found.")
        return mothers and mothers[:1], log_info

    def _check_carrier(self):
        self.ensure_one()
        log_info = ""
        if self.picking_carrier_id:
            return self.picking_carrier_id, log_info
        carrier_obj = self.env["delivery.carrier"]
        search_domain = [("code", "=", self.picking_transporter_code)]
        carriers = carrier_obj.search(search_domain)
        if not carriers:
            carriers = False
            log_info = _("Error: No shipping method found.")
        elif len(carriers) > 1:
            carriers = False
            log_info = _(
                "Error: More than one shipping method with code {} already exist."
            ).format(self.picking_transporter_code)
        return carriers and carriers[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.picking_product_id:
            return self.picking_product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = [("default_code", "=", self.picking_product_code)]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            products = False
            log_info = _(
                "Error: More than one product with code {} already exist."
            ).format(self.picking_product_code)
        return products and products[:1], log_info

    def _check_lot(self, product=False):
        self.ensure_one()
        log_info = ""
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
            if self.import_id.lot_create and self.picking_lot:
                log_info = ""
        elif len(lots) > 1:
            lots = False
            log_info = _("Error: More than one lot found")
        return lots and lots[:1], log_info

    def _create_picking(self):
        self.ensure_one()
        picking = False
        location_dest, log_info = self._check_location_dest()
        if not log_info:
            picking_type, log_info = self._check_picking_type(location=location_dest)
            if picking_type and not log_info:
                product, log_info = self._check_product()
                if not log_info:
                    if product.tracking != "none":
                        lot, log_info = self._check_lot(product=product)
                        if not lot and self.import_id.lot_create:
                            log_info = ""
                            lot = self.env["stock.production.lot"].create(
                                {
                                    "product_id": self.picking_product_id.id,
                                    "name": self.picking_lot,
                                    "company_id": self.import_id.company_id.id,
                                }
                            )
                        if lot:
                            self.picking_lot_id = lot.id
                            if self.mother_id:
                                lot.batch_id = self.mother_id.id
                    picking_obj = self.env["stock.picking"]
                    values = self._picking_values()
                    picking = picking_obj.create(values)
                    log_info = ""
        return picking, log_info

    def _picking_values(self):
        if self.picking_location_dest_id:
            location = self.picking_location_dest_id
        else:
            location = self.picking_type_id.default_location_src_id
        vals = {
            "custom_date_done": self.picking_custom_date_done,
            "scheduled_date": self.picking_custom_date_done,
            "origin": self.picking_origin,
            "picking_type_id": self.picking_type_id.id,
            "location_id": self.picking_type_id.default_location_src_id.id,
            "location_dest_id": location.id,
            "carrier_id": self.picking_carrier_id.id,
            "batch_id": self.picking_batch_id.id,
            "license_plate": self.picking_license_plate,
            "shipping_cost": self.picking_cost,
            "move_line_ids_without_package": [
                (
                    0,
                    0,
                    {
                        "product_id": self.picking_product_id.id,
                        "lot_id": self.picking_lot_id.id,
                        "qty_done": self.picking_qty_done,
                        "product_uom_id": self.picking_product_id.uom_id.id,
                        "location_id": self.picking_type_id.default_location_src_id.id,
                        "location_dest_id": location.id,
                        "standard_price": self.picking_product_id.standard_price,
                        "amount": (self.picking_product_id.standard_price)
                        * (self.picking_qty_done),
                    },
                )
            ],
        }
        return vals
