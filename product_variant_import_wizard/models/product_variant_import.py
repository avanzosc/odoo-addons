# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.account.models.product import ACCOUNT_DOMAIN
from odoo.addons.base_import_wizard.models.base_import import (
    convert2bool,
    convert2str,
)

field_column_dict = {
    "product_name": "Nombre",
    "product_code": "Referencia interna",
    "barcode": "Código de barras",
    "description": "Descripción",
    "product_type": "Tipo",
    "sale_ok": "Puede ser vendido",
    "purchase_ok": "Puede ser comprado",
    "category_name": "Categoría",
    "uon_name": "Unidad de medida",
    "purchase_uom_name": "Unidad de medida de compra",
    "property_account_income": "Cuenta Contable Venta",
    "property_account_expense": "Cuenta Contable Compra",
    "list_price": "Precio de venta",
    "standard_price": "Costo",
    "tracking": "Seguimiento",
    "customer_tax": "Impuestos",
    "invoice_policy": "Política de Facturación",
    "purchase_method": "Política de Control",
    "description_purchase": "Descripción para proveedores",
    "internal_category_name": "Categoría interna",
    "brand_name": "Marca",
    "family_name": "Familia",
    "subfamily_name": "Subfamilia",
    "season_name": "Temporada",
    "weight": "Peso",
    "volume": "Volumen",
    "route_name": "Ruta",
    "serie_name": "Serie",
    "top_graphic": "Top Graphic",
    "bottom_graphic": "Bottom Graphic",
}


class ProductVariantImport(models.Model):
    _name = "product.variant.import"
    _inherit = "base.import"
    _description = "Wizard to import product variants"

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(allfields=["type"])["type"][
            "selection"
        ]

    import_line_ids = fields.One2many(
        comodel_name="product.variant.import.line",
    )
    product_type = fields.Selection(
        selection="_get_selection_product_type",
        string="Default Product Type",
        copy=False,
    )
    product_is_storable = fields.Boolean(
        string="Default Track Inventory",
        copy=False,
    )
    uom_id = fields.Many2one(
        string="Default Unit of Measure",
        comodel_name="uom.uom",
        copy=False,
    )
    route_id = fields.Many2one(
        string="Default Inventory Route",
        comodel_name="stock.route",
        copy=False,
    )
    product_count = fields.Integer(
        string="Products",
        compute="_compute_product_count",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company.id,
        copy=False,
    )
    product_found_reference = fields.Boolean(
        string="Found Product Only By Internal Reference",
        default=False,
        copy=False,
    )
    product_found_barcode = fields.Boolean(
        string="Found Product Only By Barcode",
        default=False,
        copy=False,
    )

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        if self.uom_id:
            for line in self.import_line_ids.filtered(
                lambda c: not c.product_uom and (not c.product_uom_id)
            ):
                line.product_uom = self.uom_id.name
                line.product_uom_id = self.uom_id.id

    def _get_line_values(self, row_values=False, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values, datemode=datemode)
        if row_values:
            log_infos = []

            non_attribute_colnames = list(field_column_dict.values())
            product_name = row_values.get(field_column_dict.get("product_name"), "")
            product_code = row_values.get(field_column_dict.get("product_code"), "")
            if not product_name and not product_code:
                return {}
            product_code = convert2str(product_code) if product_code else ""
            barcode = row_values.get(field_column_dict.get("barcode"), "")
            description = row_values.get(field_column_dict.get("description"), "")
            import_line_obj = self.env["product.variant.import.line"]
            row_product_type = row_values.get(field_column_dict.get("product_type"))
            product_type = (
                self.product_type
                or row_product_type
                or import_line_obj.default_product_type()
            )
            product_is_storable = row_product_type == "product" or (
                not row_product_type and self.product_is_storable
            )
            if product_is_storable:
                product_type = "consu"
            sale_ok = convert2bool(
                row_values.get(field_column_dict.get("sale_ok")),
                import_line_obj.default_sale_ok(),
            )
            purchase_ok = convert2bool(
                row_values.get(field_column_dict.get("purchase_ok")),
                import_line_obj.default_purchase_ok(),
            )
            category_name = row_values.get(field_column_dict.get("category_name"), "")
            uom_name = row_values.get(
                field_column_dict.get("uon_name"), self.uom_id.name
            )
            purchase_uom_name = row_values.get(
                field_column_dict.get("purchase_uom_name"), ""
            )
            property_account_income = row_values.get(
                field_column_dict.get("property_account_income"), ""
            )
            property_account_income = (
                convert2str(property_account_income) if property_account_income else ""
            )
            property_account_expense = row_values.get(
                field_column_dict.get("property_account_expense"), ""
            )
            property_account_expense = (
                convert2str(property_account_expense)
                if property_account_expense
                else ""
            )
            list_price = row_values.get(field_column_dict.get("list_price"), "")
            standard_price = row_values.get(field_column_dict.get("standard_price"), "")
            tracking = row_values.get(
                field_column_dict.get("tracking"),
                import_line_obj.default_product_tracking(),
            )
            customer_tax = row_values.get(field_column_dict.get("customer_tax"), "")
            invoice_policy = row_values.get(field_column_dict.get("invoice_policy"), "")
            purchase_method = row_values.get(
                field_column_dict.get("purchase_method"), ""
            )
            description_purchase = row_values.get(
                field_column_dict.get("description_purchase"), ""
            )
            internal_category_name = row_values.get(
                field_column_dict.get("internal_category_name"), ""
            )
            brand_name = row_values.get(field_column_dict.get("brand_name"), "")
            family_name = row_values.get(field_column_dict.get("family_name"), "")
            subfamily_name = row_values.get(field_column_dict.get("subfamily_name"), "")
            season_name = row_values.get(field_column_dict.get("season_name"), "")
            weight = row_values.get(field_column_dict.get("weight"), "")
            volume = row_values.get(field_column_dict.get("volume"), "")
            route_name = row_values.get(field_column_dict.get("route_name"), "")
            serie_name = row_values.get(field_column_dict.get("serie_name"), "")
            top_graphic = row_values.get(field_column_dict.get("top_graphic"), "")
            bottom_graphic = row_values.get(field_column_dict.get("bottom_graphic"), "")
            attributes = {}
            attribute_columns = [
                i for i in row_values.keys() if i not in non_attribute_colnames
            ]
            for col_name in attribute_columns:
                if row_values.get(col_name, False):
                    attributes[col_name] = convert2str(row_values[col_name])
            values.update(
                {
                    "product_name": product_name or product_code,
                    "product_default_code": product_code,
                    "product_barcode": convert2str(barcode),
                    "description": description,
                    "sale_ok": sale_ok,
                    "purchase_ok": purchase_ok,
                    "product_is_storable": product_is_storable,
                    "category_name": category_name,
                    "product_uom": uom_name,
                    "purchase_uom_name": purchase_uom_name,
                    "property_account_income": property_account_income,
                    "property_account_expense": property_account_expense,
                    "list_price": list_price,
                    "standard_price": standard_price,
                    "customer_tax": customer_tax,
                    "description_purchase": description_purchase,
                    "internal_category_name": internal_category_name,
                    "brand_name": brand_name,
                    "family_name": family_name,
                    "subfamily_name": subfamily_name,
                    "season_name": season_name,
                    "weight": weight,
                    "volume": volume,
                    "route_name": route_name,
                    "serie_name": serie_name,
                    "top_graphic": top_graphic,
                    "bottom_graphic": bottom_graphic,
                    "attributes_name": attributes,
                }
            )
            if not product_name:
                log_infos.append(_("Product Code added as Product Name"))
            if product_type:
                if not any(
                    product_type == type
                    for type, _ in (import_line_obj._get_selection_product_type())
                ):
                    log_infos.append(_("Product Type not understood."))
                else:
                    values.update(
                        {
                            "product_type": product_type,
                        }
                    )
            if tracking:
                if not any(
                    tracking == track
                    for track, _ in (import_line_obj._get_selection_product_tracking())
                ):
                    log_infos.append(_("Product tracking not understood."))
                else:
                    values.update(
                        {
                            "product_tracking": tracking,
                        }
                    )
            if purchase_method:
                if not any(
                    purchase_method == method
                    for method, _ in (import_line_obj._get_selection_purchase_method())
                ):
                    log_infos.append(_("Purchase Method not understood."))
                else:
                    values.update(
                        {
                            "purchase_method": purchase_method,
                        }
                    )
            if invoice_policy:
                if not any(
                    invoice_policy == invoice
                    for invoice, _ in (import_line_obj._get_selection_invoice_policy())
                ):
                    log_infos.append(_("Invoice Policy not understood."))
                else:
                    values.update(
                        {
                            "invoice_policy": invoice_policy,
                        }
                    )
            if not route_name and self.route_id:
                values.update(
                    {
                        "route_name": self.route_id.name,
                        "route_id": self.route_id.id,
                    }
                )
            values.update(
                {
                    "log_info": "\n".join(log_infos),
                    "state": "error" if log_infos else "2validate",
                }
            )
        return values

    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.mapped("import_line_ids.product_id"))

    def button_open_product(self):
        self.ensure_one()
        products = self.mapped("import_line_ids.product_id")
        action = self.env.ref("product.product_normal_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", products.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ProductImportLine(models.Model):
    _name = "product.variant.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import product variants"

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(allfields=["type"])["type"][
            "selection"
        ]

    @api.model
    def _get_selection_product_tracking(self):
        return self.env["product.product"].fields_get(allfields=["tracking"])[
            "tracking"
        ]["selection"]

    @api.model
    def _get_selection_purchase_method(self):
        return self.env["product.product"].fields_get(allfields=["purchase_method"])[
            "purchase_method"
        ]["selection"]

    @api.model
    def _get_selection_invoice_policy(self):
        return self.env["product.product"].fields_get(allfields=["invoice_policy"])[
            "invoice_policy"
        ]["selection"]

    def default_product_type(self):
        default_dict = self.env["product.product"].default_get(["type"])
        return default_dict.get("type")

    def default_product_tracking(self):
        default_dict = self.env["product.product"].default_get(["tracking"])
        return default_dict.get("tracking")

    def default_sale_ok(self):
        default_dict = self.env["product.product"].default_get(["sale_ok"])
        return default_dict.get("sale_ok")

    def default_purchase_ok(self):
        default_dict = self.env["product.product"].default_get(["purchase_ok"])
        return default_dict.get("purchase_ok")

    def default_invoice_policy(self):
        default_dict = self.env["product.product"].default_get(["invoice_policy"])
        return default_dict.get("invoice_policy")

    def default_purchase_method(self):
        default_dict = self.env["product.product"].default_get(["purchase_method"])
        return default_dict.get("purchase_method")

    import_id = fields.Many2one(
        comodel_name="product.variant.import",
    )
    action = fields.Selection(
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
        copy=False,
    )
    product_name = fields.Char(
        required=True,
        copy=False,
    )
    product_default_code = fields.Char(
        string="Internal Reference",
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        copy=False,
    )
    product_barcode = fields.Char(
        string="Barcode",
        copy=False,
    )
    description = fields.Char(
        copy=False,
    )
    product_type = fields.Selection(
        string="Type",
        selection="_get_selection_product_type",
        default=default_product_type,
        required=True,
        copy=False,
    )
    sale_ok = fields.Boolean(
        string="Can be Sold",
        default=default_sale_ok,
        copy=False,
    )
    purchase_ok = fields.Boolean(
        string="Can be Purchased",
        default=default_purchase_ok,
        copy=False,
    )
    product_is_storable = fields.Boolean(
        string="Track Inventory",
        copy=False,
    )
    category_name = fields.Char(
        copy=False,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
        copy=False,
    )
    product_uom = fields.Char(
        string="UoM Name",
        copy=False,
    )
    product_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        copy=False,
    )
    purchase_uom_name = fields.Char(
        string="Purchase UoM Name",
        copy=False,
    )
    purchase_uom_id = fields.Many2one(
        string="Purchase UoM",
        comodel_name="uom.uom",
        copy=False,
    )
    property_account_income = fields.Char(
        string="Income Account Name",
        copy=False,
    )
    property_account_income_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
        domain=ACCOUNT_DOMAIN,
        copy=False,
    )
    property_account_expense = fields.Char(
        string="Expense Account Name",
        copy=False,
    )
    property_account_expense_id = fields.Many2one(
        string="Expense Account",
        comodel_name="account.account",
        domain=ACCOUNT_DOMAIN,
        copy=False,
    )
    list_price = fields.Float(
        copy=False,
    )
    standard_price = fields.Float(
        copy=False,
    )
    product_tracking = fields.Selection(
        string="Tracking",
        selection="_get_selection_product_tracking",
        default=default_product_tracking,
        required=True,
        copy=False,
    )
    customer_tax = fields.Char(
        string="Customer Tax Name",
        copy=False,
    )
    customer_tax_id = fields.Many2one(
        string="Customer Tax",
        comodel_name="account.tax",
        copy=False,
    )
    invoice_policy = fields.Selection(
        selection="_get_selection_invoice_policy",
        default=default_invoice_policy,
        copy=False,
    )
    purchase_method = fields.Selection(
        selection="_get_selection_purchase_method",
        default=default_purchase_method,
        copy=False,
    )
    description_purchase = fields.Text(
        string="Purchase Description",
        copy=False,
    )
    top_graphic = fields.Char(
        copy=False,
    )
    bottom_graphic = fields.Char(
        copy=False,
    )
    top_transfer_product_id = fields.Many2one(
        comodel_name="product.product",
        copy=False,
    )
    bottom_transfer_product_id = fields.Many2one(
        comodel_name="product.product",
        copy=False,
    )
    internal_category_name = fields.Char(
        copy=False,
    )
    internal_category_id = fields.Many2one(
        string="Internal Category",
        comodel_name="internal.product.category",
        copy=False,
    )
    brand_name = fields.Char(
        copy=False,
    )
    brand_id = fields.Many2one(
        string="Brand",
        comodel_name="product.brand",
        copy=False,
    )
    family_name = fields.Char(
        copy=False,
    )
    family_id = fields.Many2one(
        string="Family",
        comodel_name="product.category",
        copy=False,
    )
    subfamily_name = fields.Char(
        copy=False,
    )
    subfamily_id = fields.Many2one(
        string="Subfamily",
        comodel_name="product.category",
        copy=False,
    )
    season_name = fields.Char(
        copy=False,
    )
    season_id = fields.Many2one(
        string="Season",
        comodel_name="product.season",
        copy=False,
    )
    serie_name = fields.Char(
        copy=False,
    )
    serie_id = fields.Many2one(
        string="Serie",
        comodel_name="product.series",
        copy=False,
    )
    weight = fields.Float(
        copy=False,
    )
    volume = fields.Float(
        copy=False,
    )
    attributes_name = fields.Char(
        copy=False,
    )
    attribute_ids = fields.Many2many(
        string="Atrributes",
        comodel_name="product.attribute.value",
        relation="rel_import_line_attribute",
        column1="import_line_id",
        column2="attribute_id",
    )
    route_name = fields.Char(
        string="Inventory Route Name",
        copy=False,
    )
    route_id = fields.Many2one(
        string="Inventory Route",
        comodel_name="stock.route",
        copy=False,
    )

    def _action_validate(self):  # noqa: C901
        update_values = super()._action_validate()
        log_infos = []
        tax = purchase_uom = account_income = account_expense = internal_categ = False
        brand = family = subfamily = season = serie = route = False
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        if self.product_barcode:
            log_info_barcode = self._check_barcode()
            if log_info_barcode:
                log_infos.append(log_info_barcode)
        category, log_info_category = self._check_category(product=product)
        if log_info_category:
            log_infos.append(log_info_category)
        top_transfer = bottom_transfer = False
        if category:
            profile_product = self._get_category_profile_product(category)
            if profile_product.requires_transfer:
                transfer_category = profile_product.transfer_category_id
                if not transfer_category:
                    log_infos.append(_("The transfer category is required."))
                else:
                    if self.top_graphic:
                        top_transfer, log_info_top_transfer = (
                            self._check_transfer_product(
                                self.top_graphic, transfer_category
                            )
                        )
                        if log_info_top_transfer:
                            log_infos.append(log_info_top_transfer)
                    if self.bottom_graphic:
                        bottom_transfer, log_info_bottom_transfer = (
                            self._check_transfer_product(
                                self.bottom_graphic, transfer_category
                            )
                        )
                        if log_info_bottom_transfer:
                            log_infos.append(log_info_bottom_transfer)
        uom, log_info_uom = self._check_sale_uom(product=product)
        if log_info_uom:
            log_infos.append(log_info_uom)
        if self.purchase_uom_name:
            purchase_uom, log_info_purchase_uom = self._check_purchase_uom()
            if log_info_purchase_uom:
                log_infos.append(log_info_purchase_uom)
        if self.property_account_income:
            account_income, log_info_income = self._check_account_income()
            if log_info_income:
                log_infos.append(log_info_income)
        if self.property_account_expense:
            account_expense, log_info_expense = self._check_account_expense()
            if log_info_expense:
                log_infos.append(log_info_expense)
        if self.customer_tax:
            tax, log_info_tax = self._check_tax()
            if log_info_tax:
                log_infos.append(log_info_tax)
        if self.internal_category_name:
            internal_categ, log_info_internal_categ = self._check_internal_categ()
            if log_info_internal_categ:
                log_infos.append(log_info_internal_categ)
        if self.brand_name:
            brand, log_info_brand = self._check_brand()
            if log_info_brand:
                log_infos.append(log_info_brand)
        if self.family_name:
            family, log_info_family = self._check_family()
            if log_info_family:
                log_infos.append(log_info_family)
        if self.subfamily_name:
            subfamily, log_info_subfamily = self._check_subfamily()
            if log_info_subfamily:
                log_infos.append(log_info_subfamily)
        if self.season_name:
            season, log_info_season = self._check_season()
            if log_info_season:
                log_infos.append(log_info_season)
        if self.serie_name:
            serie, log_info_serie = self._check_serie()
            if log_info_serie:
                log_infos.append(log_info_serie)
        if self.route_name:
            route, log_info_route = self._check_route()
            if log_info_route:
                log_infos.append(log_info_route)
        attributes = []
        attribute = safe_eval(self.attributes_name) if self.attributes_name else {}
        if category and self._category_requires_shape(category):
            shape_value = next(
                (
                    value
                    for name, value in attribute.items()
                    if name.strip().upper() == "SHAPE"
                ),
                False,
            )
            if not shape_value:
                log_infos.append(_("Shape is required for DECK products."))
        for col in attribute:
            if attribute[col]:
                attr, log_info_attr = self._check_variant(
                    name=col, value=attribute[col]
                )
                if log_info_attr:
                    log_infos.append(log_info_attr)
                if attr and not log_info_attr:
                    attributes.append(attr.id)
        state = "error" if log_infos else "pass"
        action = "nothing"
        if state != "error":
            action = "create"
        update_values.update(
            {
                "product_id": product and product.id,
                "category_id": category and category.id,
                "top_transfer_product_id": top_transfer and top_transfer.id,
                "bottom_transfer_product_id": bottom_transfer and bottom_transfer.id,
                "product_uom_id": uom and uom.id,
                "purchase_uom_id": purchase_uom and purchase_uom.id,
                "customer_tax_id": tax and tax.id,
                "property_account_income_id": account_income and (account_income.id),
                "property_account_expense_id": account_expense and (account_expense.id),
                "internal_category_id": internal_categ and internal_categ.id,
                "brand_id": brand and brand.id,
                "family_id": family and family.id,
                "subfamily_id": subfamily and subfamily.id,
                "season_id": season and season.id,
                "serie_id": serie and serie.id,
                "route_id": route and route.id,
                "attribute_ids": [(6, 0, attributes)],
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _action_process(self):
        update_values = super()._action_process()
        log_info = ""
        product = self.product_id or False
        if self.import_id.company_id:
            self = self.with_company(self.import_id.company_id)
        if self.action == "create":
            product, log_info = self._create_product()
            if product and hasattr(product, "generate_code"):
                product.generate_code()
            if product and not log_info:
                product.product_tmpl_id.action_unify_shape_attributes()
                self._process_transfers(product)
        state = "error" if log_info else "done"
        action = "nothing" if log_info else "create"
        update_values.update(
            {
                "product_id": product and product.id or False,
                "log_info": log_info,
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _get_category_profile_product(self, category):
        return (
            category.attribute_profile_id.default_profile_product_id
            or category.default_profile_product_id
        )

    def _category_requires_shape(self, category):
        profile_name = (category.attribute_profile_id.name or "").strip().upper()
        return profile_name in ("DECK", "DECKS")

    def _check_transfer_product(self, transfer_name, transfer_category):
        products = self.env["product.product"].search(
            [
                ("name", "=", transfer_name),
                ("categ_id", "=", transfer_category.id),
                "|",
                ("company_id", "=", self.import_id.company_id.id),
                ("company_id", "=", False),
            ]
        )
        if len(products) > 1:
            return False, _(
                "More than one transfer product named '%(transfer_name)s' found."
            ) % {"transfer_name": transfer_name}
        return products, ""

    def _process_transfers(self, product):
        profile_product = self._get_category_profile_product(product.categ_id)
        if not profile_product.requires_transfer:
            return
        transfer_category = profile_product.transfer_category_id
        transfer_values = {}
        for graphic_field, line_product_field, product_field in (
            ("top_graphic", "top_transfer_product_id", "top_transfer_product_id"),
            (
                "bottom_graphic",
                "bottom_transfer_product_id",
                "bottom_transfer_product_id",
            ),
        ):
            transfer_name = self[graphic_field]
            if not transfer_name:
                continue
            transfer_product = self[line_product_field]
            if not transfer_product:
                transfer_product, __ = self._check_transfer_product(
                    transfer_name, transfer_category
                )
            if not transfer_product:
                transfer_product = self.env["product.product"].create(
                    {
                        "name": transfer_name,
                        "categ_id": transfer_category.id,
                        "company_id": self.import_id.company_id.id,
                    }
                )
                if hasattr(transfer_product, "generate_code"):
                    transfer_product.generate_code()
            transfer_values[product_field] = transfer_product.id
        if transfer_values:
            product.write(transfer_values)

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = [("name", "=", self.product_name)]
        if self.product_default_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.product_default_code)], search_domain]
            )
            if self.import_id.product_found_reference:
                search_domain = [("default_code", "=", self.product_default_code)]
        if self.product_barcode:
            if self.import_id.product_found_barcode:
                search_domain = [("barcode", "=", self.product_barcode)]
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
        products = product_obj.with_company(self.import_id.company_id).search(
            search_domain
        )
        if len(products) > 1:
            products = False
            log_info = _("More than one product found.")
        return products, log_info

    def _check_category(self, product=False):
        self.ensure_one()
        log_info = ""
        if self.category_id:
            return self.category_id, log_info
        if product and not self.category_name:
            return product.categ_id, log_info
        return self._check_category_name(self.category_name)

    def _check_family(self):
        self.ensure_one()
        log_info = ""
        if self.family_id:
            return self.family_id, log_info
        return self._check_category_name(self.family_name)

    def _check_subfamily(self):
        self.ensure_one()
        log_info = ""
        if self.subfamily_id:
            return self.subfamily_id, log_info
        return self._check_category_name(self.subfamily_name)

    def _check_category_name(self, category_name):
        self.ensure_one()
        log_info = ""
        category_obj = self.env["product.category"]
        search_domain = [
            "|",
            ("name", "=", category_name),
            ("complete_name", "=", category_name),
        ]
        categories = category_obj.search(search_domain)
        if not categories:
            log_info = _("Product category '%(category_name)s' not found.") % {
                "category_name": category_name,
            }
        elif len(categories) > 1:
            categories = False
            log_info = _("More than one product category found.")
        return categories, log_info

    def _check_internal_categ(self):
        self.ensure_one()
        log_info = ""
        if self.internal_category_id:
            return self.internal_category_id, log_info
        internal_categ_obj = self.env["internal.product.category"]
        search_domain = [("name", "=", self.internal_category_name)]
        internal_categs = internal_categ_obj.search(search_domain)
        if not internal_categs:
            internal_categs = False
            log_info = _("Internal category not found.")
        elif len(internal_categs) > 1:
            internal_categs = False
            log_info = _("More than one internal category found.")
        return internal_categs, log_info

    def _check_sale_uom(self, product=False):
        self.ensure_one()
        log_info = ""
        if self.product_uom_id:
            return self.product_uom_id, log_info
        if product and not self.product_uom:
            return product.uom_id, log_info
        return self._check_uom(self.product_uom)

    def _check_purchase_uom(self):
        self.ensure_one()
        log_info = ""
        if self.purchase_uom_id:
            return self.purchase_uom_id, log_info
        return self._check_uom(self.purchase_uom_name)

    def _check_uom(self, uom_name=False):
        self.ensure_one()
        log_info = ""
        uom_obj = self.env["uom.uom"]
        search_domain = [("name", "=", uom_name)]
        uoms = uom_obj.search(search_domain)
        if not uoms:
            log_info = _("Unit of measure not found.")
        elif len(uoms) > 1:
            uoms = False
            log_info = _("More than one unit of measure exist.")
        return uoms and uoms[:1], log_info

    def _check_brand(self):
        self.ensure_one()
        log_info = ""
        if self.brand_id:
            return self.brand_id, log_info
        brand_obj = self.env["product.brand"]
        search_domain = [("name", "=", self.brand_name)]
        brands = brand_obj.search(search_domain)
        if not brands:
            log_info = _("Brand not found.")
        elif len(brands) > 1:
            brands = False
            log_info = _("More than one brand found.")
        return brands and brands[:1], log_info

    def _check_season(self):
        self.ensure_one()
        log_info = ""
        if self.season_id:
            return self.season_id, log_info
        season_obj = self.env["product.season"]
        search_domain = [("name", "ilike", self.season_name)]
        seasons = season_obj.search(search_domain)
        if not seasons:
            log_info = _("Season not found.")
        elif len(seasons) > 1:
            seasons = False
            log_info = _("More than one season found.")
        return seasons and seasons[:1], log_info

    def _check_serie(self):
        self.ensure_one()
        log_info = ""
        if self.serie_id:
            return self.serie_id, log_info
        serie_obj = self.env["product.series"]
        search_domain = [("name", "ilike", self.serie_name)]
        series = serie_obj.search(search_domain)
        if not series:
            log_info = _("Serie not found.")
        elif len(series) > 1:
            series = False
            log_info = _("More than one serie found.")
        return series and series[:1], log_info

    def _check_tax(self):
        self.ensure_one()
        log_info = ""
        if self.customer_tax_id:
            return self.customer_tax_id, log_info
        if not self.customer_tax:
            return False, log_info
        tax_obj = self.env["account.tax"]
        search_domain = [
            "&",
            ("name", "ilike", self.customer_tax),
            "|",
            ("company_id", "=", self.import_id.company_id.id),
            ("company_id", "=", False),
        ]
        taxes = tax_obj.search(search_domain)
        if not taxes:
            log_info = _("Tax not found.")
        elif len(taxes) > 1:
            taxes = False
            log_info = _("More than one taxes found.")
        return taxes and taxes[:1], log_info

    def _check_barcode(self):
        self.ensure_one()
        log_info = ""
        if self.product_barcode:
            same_barcode = self.import_id.import_line_ids.filtered(
                lambda c: c.product_barcode == (self.product_barcode)
                and c.id != self.id
            )
            if same_barcode:
                log_info = _(
                    "There are other lines in this importer with" + " the same barcode."
                )
            same_barcode = self.env["product.product"].search(
                [
                    ("name", "!=", self.product_name),
                    ("barcode", "=", self.product_barcode),
                ]
            )
            if same_barcode:
                log_info = _(
                    "Another product with the same barcode exists" + " in the system."
                )
            return log_info

    def _check_account_income(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_income_id:
            return self.property_account_income_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [
            ("code", "=", self.property_account_income),
        ]
        search_domain = expression.AND(
            [
                safe_eval(
                    ACCOUNT_DOMAIN, {"current_company_id": self.import_id.company_id.id}
                ),
                search_domain,
            ]
        )
        accounts = account_obj.search(search_domain)
        if not accounts:
            log_info = _("Property account income not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("More than one property account income found.")
        return accounts and accounts[:1], log_info

    def _check_account_expense(self):
        self.ensure_one()
        log_info = ""
        if self.property_account_expense_id:
            return self.property_account_expense_id, log_info
        account_obj = self.env["account.account"]
        search_domain = [
            ("code", "=", self.property_account_expense),
        ]
        search_domain = expression.AND(
            [
                safe_eval(
                    ACCOUNT_DOMAIN, {"current_company_id": self.import_id.company_id.id}
                ),
                search_domain,
            ]
        )
        accounts = account_obj.search(search_domain)
        if not accounts:
            log_info = _("Property account expense not found.")
        elif len(accounts) > 1:
            accounts = False
            log_info = _("More than one property account expense found.")
        return accounts and accounts[:1], log_info

    def _check_variant(self, name=False, value=False):
        self.ensure_one()
        log_info = ""
        attribute_values = False
        attribute_obj = self.env["product.attribute"]
        search_domain = [("name", "=ilike", name)]
        attributes = attribute_obj.search(search_domain)
        if not attributes:
            attributes = False
            log_info = _("Attribute {} not found.").format(name)
        elif len(attributes) > 1:
            attributes = False
            log_info = _("More than one attribute {} found.").format(name)
        elif len(attributes) == 1:
            attribute_value_obj = self.env["product.attribute.value"]
            search_domain = [("name", "=", value), ("attribute_id", "=", attributes.id)]
            attribute_values = attribute_value_obj.search(search_domain)
            if not attribute_values:
                attribute_values = False
                log_info = _(
                    "%(value)s value not found for attribute %(attribute)s.",
                    value=value,
                    attribute=name,
                )
            elif len(attribute_values) > 1:
                attribute_values = False
                log_info = _(
                    "More than one attribute value %(value)s found for "
                    "attribute %(attribute)s.",
                    value=value,
                    attribute=name,
                )
        return attribute_values, log_info

    def _check_route(self):
        self.ensure_one()
        log_info = ""
        if self.route_id:
            return self.route_id, log_info
        routes = self.env["stock.route"].search(
            [
                ("name", "=", self.route_name),
                "|",
                ("company_id", "=", self.import_id.company_id.id),
                ("company_id", "=", False),
            ]
        )
        if not routes:
            log_info = _("Inventory route {} not found.").format(self.route_name)
        elif len(routes) > 1:
            routes = False
            log_info = _("More than one inventory route {} found.").format(
                self.route_name
            )
        return routes and routes[:1], log_info

    def _create_product(self):
        self.ensure_one()
        product, log_info = self._check_product()
        if not product and not log_info:
            product_obj = self.env["product.product"]
            values = self._product_values()
            values.update(
                {
                    "name": self.product_name,
                    "company_id": self.import_id.company_id.id,
                }
            )
            product = product_obj.with_company(self.import_id.company_id).create(values)
            product = self._apply_variant_attributes(product, values)
            log_info = ""
        return product, log_info

    def _apply_variant_attributes(self, product, values):
        self.ensure_one()
        if not self.attribute_ids:
            return product
        template = product.product_tmpl_id
        for attribute in self.attribute_ids.mapped("attribute_id"):
            values_for_attribute = self.attribute_ids.filtered(
                lambda value, attribute=attribute: value.attribute_id == attribute
            )
            line = template.attribute_line_ids.filtered(
                lambda tmpl_line, attribute=attribute: (
                    tmpl_line.attribute_id == attribute
                )
            )
            if line:
                line.value_ids = [(4, value.id) for value in values_for_attribute]
            else:
                self.env["product.template.attribute.line"].create(
                    {
                        "product_tmpl_id": template.id,
                        "attribute_id": attribute.id,
                        "value_ids": [(6, 0, values_for_attribute.ids)],
                    }
                )
        template._create_variant_ids()
        combination = template.valid_product_template_attribute_line_ids.mapped(
            "product_template_value_ids"
        ).filtered(lambda value: value.product_attribute_value_id in self.attribute_ids)
        variant = template.product_variant_ids.filtered(
            lambda variant: set(variant.product_template_attribute_value_ids.ids)
            == set(combination.ids)
        )[:1]
        if variant and variant != product:
            variant.write(values)
            return variant
        return product

    def _product_values(self):
        self.ensure_one()
        values = {
            "default_code": self.product_default_code,
            "description": self.description,
            "type": self.product_type,
            "is_storable": self.product_is_storable,
            "sale_ok": self.sale_ok,
            "purchase_ok": self.purchase_ok,
            "categ_id": self.category_id.id,
            "internal_category_id": self.internal_category_id.id,
            "uom_id": self.product_uom_id.id,
            "uom_po_id": self.purchase_uom_id.id or self.product_uom_id.id,
            "property_account_income_id": self.property_account_income_id.id,
            "property_account_expense_id": self.property_account_expense_id.id,
            "list_price": self.list_price,
            "standard_price": self.standard_price,
            "tracking": self.product_tracking,
            "invoice_policy": self.invoice_policy,
            "purchase_method": self.purchase_method,
            "description_purchase": self.description_purchase,
            "product_brand_id": self.brand_id.id,
            "family_id": self.family_id.id,
            "sub_family_id": self.subfamily_id.id,
            "season_id": self.season_id.id,
            "serie_id": self.serie_id.id,
            "volume": self.volume,
            "weight": self.weight,
            "route_ids": [(6, 0, self.route_id.ids)],
        }
        if self.product_barcode:
            values.update(
                {
                    "barcode": self.product_barcode,
                }
            )
        if self.customer_tax_id:
            values.update(
                {
                    "taxes_id": [(4, self.customer_tax_id.id)],
                }
            )
        return values
