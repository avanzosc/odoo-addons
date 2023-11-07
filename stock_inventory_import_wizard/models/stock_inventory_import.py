# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockInventoryImport(models.Model):
    _name = "stock.inventory.import"
    _inherit = "base.import"
    _description = "Wizard to import inventory"

    import_inventory_id = fields.Many2one(
        comodel_name="stock.inventory", string="Inventory"
    )
    import_line_ids = fields.One2many(
        comodel_name="stock.inventory.import.line",
    )
    inventory_line_count = fields.Integer(
        string="# Inventory Lines",
        compute="_compute_inventory_line_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env["res.company"]._company_default_get(
            "stock.inventory.import"),
    )
    lot_create = fields.Boolean(
        string="Create Lot",
        default=False,
    )

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            inventory_product = row_values.get("Descripcion", "")
            inventory_product_code = row_values.get("Codigo", "")
            inventory_location = row_values.get("Ubicacion", "")
            inventory_lot = row_values.get("Lote", "")
            inventory_product_qty = row_values.get("Cantidad", "")
            log_info = ""
            if (
                not inventory_product
                and not (inventory_lot)
                and not (inventory_location)
            ):
                return {}
            values.update(
                {
                    "inventory_product": inventory_product,
                    "inventory_product_code": inventory_product_code,
                    "inventory_location": inventory_location,
                    "inventory_lot": inventory_lot,
                    "inventory_product_qty": inventory_product_qty,
                    "log_info": log_info,
                }
            )
        return values

    def _compute_inventory_line_count(self):
        for record in self:
            record.inventory_line_count = len(
                record.mapped("import_line_ids.inventory_line_id")
            )

    def _create_inventory(self):
        values = {
            "name": _("Imported Inventory"),
            "prefill_counted_quantity": "counted",
            "company_id": self.company_id.id,
            "date": self.file_date,
            "start_empty": True,
        }
        inventory = self.env["stock.inventory"].create(values)
        inventory.action_start()
        return inventory

    def action_process(self):
        for wiz in self:
            if not wiz.import_inventory_id:
                inventory = wiz._create_inventory()
                wiz.write(
                    {
                        "import_inventory_id": inventory.id,
                    }
                )
        return super().action_process()

    def button_open_inventory(self):
        self.ensure_one()
        action = self.env.ref("stock.action_inventory_form")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "=", self.import_inventory_id.id)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def button_open_inventory_line(self):
        self.ensure_one()
        inventory_lines = self.mapped("import_line_ids.inventory_line_id")
        action = self.env.ref(
            "stock_inventory_import_wizard.action_stock_inventory_line"
        )
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", inventory_lines.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class StockInventoryImportLine(models.Model):
    _name = "stock.inventory.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import inventory lines"

    import_inventory_id = fields.Many2one(
        comodel_name="stock.inventory",
        related="import_id.import_inventory_id",
        store=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="import_id.company_id",
        store=True,
    )
    import_id = fields.Many2one(
        comodel_name="stock.inventory.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete="cascade",
    )
    inventory_line_id = fields.Many2one(
        string="Inventory Line",
        comodel_name="stock.inventory.line",
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
    inventory_product_qty = fields.Char(
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
        comodel_name="stock.production.lot",
        string="Lot",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        self.ensure_one()
        update_values = super()._action_validate()
        log_infos = []
        lot = False
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        if product:
            lot, log_info_lot = self._check_lot(product)
            if log_info_lot:
                log_infos.append(log_info_lot)
        location, log_info_location = self._check_location()
        if log_info_location:
            log_infos.append(log_info_location)
        state = "error" if log_infos else "pass"
        action = "create" if state != "error" else "nothing"
        update_values.update(
            {
                "inventory_product_id": product and product.id,
                "inventory_location_id": location and location.id,
                "inventory_lot_id": lot and lot.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        self.ensure_one()
        update_values = super()._action_process()
        if not self.import_id.import_inventory_id:
            self.import_id.import_inventory_id = self.import_id._create_inventory()
        inventory_line = self._create_inventory_line(self.import_id.import_inventory_id)
        update_values.update(
            {
                "inventory_line_id": inventory_line.id,
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
            ("display_name", "=", self.inventory_location),
            ("name", "=", self.inventory_location),
        ]
        print(search_domain)
        locations = location_obj.search(search_domain)
        for line in locations:
            print(line.display_name)
        if not locations:
            log_info = _("No location found.")
        elif len(locations) > 1:
            locations = False
            log_info = _(
                "More than one location with name %(location_name)s already exist."
            ) % {
                "location_name": self.inventory_location,
            }
        return locations and locations[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.inventory_product_id:
            return self.inventory_product_id, log_info
        product_obj = self.env["product.product"]
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
            log_info = _("More than one product %(product_name)s already exist.") % {
                "product_name": self.inventory_product_code or self.inventory_product,
            }
        return products and products[:1], log_info

    def _check_lot(self, product):
        self.ensure_one()
        log_info = ""
        if product.tracking not in ("serial", "lot"):
            return False, log_info
        elif not self.inventory_lot and not self.inventory_lot_id:
            return False, _("Lot required for product %(product_name)s.") % {
                "product_name": product.display_name,
            }
        if self.inventory_lot_id:
            return self.inventory_lot_id, log_info
        search_domain = [
            ("name", "=", self.inventory_lot),
            ("product_id", "=", product.id),
            ("company_id", "=", self.import_id.company_id.id),
        ]
        lots = self.env["stock.production.lot"].search(search_domain)
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
                "already exist."
            ) % {
                "lot_name": self.inventory_lot,
                "product_name": product.display_name,
            }
        return lots and lots[:1], log_info

    def _create_inventory_line(self, inventory):
        self.ensure_one()
        return (
            self.sudo()
            .env["stock.inventory.line"]
            .create(self._inventory_line_values(inventory))
        )

    def _inventory_line_values(self, inventory):
        self.ensure_one()
        lot = self.inventory_lot_id
        if (
            self.import_id.lot_create
            and self.inventory_lot
            and not lot
            and self.inventory_product_id.tracking in ("serial", "lot")
        ):
            lot, log_info = self._check_lot(self.inventory_product_id)
            if not lot:
                lot = self.env["stock.production.lot"].create(
                    {
                        "product_id": self.inventory_product_id.id,
                        "name": self.inventory_lot,
                        "company_id": self.company_id.id,
                    }
                )
            self.inventory_lot_id = lot
        return {
            "inventory_id": inventory.id,
            "product_id": self.inventory_product_id.id,
            "location_id": self.inventory_location_id.id,
            "prod_lot_id": lot and lot.id,
            "product_qty": self.inventory_product_qty,
        }
