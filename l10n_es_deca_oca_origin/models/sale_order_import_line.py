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
    addressee_ids = fields.Many2many(
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
        if self.client_order_ref:
            sale, log_info_origin = self._check_origin()
            if log_info_origin:
                log_infos.append(log_info_origin)
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
            self.addressee_ids,
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
                "customer_id": customer.id
                if customer and len(customer) == 1
                else False,
                "carrier_id": carrier.id if carrier and len(carrier) == 1 else False,
                "charging_point_id": charging_point.id
                if charging_point and len(charging_point) == 1
                else False,
                "addressee_ids": [(6, 0, addressee.ids)] if addressee else False,
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

    def _get_partner(self, partner, name, description, log_infos, city=False):
        counter = name.count("+") + 1 if name else 1
        if not name or (partner and len(partner) == counter):
            return partner
        old_log_infos = log_infos
        names = name.split("+")
        cities = city.split("+") if city else []
        if len(names) != len(cities) and (len(names) > 1 or len(cities) > 1):
            log_infos.append(_("The number of names and cities does not match."))
            return self.env["res.partner"]
        if not cities:
            cities = [False] * len(names)
        partners = self.env["res.partner"]
        for partner_name, partner_city in zip(names, cities, strict=False):
            found_partner = self._check_partner(
                partner_name.strip(), partner_city.strip() if partner_city else False
            )
            if not found_partner:
                log_infos.append(
                    _("%(description)s not found. " "Name: %(name)s, City: %(city)s")
                    % {
                        "description": description,
                        "name": partner_name.strip(),
                        "city": partner_city or "",
                    }
                )
            else:
                if len(partner) > 1:
                    log_infos.append(
                        _(
                            "More than one %(description)s already exist. "
                            "Name: %(name)s, City: %(city)s"
                        )
                        % {
                            "description": description,
                            "name": partner_name.strip(),
                            "city": partner_city or "",
                        }
                    )
                else:
                    partners |= found_partner
        if old_log_infos != log_infos:
            return partners
        if len(partners) > 1 and description == _("Customer"):
            if name == self.charging_point_name:
                partners = self._check_partner(name, self.charging_city)
            elif name == self.addressee_name:
                partners = self._check_partner(name, self.addressee_city)
            if not found_partner:
                log_infos.append(_("%s not found.") % description)
            elif len(partner) > 1:
                log_infos.append(_("More than one %s already exist.") % description)
        return partners

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
        return partner_obj.search(search_domain)

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
        return vehicle_obj.search(search_domain)

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
            sale = self._find_sale_order()
            if not sale:
                sale = self._create_sale_order()
        return self._create_sale_order_line(sale)

    def _find_sale_order(self):
        sale_obj = self.env["sale.order"]
        trailer_license_plate_id = (
            self.remolque_vehicle_id.id if self.remolque_vehicle_id.id else False
        )
        cond = [
            ("partner_id", "=", self.customer_id.id),
            ("company_id", "=", self.company_id.id),
            ("sale_import_id", "=", self.import_id.id),
            ("carrier_contact_id", "=", self.carrier_id.id),
            ("tractor_license_plate_id", "=", self.tractor_vehicle_id.id),
            ("special_authorization", "=", self.special_authorization),
            ("trailer_license_plate_id", "=", trailer_license_plate_id),
            ("client_order_ref", "=", self.client_order_ref),
        ]
        if self.date_order:
            date_order = f"{fields.Date.to_string(self.date_order)} 08:00:00"
            date_order = datetime.strptime(date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            date_order = timezone.localize(date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            cond.append(("date_order", "=", date_order))
            cond.append(("commitment_date", "=", date_order))
        return sale_obj.search(cond, limit=1)

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
        values["trailer_license_plate_id"] = (
            self.remolque_vehicle_id.id if self.remolque_vehicle_id.id else False
        )
        if self.date_order:
            date_order = f"{fields.Date.to_string(self.date_order)} 08:00:00"
            date_order = datetime.strptime(date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            date_order = timezone.localize(date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            values["date_order"] = date_order
            values["commitment_date"] = date_order
        values["client_order_ref"] = self.client_order_ref
        return values

    def _sale_order_line_values(self, sale):
        values = {
            "order_id": sale.id,
            "name": self.import_id.product_id.name,
            "product_id": self.import_id.product_id.id,
            "product_uom": self.import_id.product_id.uom_id.id,
            "product_uom_qty": self.quantity,
            "price_unit": self.price_unit,
            "place_of_loading_id": self.charging_point_id.id,
            "place_of_delivery_ids": [(6, 0, self.addressee_ids.ids)],
            "upload_date": self.upload_date,
            "occupation": self.occupation,
            "deca_weight": self.weight,
        }
        return values
