# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import unicodedata
from datetime import datetime

import pytz

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.models import expression


def normalize_text(value):
    if not value:
        return ""

    return "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    ).lower()


class SaleOrderImportLine(models.Model):
    _name = "sale.order.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import sale orders"

    import_id = fields.Many2one(
        comodel_name="sale.order.import",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="import_id.company_id",
        store=True,
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
    )
    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
    )
    date_order = fields.Date(
        string="Travel Date",
        copy=False,
    )
    upload_date = fields.Date(
        copy=False,
    )
    carrier_name = fields.Char(
        copy=False,
    )
    carrier_id = fields.Many2one(
        string="Carrier",
        comodel_name="res.partner",
        copy=False,
    )
    tractor_licence_plate = fields.Char(
        copy=False,
    )
    tractor_vehicle_id = fields.Many2one(
        string="Tractor Vehicle", comodel_name="fleet.vehicle"
    )
    remolque_licence_plate = fields.Char(
        copy=False,
    )
    remolque_vehicle_id = fields.Many2one(
        string="Remolque Vehicle", comodel_name="fleet.vehicle"
    )
    customer_name = fields.Char(
        string="Payer Name",
        copy=False,
    )
    customer_id = fields.Many2one(
        string="Payer",
        comodel_name="res.partner",
        copy=False,
    )
    charging_point_name = fields.Char(
        copy=False,
    )
    charging_point_id = fields.Many2one(
        string="Charging Point",
        comodel_name="res.partner",
        copy=False,
    )
    charging_city = fields.Char(copy=False)
    client_order_ref = fields.Char(
        string="Customer Order Reference",
        copy=False,
    )
    product_name = fields.Char(
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        copy=False,
    )
    quantity = fields.Float(
        copy=False,
    )
    occupation = fields.Float(
        copy=False,
    )
    weight = fields.Float(
        copy=False,
    )
    addressee_name = fields.Char(
        copy=False,
    )
    addressee_id = fields.Many2one(
        string="Addressee",
        comodel_name="res.partner",
        copy=False,
    )
    addressee_city = fields.Char(copy=False)
    price_unit = fields.Float(
        copy=False,
    )
    special_authorization = fields.Char(
        copy=False,
    )
    deca_notes = fields.Text(
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        sale, log_info_origin = self._check_origin()
        if log_info_origin:
            log_infos.append(log_info_origin)
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        customer = self._get_partner(
            self.customer_id,
            self.customer_name,
            _("Customer"),
            log_infos,
        )
        carrier = self._get_partner(
            self.carrier_id,
            self.carrier_name,
            _("Carrier"),
            log_infos,
        )
        charging_point = self._get_partner(
            self.charging_point_id,
            self.charging_point_name,
            _("Charging Point"),
            log_infos,
            city=self.charging_city,
        )
        addressee = self._get_partner(
            self.addressee_id,
            self.addressee_name,
            _("Addressee"),
            log_infos,
            city=self.addressee_city,
        )
        tractor_vehicle = self._get_vehicle(
            self.tractor_vehicle_id,
            self.tractor_licence_plate,
            _("Tractor License Plate"),
            log_infos,
        )
        remolque_vehicle = self._get_vehicle(
            self.remolque_vehicle_id,
            self.remolque_licence_plate,
            _("Remolque License Plate"),
            log_infos,
        )
        update_values.update(
            {
                "product_id": product.id if product and len(product) == 1 else False,
                "customer_id": customer.id
                if customer and len(customer) == 1
                else False,
                "carrier_id": carrier.id if carrier and len(carrier) == 1 else False,
                "charging_point_id": charging_point.id
                if charging_point and len(charging_point) == 1
                else False,
                "addressee_id": addressee.id
                if addressee and len(addressee) == 1
                else False,
                "tractor_vehicle_id": tractor_vehicle.id
                if tractor_vehicle and len(tractor_vehicle) == 1
                else False,
                "remolque_vehicle_id": remolque_vehicle.id
                if remolque_vehicle and len(remolque_vehicle) == 1
                else False,
                "log_info": "\n".join(log_infos),
                "state": "error" if log_infos else "pass",
                "action": "create",
            }
        )
        return update_values

    def _check_origin(self):
        log_info = ""
        error = _(
            "Error: Rows with the same Customer Order Reference have "
            "different information for importing sales order header "
            "data."
        )
        search_domain = [("client_order_ref", "=", self.client_order_ref)]
        sale = self.env["sale.order"].search(search_domain, limit=1)
        if sale:
            if not sale.sale_import_id or sale.sale_import_id != self.import_id:
                log_info = _(
                    "Error: Sale Order already exist with this Client Order "
                    "Ref.: %(client_order_ref)s."
                ) % {
                    "client_order_ref": self.client_order_ref,
                }
        if not log_info:
            lines = self.import_id.import_line_ids.filtered(
                lambda x: x.client_order_ref == self.client_order_ref
            )
            if lines:
                found = lines.filtered(
                    lambda x: (
                        x.customer_name != self.customer_name
                        or x.date_order != self.date_order
                        or x.carrier_name != self.carrier_name
                        or x.tractor_licence_plate != self.tractor_licence_plate
                        or x.remolque_licence_plate != self.remolque_licence_plate
                        or x.special_authorization != self.special_authorization
                    )
                )
                if found:
                    log_info = error
        return sale, log_info

    def _check_product(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        products = False
        if self.product_name:
            name = self.product_name.replace(" ", "")
            name = "".join(
                c
                for c in unicodedata.normalize("NFD", name)
                if unicodedata.category(c) != "Mn"
            )
            search_domain = [("trim_name", "=ilike", name)]
            products = product_obj.search(search_domain)
            if not products:
                products = product_obj.with_context(
                    lang=self.env.context.get("lang", "es_ES")
                ).search([("name", "=ilike", self.product_name)])
            if not products and "from_sale_wizard_laser" not in self.env.context:
                error = _("Product not found.")
                log_info = error if not log_info else f"{log_info} {error}"
            elif len(products) > 1:
                products, log_info = self._more_than_one_product_found(log_info, name)
        return products, log_info

    def _get_partner(self, partner, name, description, log_infos, city=False):
        if partner or not name:
            return partner
        partner = self._check_partner(name, city)
        if len(partner) > 1 and description in ("Customer", "Cliente"):
            if name == self.charging_point_name:
                partner = self._check_partner(name, self.charging_city)
            elif name == self.addressee_name:
                partner = self._check_partner(name, self.addressee_city)
        if not partner:
            log_infos.append(_("%s not found.") % description)
        elif len(partner) > 1:
            log_infos.append(_("More than one %s already exist.") % description)
        return partner

    def _more_than_one_product_found(self, log_info, name):
        product_obj = self.env["product.product"]
        search_domain = []
        if self.product_name:
            search_domain.append(("trim_name", "=ilike", name))
        products = product_obj.search(search_domain)
        if len(products) == 0 and "from_sale_wizard_laser" not in self.env.context:
            error = _("Product not found.")
            log_info = error if not log_info else f"{log_info} {error}"
        if len(products) > 1:
            error = _("More than one product already exist.")
            log_info = error if not log_info else f"{log_info} {error}"
        return products, log_info

    def _check_partner(self, name, city):
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        search_domain = [
            ("name_normalized", "ilike", normalize_text(name)),
        ]
        if city:
            search_domain.append(("city_normalized", "ilike", normalize_text(city)))
        if self.import_id.company_id:
            company = self.import_id.company_id
            partner_obj = partner_obj.with_company(company)
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", company.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
        partner = partner_obj.search(search_domain)
        return partner

    def _get_vehicle(self, vehicle, licence_plate, description, log_infos):
        if vehicle or not licence_plate:
            return vehicle
        vehicle = self._check_vehicle(licence_plate)
        if not vehicle:
            log_infos.append(_("%s not found in vehicles.") % description)
        elif len(vehicle) > 1:
            log_infos.append(
                _("More than one %s already exist in vehicles.") % description
            )
        return vehicle

    def _check_vehicle(self, license_plate):
        self.ensure_one()
        vehicle_obj = self.env["fleet.vehicle"]
        if self.import_id.company_id:
            vehicle_obj = vehicle_obj.with_company(self.import_id.company_id)
        search_domain = [("license_plate", "=", license_plate)]
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
        vehicles = vehicle_obj.search(search_domain)
        return vehicles

    def _action_process(self):
        update_values = super()._action_process()
        if self.import_id.company_id:
            self = self.with_company(self.import_id.company_id)
        if self.action == "create":
            sale_line = self._create_sale_line()
            state = "done"
            update_values.update(
                {
                    "sale_order_id": sale_line.order_id and sale_line.order_id.id,
                    "log_info": "",
                    "state": state,
                }
            )
        return update_values

    def _create_sale_line(self):
        self.ensure_one()
        if self.client_order_ref:
            sale, log_info_origin = self._check_origin()
            if log_info_origin:
                raise UserError(log_info_origin)
            if not sale:
                sale = self._create_sale_order()
        else:
            sale = self._create_sale_order()
        return self._create_sale_order_line(sale)

    def _create_sale_order(self):
        sale_obj = self.env["sale.order"]
        values = self._sale_order_values()
        new_sale = sale_obj.new(values)
        for comp_onchange in new_sale._onchange_methods["partner_id"]:
            comp_onchange(new_sale)
        vals = new_sale._convert_to_write(new_sale._cache)
        return sale_obj.create(vals)

    def _create_sale_order_line(self, sale):
        values = self._sale_order_line_values(sale)
        sale_line = self.env["sale.order.line"].create(values)
        return sale_line

    def _sale_order_values(self):
        values = {
            "partner_id": self.customer_id.id,
            "company_id": self.company_id.id,
            "sale_import_id": self.import_id.id,
            "carrier_contact_id": self.carrier_id.id,
            "tractor_license_plate_id": self.tractor_vehicle_id.id,
            "special_authorization": self.special_authorization,
            "deca_notes": self.deca_notes,
        }
        if self.remolque_vehicle_id:
            values["trailer_license_plate_id"] = self.remolque_vehicle_id.id
        if self.date_order:
            date_order = f"{fields.Date.to_string(self.date_order)} 08:00:00"
            date_order = datetime.strptime(date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            date_order = timezone.localize(date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            values["date_order"] = date_order
            values["commitment_date"] = date_order
        if self.client_order_ref:
            values["client_order_ref"] = self.client_order_ref
        return values

    def _sale_order_line_values(self, sale):
        values = {
            "order_id": sale.id,
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "product_uom": self.product_id.uom_id.id,
            "product_uom_qty": self.quantity,
            "price_unit": self.price_unit,
            "place_of_loading_id": self.charging_point_id.id,
            "place_of_delivery_id": self.addressee_id.id,
            "upload_date": self.upload_date,
            "deca_weight": self.weight,
        }
        return values
