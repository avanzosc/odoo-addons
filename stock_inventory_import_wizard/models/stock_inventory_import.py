# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression

from odoo.addons.base_import_wizard.models.base_import import check_number, convert2str


class StockInventoryImport(models.Model):
    _name = "stock.inventory.import"
    _inherit = "base.import"
    _description = "Wizard to import inventory"

    import_line_ids = fields.One2many(
        comodel_name="stock.inventory.import.line",
    )
    inventory_line_count = fields.Integer(
        string="# Inventory Lines",
        compute="_compute_inventory_line_count",
    )
    lot_create = fields.Boolean(
        string="Create Lot",
        default=False,
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            inventory_product = row_values.get("Descripcion", "")
            inventory_product_code = row_values.get("Codigo", "")
            inventory_location = row_values.get("Ubicacion", "")
            inventory_lot = row_values.get("Lote", "")
            inventory_owner = row_values.get("Propietario", "")
            inventory_package = row_values.get("Paquete", "")
            inventory_product_qty = row_values.get("Cantidad", 0.0)
            log_info = ""
            if not inventory_product and not inventory_location:
                return {}
            values.update(
                {
                    "inventory_product": convert2str(inventory_product),
                    "inventory_product_code": convert2str(inventory_product_code),
                    "inventory_location": convert2str(inventory_location),
                    "inventory_lot": convert2str(inventory_lot),
                    "inventory_owner": convert2str(inventory_owner),
                    "inventory_package": convert2str(inventory_package),
                    "inventory_product_qty": check_number(inventory_product_qty),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_inventory_line_count(self):
        for record in self:
            record.inventory_line_count = len(record.mapped("import_line_ids.quant_id"))

    def button_open_inventory(self):
        self.ensure_one()
        quants = self.mapped("import_line_ids.quant_id")
        action = self.env["stock.quant"].action_view_inventory()
        action["domain"] = [("id", "in", quants.ids)]
        return action


class StockInventoryImportLine(models.Model):
    _name = "stock.inventory.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import inventory lines"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="inventory_location_id.company_id",
        store=True,
    )
    import_id = fields.Many2one(
        comodel_name="stock.inventory.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
    )
    quant_id = fields.Many2one(
        string="Quant",
        comodel_name="stock.quant",
    )
    inventory_product = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_location = fields.Char(
        string="Location Name",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    inventory_lot = fields.Char(
        string="Lot Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_owner = fields.Char(
        string="Owner Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_package = fields.Char(
        string="Package Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_product_qty = fields.Float(
        string="Product Qty",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        domain=[("type", "=", "product")],
        states={"done": [("readonly", True)]},
    )
    inventory_location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_lot_id = fields.Many2one(
        comodel_name="stock.lot",
        string="Lot",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_owner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Owner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_package_id = fields.Many2one(
        comodel_name="stock.quant.package",
        string="Package",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        self.ensure_one()
        update_values = super()._action_validate()
        log_infos = []
        product = lot = owner = package = False
        location, log_info_location = self._check_location()
        if log_info_location:
            log_infos.append(log_info_location)
        if location:
            company = location.company_id
            product, log_info_product = self._check_product(company)
            if log_info_product:
                log_infos.append(log_info_product)
            if product:
                lot, log_info_lot = self._check_lot(product=product, company=company)
                if log_info_lot:
                    log_infos.append(log_info_lot)
            if self.inventory_owner:
                owner, log_info_owner = self._check_owner(company)
                if log_info_owner:
                    log_infos.append(log_info_owner)
            if self.inventory_package:
                package, log_info_package = self._check_package(company)
                if log_info_package:
                    log_infos.append(log_info_package)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "inventory_product_id": product and product.id,
                "inventory_location_id": location and location.id,
                "inventory_lot_id": lot and lot.id,
                "inventory_owner_id": owner and owner.id,
                "inventory_package_id": package and package.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        self.ensure_one()
        update_values = super()._action_process()
        if (
            self.import_id.lot_create
            and self.inventory_lot
            and not self.inventory_lot_id
            and self.inventory_product_id.tracking in ("serial", "lot")
        ):
            lot, log_info = self._check_lot(self.inventory_product_id)
            if not lot:
                lot = self.env["stock.lot"].create(
                    {
                        "product_id": self.inventory_product_id.id,
                        "name": self.inventory_lot,
                        "company_id": self.company_id.id,
                    }
                )
            self.inventory_lot_id = lot
        quant_obj = self.env["stock.quant"].with_company(self.company_id)
        domain = [
            ("product_id", "=", self.inventory_product_id.id),
            ("lot_id", "=", self.inventory_lot_id.id),
            ("location_id", "=", self.inventory_location_id.id),
            ("owner_id", "=", self.inventory_owner_id.id),
            ("package_id", "=", self.inventory_package_id.id),
        ]
        quant = quant_obj.search(domain, limit=1)
        if quant:
            quant.write({"inventory_quantity": self.inventory_product_qty})
            quant.action_apply_inventory()
        else:
            quant = quant_obj.create(
                {
                    "product_id": self.inventory_product_id.id,
                    "lot_id": self.inventory_lot_id.id,
                    "location_id": self.inventory_location_id.id,
                    "owner_id": self.inventory_owner_id.id,
                    "package_id": self.inventory_package_id.id,
                    "inventory_quantity": self.inventory_product_qty,
                }
            )
            quant.action_apply_inventory()
        update_values.update(
            {
                "quant_id": quant.id,
                "state": "done",
            }
        )
        return update_values

    def _check_location(self):
        self.ensure_one()
        log_info = ""
        if self.inventory_location_id:
            return self.inventory_location_id, log_info
        location_obj = self.env["stock.location"]
        search_domain = [
            ("usage", "=", "internal"),
            "|",
            ("complete_name", "=", self.inventory_location),
            ("name", "=", self.inventory_location),
        ]
        locations = location_obj.search(search_domain)
        if not locations:
            log_info = _("No location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _(
                "More than one location with name %(location_name)s found."
            ) % {
                "location_name": self.inventory_location,
            }
        return locations and locations[:1], log_info

    def _check_product(self, company=False):
        self.ensure_one()
        log_info = ""
        if self.inventory_product_id:
            return self.inventory_product_id, log_info
        product_obj = self.env["product.product"].with_company(company)
        search_domain = [("type", "=", "product")]
        if self.inventory_product_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.inventory_product_code)], search_domain]
            )
        else:
            search_domain = expression.AND(
                [[("name", "=", self.inventory_product)], search_domain]
            )
        products = product_obj.search(search_domain)
        if not products:
            log_info = _("No product %(product_name)s found.") % {
                "product_name": self.inventory_product_code or self.inventory_product,
            }
        elif len(products) > 1:
            products = False
            log_info = _("More than one product %(product_name)s found.") % {
                "product_name": self.inventory_product_code or self.inventory_product,
            }
        return products and products[:1], log_info

    def _check_lot(self, product=False, company=False):
        self.ensure_one()
        log_info = ""
        if product.tracking not in ("serial", "lot") and self.inventory_lot:
            return False, _("Untraceable product, but has lot.")
        if product.tracking not in ("serial", "lot") and not self.inventory_lot:
            return False, log_info
        if product.tracking in ("serial", "lot") and not self.inventory_lot:
            return False, _("Lot required for product %(product_name)s.") % {
                "product_name": product.display_name,
            }
        if self.inventory_lot_id:
            return self.inventory_lot_id, log_info
        lot_obj = self.env["stock.lot"].with_company(company)
        search_domain = [
            ("name", "=", self.inventory_lot),
            ("product_id", "=", product.id),
        ]
        lots = lot_obj.search(search_domain)
        if not lots:
            log_info = _(
                "No lot with name %(lot_name)s found for product %(product_name)s."
            ) % {
                "lot_name": self.inventory_lot,
                "product_name": product.display_name,
            }
            if self.import_id.lot_create and self.inventory_lot:
                log_info = ""
        elif len(lots) > 1:
            lots = False
            log_info = _(
                "More than one lot with name %(lot_name)s and product %(product_name)s "
                "found."
            ) % {
                "lot_name": self.inventory_lot,
                "product_name": product.display_name,
            }
        return lots and lots[:1], log_info

    def _check_owner(self, company=False):
        self.ensure_one()
        log_info = ""
        if self.inventory_owner_id:
            return self.inventory_owner_id, log_info
        owner_obj = self.env["res.partner"]
        search_domain = [
            ("name", "=", self.inventory_owner),
            "|",
            ("company_id", "=", company.id),
            ("company_id", "=", False),
        ]
        owners = owner_obj.search(search_domain)
        if not owners:
            log_info = _("No owner found.")
        elif len(owners) > 1:
            owners = False
            log_info = _("More than one owner with name %(owner_name)s found.") % {
                "owner_name": self.inventory_owner,
            }
        return owners and owners[:1], log_info

    def _check_package(self, company=False):
        self.ensure_one()
        log_info = ""
        if self.inventory_package_id:
            return self.inventory_package_id, log_info
        package_obj = self.env["stock.quant.package"]
        search_domain = [
            ("name", "=", self.inventory_package),
            "|",
            ("company_id", "=", company.id),
            ("company_id", "=", False),
        ]
        packages = package_obj.search(search_domain)
        if not packages:
            log_info = _("No package found.")
        elif len(packages) > 1:
            packages = False
            log_info = _("More than one package with name %(package_name)s found.") % {
                "package_name": self.inventory_package,
            }
        return packages and packages[:1], log_info
