# Copyright 2022 Patxi Lersundi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductImport(models.Model):
    _name = "product.import"
    _inherit = "base.import"
    _description = "Wizard to import products"

    import_line_ids = fields.One2many(
        comodel_name="product.import.line",
        inverse_name="import_id",
        )
    product_type = fields.Selection(
        selection="_get_selection_product_type",
        string="Default Product Type",
        default='product',
    )
    uom_id = fields.Many2one(
        string="Default Unit of Measure",
        comodel_name="uom.uom",
    )
    product_count = fields.Integer(
        string="# Products",
        compute="_compute_product_count",
    )
    variants_count = fields.Integer(
        string="# Variants",
        compute="_compute_variants_count",
    )

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(
            allfields=["type"])["type"]["selection"]

    # Get values from file
    def _get_line_values(self, row_values={}):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        product_name = row_values.get("Product Name", "").strip()
        product_code = row_values.get("Product Code", "").strip()
        category_name = row_values.get("Category Name", "").strip()
        uom_name = row_values.get("UoM Name", "").strip()
        product_type_name = row_values.get("Product Type Name", "").strip()
        attribute_name = row_values.get("Attribute Name", "").strip()
        attribute_values = row_values.get("Attribute Values", "").strip()
        product_list_price = row_values.get("Product Sales Price", "")
        product_standard_price = row_values.get("Product Cost", "")
        log_info = ""
        if not product_name:
            if product_code:
                product_name = product_code
                log_info = _("Product Code added as Product Name")
            else:
                return {}
        values.update({
            "product_name": product_name,
            "product_default_code": product_code,
            "category_name": category_name,
            "product_uom": uom_name,
            "product_type_name": product_type_name,
            "attribute_name": attribute_name,
            "attribute_values": attribute_values,
            "product_list_price": product_list_price,
            "product_standard_price": product_standard_price,
            "log_info": log_info,
        })
        if not uom_name and self.uom_id:
            values.update({
                "product_uom": self.uom_id.name,
                "product_uom_id": self.uom_id.id,
            })
        if product_type_name:
            values.update({
                    "product_type_dest": product_type_name,
            })
        else:
            if self.product_type:
                values.update({
                    "product_type_dest": self.product_type,
                })
        return values

    # Product Templates management
    # 1. Count
    def _compute_product_count(self):
        for record in self:
            record.product_count = (
                len(record.mapped("import_line_ids.product_tmpl_id"))
            )

    # 2. Edit list
    def button_open_product(self):
        self.ensure_one()
        products = self.mapped("import_line_ids.product_tmpl_id")
        action = self.env.ref("product.product_template_action_all")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([[("id", "in", products.ids)],
                                 safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    # Product Variants management
    # 1. Count
    def _compute_variants_count(self):
        for record in self:
            record.variants_count = (
                len(record.mapped("import_line_ids.product_ids"))
            )

    # 2. Edit list
    def button_open_variants(self):
        self.ensure_one()
        variants = self.mapped("import_line_ids.product_ids")
        action = self.env.ref("product.product_normal_action")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([[("id", "in", variants.ids)],
                                 safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict


class ProductImportLine(models.Model):
    _name = "product.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import products"

    @api.model
    def _get_selection_product_type(self):
        return self.env["product.product"].fields_get(
            allfields=["type"])["type"]["selection"]

    def default_product_type(self):
        default_dict = self.env["product.product"].default_get(["type"])
        return default_dict.get("type")

    import_id = fields.Many2one(
        comodel_name="product.import",
        string="Import Wizard",
        ondelete="cascade",
        required=True,
    )
    product_name = fields.Char(
        string="Name (in file)",
        required=True,
    )
    product_default_code = fields.Char(
        string="Internal Reference (in file)",
    )
    product_tmpl_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
    )
    product_ids = fields.Many2many(
        string="Products (variants)",
        comodel_name="product.product",
    )
    product_uom = fields.Char(
        string="Unit of Measure (in file)",
    )
    product_uom_id = fields.Many2one(
        string="Unit of Measure",
        comodel_name="uom.uom",
    )
    category_name = fields.Char(
        string="Category Name (in file)",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
    )
    product_type_name = fields.Char(
        string="Product Type (in file)",
    )
    product_type_dest = fields.Selection(
        selection="_get_selection_product_type",
        string="Product Type",
        default=default_product_type,
        required=True,
    )
    attribute_name = fields.Char(
        string="Attribute Name (in file)",
    )
    attribute_id = fields.Many2one(
        string='Attribute',
        comodel_name='product.attribute',
    )
    attribute_values = fields.Char(
        string="Attribute Values (in file)",
    )
    attribute_values_ids = fields.Many2many(
        string="Attribute Values",
        comodel_name='product.attribute.value',
        domain="[('attribute_id','ilike',attribute_id)]",
    )
    product_list_price = fields.Char(
        string="Product Sales Price",
    )
    product_standard_price = fields.Char(
        string="Product Cost",
    )
    sale_ok = fields.Boolean(
        string="Can be Sold",
        default=True,
    )
    purchase_ok = fields.Boolean(
        string="Can be Purchased",
        default=True,
    )

    # Validate Product data
    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""

            product_tmpl, log_info = line._check_product_template()
            if product_tmpl:
                product_ids = [(6, 0, product_tmpl.product_variant_ids.ids)]
                product_category = product_tmpl.categ_id
                product_uom = product_tmpl.uom_id
                product_type_name = product_tmpl.type

                # # By default, as Product Template exists
                # state = "pass"
                state = "error" if log_info else "pass"

                # Add some data from Product Template
                line_values.append((1, line.id, {
                    "product_tmpl_id": product_tmpl and product_tmpl.id,
                    "product_ids": product_ids,
                    "category_name": product_category and product_category.name,
                    "category_id": product_category and product_category.id,
                    "product_uom": product_uom and product_uom.name,
                    "product_uom_id": product_uom and product_uom.id,
                    "product_type_name": product_type_name,
                    "product_type_dest": product_type_name,
                    "product_list_price": product_tmpl.list_price,
                    "product_standard_price": product_tmpl.standard_price,
                    "log_info": log_info,
                    "state": state,
                }))

                # Attribute and values, if used
                if product_tmpl.attribute_line_ids:
                    product_attribute = (
                        product_tmpl.attribute_line_ids[0].attribute_id)
                    product_attribute_value_ids = (
                        product_tmpl.attribute_line_ids[0].value_ids.ids)
                    line_values.append((1, line.id, {
                        "attribute_name": (
                            product_attribute and product_attribute.name),
                        "attribute_id": (
                            product_attribute and product_attribute.id),
                        "attribute_values_ids": [
                            (6, 0, product_attribute_value_ids)],
                    }))
            else:
                # We know Product does not exists, so we "reset" log_info
                log_info = ""

                # Category
                category, error_returned = line._check_category()
                if error_returned:
                    log_info += error_returned

                # Unit of Measure
                if not line.product_uom:
                    if line.import_id.uom_id:
                        line.product_uom = line.import_id.uom_id.name
                uom, error_returned = line._check_uom()
                if error_returned:
                    log_info += error_returned

                # Type
                if not line.product_type_name:
                    if line.import_id.product_type:
                        line.product_type_name = line.import_id.product_type
                    else:
                        line.product_type_name = line.product_type_dest
                        log_info = _("{}{}Error: Product Type not found => "
                                     "Assigning to 'Consumable'").format(
                                         log_info, "\n")

                # Attribute
                # If not found, no error giving
                attribute, error_returned = line._check_attribute()

                # Attribute values
                # If Attribute not found, no need to get Attribute values
                attribute_values_ids = [(5)]
                if attribute:
                    attribute_values_ids, error_returned = (
                            line._check_attribute_values(attribute.id)
                        )
                    if error_returned:
                        log_info += error_returned

                # Remove (if exists) starting "\n"
                log_info = log_info.replace("\n", "", 1)

                # State #
                state = "error" if log_info else "pass"

                line_values.append((1, line.id, {
                    "product_tmpl_id": product_tmpl and product_tmpl.id,
                    "category_id": category and category.id,
                    "product_uom_id": uom and uom.id,
                    "product_type_dest": line.product_type_dest,
                    "attribute_id": attribute and attribute.id,
                    "attribute_values_ids": attribute and attribute_values_ids,
                    "list_price": line.product_list_price,
                    "standard_price": line.product_standard_price,
                    "log_info": log_info,
                    "state": state,
                }))
        return line_values

    # Process Product data: create new Products
    def action_process(self):
        super().action_process()
        line_values = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            product_tmpl, log_info = line._check_product_template()
            if not product_tmpl:
                # Create new Template
                product_tmpl, log_info = line._create_product_template()
                state = "error" if log_info else "done"
                line_values.append((1, line.id, {
                    "product_tmpl_id": product_tmpl.id,
                    "product_ids": [(
                        6, 0, product_tmpl.product_variant_ids.ids
                        )],
                    "log_info": log_info,
                    "state": state,
                }))
            else:
                state = "done"
                log_info = ""
                line.update({
                    "log_info": log_info,
                    "state": state,
                })
        return line_values

    # ---- Checking product data Methods -----

    # Check Product Template
    def _check_product_template(self):
        self.ensure_one()
        error_log = ""

        # Initial checkings
        # Name
        if self.product_name:
            self.product_name.strip()
        else:
            self.product_name = ''
        # Default code
        if self.product_default_code:
            self.product_default_code.strip()
        else:
            self.product_default_code = ''

        product_tmpl_obj = self.env["product.template"]

        # Searching for Product Template
        # First: by Internal Code
        search_domain = [("default_code", "=ilike", self.product_default_code)]
        product_templates = product_tmpl_obj.search(search_domain)
        if len(product_templates) > 1:
            error_log = _(
                "Error: More than one Product template exist with this Code")
        elif not product_templates:
            # Search by Product Name
            if self.product_name:
                search_domain = [("name", "=ilike", self.product_name)]
                product_templates = product_tmpl_obj.search(search_domain)
                if len(product_templates) > 1:
                    error_log = _(
                        "Error: More than one Product template exist with this Name")
                elif not product_templates:
                    error_log = _("Error: Product not found: {}").format(
                        self.product_name)
        return product_templates[:1], error_log

    # Check Product
    def _check_product(self):
        self.ensure_one()
        error_log = ""

        # Initial checkings
        # Name
        if self.product_name:
            self.product_name.strip()
        # Default code
        if self.product_default_code:
            self.product_default_code.strip()
        else:
            self.product_default_code = ''

        product_obj = self.env["product.product"]

        # Searching for Product Template
        # First: by Internal Code
        search_domain = [("default_code", "=ilike", self.product_default_code)]
        products = product_obj.search(search_domain)
        if len(products) > 1:
            error_log = _("Error: More than one Product exist")
        elif not products:
            # Search by Product Name
            if self.product_name:
                search_domain = [("name", "=ilike", self.product_name)]
                products = product_obj.search(search_domain)
                if len(products) > 1:
                    error_log = _("Error: More than one Product exist")
                elif not products:
                    error_log = _("Error: Product not found: {}").format(
                        self.product_name)
        return products[:1], error_log

    # Check Category
    def _check_category(self):
        self.ensure_one()
        error_log = ""

        # Category already selected
        if self.category_id:
            return self.category_id, error_log

        # Initial checkings
        if self.category_name:
            self.category_name.strip()
        else:
            self.category_name = ''

        # Search for Category
        category_obj = self.env["product.category"]
        search_domain = [("name", "=ilike", self.category_name)]
        categories = category_obj.search(search_domain)
        if not categories:
            error_log = _("{}Error: Category not found {}").format(
                "\n", self.category_name)
        elif len(categories) > 1:
            error_log = _(
                "{}Error: More than one product category exist").format("\n")
        return categories[:1], error_log

    # Check Unit of Measure
    def _check_uom(self):
        self.ensure_one()
        error_log = ""

        # UoM already selected
        if self.product_uom_id:
            return self.product_uom_id, error_log

        # Initial checkings
        if self.product_uom:
            self.product_uom.strip()
        else:
            self.product_uom = ''

        # Search for UoM
        uom_obj = self.env["uom.uom"]
        search_domain = [("name", "=ilike", self.product_uom)]
        uoms = uom_obj.search(search_domain)
        if not uoms:
            error_log = _("{}Error: Unit of measure not found {}").format(
                "\n", self.product_uom)
        elif len(uoms) > 1:
            error_log = _(
                "{}Error: More than one Unit of measure exist"
                ).format("\n")
        return uoms[:1], error_log

    # Check Attribute
    def _check_attribute(self):
        self.ensure_one()
        error_log = ""

        # Attribute already selected
        if self.attribute_id:
            return self.attribute_id, error_log

        # Initial checkings
        if self.attribute_name:
            self.attribute_name.strip()
        else:
            self.attribute_name = ''

        # Search for Attribute
        attribute_obj = self.env["product.attribute"]
        search_domain = [("name", "=ilike", self.attribute_name)]
        attributes = attribute_obj.search(search_domain)
        if not attributes:
            error_log = _("{}Error: Attribute not found {}").format(
                "\n", self.attribute_name)
        elif len(attributes) > 1:
            error_log = _("{}Error: More than one attribute exist").format(
                "\n")
        return attributes[:1], error_log

    # Check Attribute values
    def _check_attribute_values(self, attribute_id):
        self.ensure_one()
        error_log = ""
        if self.attribute_values_ids:
            return self.attribute_values_ids, error_log
        attribute_values_obj = self.env["product.attribute.value"]
        separator = ','
        attribute_values_name_list_in_file = (
            self.attribute_values.split(separator))
        attribute_values_name_list = (
            [x.strip(' ') for x in attribute_values_name_list_in_file])
        attribute_values_list_of_id = []
        for attribute_value_name in attribute_values_name_list:
            search_domain = ["&", ("attribute_id", "=", attribute_id),
                             ("name", "=ilike", attribute_value_name)]
            attribute_value = attribute_values_obj.search(search_domain)
            if not attribute_value:
                error_log = _(
                    "{}{}Error: Attribute value not found {}").format(
                        error_log, "\n", attribute_value_name)
            elif len(attribute_value) > 1:
                error_log = _(
                    "{}Error: More than one attribute value exist"
                    ).format("\n")
            else:
                attribute_values_list_of_id.append(attribute_value.id)
        return [(6, 0, attribute_values_list_of_id)], error_log

    # Creating methods for product Template & product

    # Create Product Template
    def _create_product_template(self):
        self.ensure_one()
        error_log = ""

        # First check if Template exists
        product_tmpl, error_log = self._check_product_template()

        # If Template does not exist => let's create it
        if not product_tmpl:
            error_log = ""

            product_tmpl_obj = self.env["product.template"]
            vals = {
                    "name": self.product_name,
                    "uom_id": self.product_uom_id.id,
                    "uom_po_id": self.product_uom_id.id,
                    "categ_id": self.category_id.id,
                    "type": self.product_type_dest,
                    "default_code": self.product_default_code,
            }

            # If Attribute (and values) is used by the user
            if self.attribute_id and self.attribute_values_ids:
                vals['attribute_line_ids'] = [(0, 0, {
                        "attribute_id": self.attribute_id.id,
                        "value_ids": [(6, 0, self.attribute_values_ids.ids)],
                        }
                    )]

            # If Product Sales Price is not used by the user
            if not self.product_list_price:
                self.product_list_price = 0.0
            vals['list_price'] = self.product_list_price

            # If Product Standard Price (Cost) is not used by the user
            if not self.product_standard_price:
                self.product_standard_price = 0.0
            vals['standard_price'] = self.product_standard_price

            # Now its time to create Product Template
            product_tmpl = product_tmpl_obj.create(vals)

        return product_tmpl, error_log

    # Create Product
    def _create_product(self):
        self.ensure_one()
        error_log = ""
        product, error_log = self._check_product()
        if not product and not error_log:
            product_obj = self.env["product.product"]
            product = product_obj.create({
                "name": self.product_name,
                "default_code": self.product_default_code,
                "uom_id": self.product_uom_id.id,
                "uom_po_id": self.product_uom_id.id,
                "categ_id": self.category_id.id,
            })
            error_log = ""
        return product, error_log
