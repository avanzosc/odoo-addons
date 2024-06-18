# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.standard_price",
        "base_cost",
        "extra_cost",
    )
    def _compute_standard_price(self):
        for product in self:
            product.standard_price = product.base_cost + product.extra_cost

    def _update_fix_price(self, vals):
        pass

    price_cost_changed = fields.Boolean(string="Price/Cost Changed", default=False)
    sale_configuration = fields.Boolean(
        string="Sale conf: Base + Attributes", default=False
    )
    standard_price = fields.Float(
        string="Total cost (base + extra)",
        compute=False,
        inverse=False,
        search=False,
        store=True,
        copy=False,
    )
    product_category_sale_price_id = fields.Many2one(
        string="Product category sale price",
        comodel_name="product.category.sale.price",
        copy=False,
    )
    base_cost = fields.Float(string="Base cost", copy=False, default=0.0)
    extra_cost = fields.Float(string="Extra cost", copy=False, default=0.0)
    target_cost = fields.Float(string="Target cost", copy=False, default=0.0)
    manual_pvp = fields.Boolean(string="Manual PSP", default=False, copy=False)
    generate_last_price_change_date = fields.Boolean(
        string="Generate last price change date", default=False, copy=False
    )
    last_price_change_date = fields.Date(string="Last price change date", copy=False)
    only_read_prices = fields.Boolean(
        string="Only read prices", compute="_compute_only_read_prices", copy=False
    )
    my_standard_price = fields.Float(
        string="Total cost (base + extra)",
        default=1.0,
        copy=False,
        digits="Product Price",
        help="Price at which the product is sold to customers.",
    )
    my_list_price = fields.Float(
        string="Sales Price",
        default=1.0,
        copy=False,
        digits="Product Price",
        help="Price at which the product is sold to customers.",
    )
    separator_1 = fields.Char(string="||", default="||")
    new_extra_cost = fields.Float(string="New extra cost", copy=False, default=0.0)
    last_change_date_new_extra_cost = fields.Date(
        string="Last change date new extra cost", readonly=True, copy=False
    )
    new_target_cost = fields.Float(string="New target cost", copy=False, default=0.0)
    new_product_category_sale_price_id = fields.Many2one(
        string="New Product category sale price",
        comodel_name="product.category.sale.price",
        copy=False,
    )
    new_sale_price = fields.Float(
        string="New sale price",
        digits="Product Price",
        default=0.0,
        copy=False,
    )
    my_new_sale_price = fields.Float(
        string="New sale price",
        digits="Product Price",
        default=0.0,
        copy=False,
    )
    last_new_sale_price_change_date = fields.Date(
        string="Last change date new sale price", copy=False
    )
    separator_2 = fields.Char(string="||", default="||")
    percentage_between_costs = fields.Float(
        string="Percentage between costs",
        digits=(16, 2),
        compute="_compute_percentage_between_costs",
        copy=False,
        store=True,
    )

    @api.depends("target_cost", "standard_price")
    def _compute_percentage_between_costs(self):
        for template in self:
            percentage_between_costs = -100
            if template.target_cost and template.standard_price:
                percentage_between_costs = (
                    (template.target_cost / template.standard_price) - 1
                ) * 100
            template.percentage_between_costs = percentage_between_costs

    @api.depends("attribute_line_ids")
    def _compute_template_attributes_count(self):
        for template in self:
            template.template_attributes_count = 0

    def _compute_only_read_prices(self):
        group = self.env.ref(
            "product_sale_configuration.allow_change_sale_price", False
        )
        for product in self:
            only_read = True
            if self.env.user.id in group.users.ids:
                only_read = False
            product.only_read_prices = only_read

    @api.onchange("list_price")
    def _onchange_list_price(self):
        for product in self:
            product.price_cost_changed = True
            if product.manual_pvp:
                product.my_list_price = product.list_price

    @api.onchange("base_cost", "extra_cost")
    def _onchange_base_extra_cost(self):
        for product in self:
            product.price_cost_changed = True
            product.standard_price = product.base_cost + product.extra_cost
            product.my_standard_price = product.base_cost + product.extra_cost

    @api.onchange(
        "manual_pvp",
        "target_cost",
        "new_target_cost",
        "product_category_sale_price_id",
        "new_product_category_sale_price_id",
    )
    def _onchange_category_sale_price(self):
        group = self.env.ref(
            "product_sale_configuration.allow_change_sale_price", False
        )
        if self.env.user.id not in group.users.ids:
            raise ValidationError(
                _(
                    "You do not have permission to change the sale price of the"
                    " product."
                )
            )
        for product in self:
            product.price_cost_changed = True
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" not in self.env.context
            ):
                with_lst_price = True if product.list_price else False
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" in self.env.context
            ):
                with_new_sale_price = True if product.new_sale_price else False
            imp = 0
            new_sale_price = 0
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" not in self.env.context
            ):
                if not product.manual_pvp and product.product_category_sale_price_id:
                    category = product.product_category_sale_price_id
                    imp = (
                        product.target_cost
                        + ((product.target_cost * category.percentage) / 100)
                        + category.fixed_amount
                    )
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" in self.env.context
            ):
                if (
                    not product.manual_pvp
                    and product.new_product_category_sale_price_id
                ):
                    category = product.new_product_category_sale_price_id
                    new_sale_price = (
                        product.new_target_cost
                        + ((product.new_target_cost * category.percentage) / 100)
                        + category.fixed_amount
                    )
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" in self.env.context
            ):
                product.new_sale_price = new_sale_price
                product.my_new_sale_price = new_sale_price
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" not in self.env.context
            ):
                product.list_price = imp
                product.my_list_price = imp
                product.generate_last_price_change_date = True
                product.last_price_change_date = fields.Date.context_today(self)
            title = False
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" not in self.env.context
            ) and (with_lst_price and imp == 0 and product.name):
                title = _("Warning for product: %s") % product.name
                message = _("You just changed the sale price")
                warning = {"title": title, "message": message}
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" in self.env.context
            ) and (with_new_sale_price and new_sale_price == 0 and product.name):
                if not title:
                    title = _("Warning for product: %s") % product.name
                    message = _("You just changed the new sale price")
                    warning = {"title": title, "message": message}
                else:
                    my_message = _("{}, and the new sale price.").format(message)
                    message = my_message
            if title:
                return {"warning": warning}

    @api.model
    def create(self, values):
        if "generate_last_price_change_date" in values and values.get(
            "generate_last_price_change_date", False
        ):
            values.update(
                {
                    "last_price_change_date": fields.Date.context_today(self),
                    "generate_last_price_change_date": False,
                }
            )
        if "my_list_price" in values:
            values["list_price"] = values.get("my_list_price")
        if "my_standard_price" in values:
            values["standard_price"] = values.get("my_standard_price")
        template = super(
            ProductTemplate, self.with_context(product_created_from_template=True)
        ).create(values)
        if template.product_variant_count == 1:
            template.put_template_info_in_product()
        return template

    def write(self, values):
        keys = values.keys()
        if (
            "update_base_cost" not in self.env.context
            and len(keys) == 1
            and "standard_price" in values
        ):
            values["base_cost"] = values.get("standard_price")
            values["standard_price"] = values.get("standard_price") + self.extra_cost
        if "generate_last_price_change_date" in values and values.get(
            "generate_last_price_change_date", False
        ):
            values.update(
                {
                    "last_price_change_date": fields.Date.context_today(self),
                    "generate_last_price_change_date": False,
                }
            )
        if (
            "update_base_cost" in self.env.context
            and len(self) == 1
            and "standard_price" in values
        ):
            values["base_cost"] = values.get("standard_price")
            values["standard_price"] = values.get("standard_price") + self.extra_cost
        if "my_list_price" in values:
            values["list_price"] = values.get("my_list_price")
        if "my_standard_price" in values:
            values["standard_price"] = values.get("my_standard_price")
        if "my_new_sale_price" in values:
            values["new_sale_price"] = values.get("my_new_sale_price")
        if "new_extra_cost" in values:
            values["last_change_date_new_extra_cost"] = fields.Date.context_today(self)
        if "new_sale_price" in values:
            values["last_new_sale_price_change_date"] = fields.Date.context_today(self)
        found = False
        if "price_cost_changed" in values and values.get("price_cost_changed", False):
            del values["price_cost_changed"]
            found = True
        result = super().write(values)
        if found:
            for template in self:
                if template.product_variant_count == 1:
                    template.put_template_info_in_product()
        return result

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        self.ensure_one()
        result = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        #        quantity = self.env.context.get('quantity', add_qty)
        #        context = dict(self.env.context, quantity=quantity, pricelist=pricelist.id if pricelist else False)
        #        product_template = self.with_context(context)
        #        if product_template.sale_configuration and 'price' in result:
        #            imp = result.get('price') + product_template.list_price
        #            result['price'] = imp
        return result

    def put_template_info_in_product(self):
        vals = {}
        product = self.product_variant_ids[0]
        if product.standard_price != self.standard_price:
            vals["standard_price"] = self.standard_price
        if (
            product.product_category_sale_price_id
            != self.product_category_sale_price_id
        ):
            vals["product_category_sale_price_id"] = (
                self.product_category_sale_price_id.id
                if self.product_category_sale_price_id
                else None
            )
        if product.base_cost != self.base_cost:
            vals["base_cost"] = self.base_cost
        if product.extra_cost != self.extra_cost:
            vals["extra_cost"] = self.extra_cost
        if product.target_cost != self.target_cost:
            vals["target_cost"] = self.target_cost
        if product.manual_pvp != self.manual_pvp:
            vals["manual_pvp"] = self.manual_pvp
        if product.my_standard_price != self.my_standard_price:
            vals["my_standard_price"] = self.my_standard_price
        if product.my_list_price != self.my_list_price:
            vals["my_list_price"] = self.my_list_price
        if product.lst_price != self.list_price:
            vals["lst_price"] = self.my_list_price
        if product.new_extra_cost != self.new_extra_cost:
            vals["new_extra_cost"] = self.new_extra_cost
        if product.new_target_cost != self.new_target_cost:
            vals["new_target_cost"] = self.new_target_cost
        if (
            product.new_product_category_sale_price_id
            != self.new_product_category_sale_price_id
        ):
            vals["new_product_category_sale_price_id"] = (
                self.new_product_category_sale_price_id.id
                if self.new_product_category_sale_price_id
                else None
            )
        if product.new_sale_price != self.new_sale_price:
            vals["new_sale_price"] = self.new_sale_price
        if product.my_new_sale_price != self.my_new_sale_price:
            vals["my_new_sale_price"] = self.my_new_sale_price
        product.write(vals)
        if (
            product.last_new_sale_price_change_date
            != self.last_new_sale_price_change_date
        ):
            product.last_new_sale_price_change_date = (
                self.last_new_sale_price_change_date
            )
        if product.last_price_change_date != self.last_price_change_date:
            product.last_price_change_date = self.last_price_change_date
        if (
            product.last_change_date_new_extra_cost
            != self.last_change_date_new_extra_cost
        ):
            product.last_change_date_new_extra_cost = (
                self.last_change_date_new_extra_cost
            )


class ProductProduct(models.Model):
    _inherit = "product.product"

    template_attributes_count = fields.Integer(
        string="Template attributes count",
        store=True,
        compute="_compute_template_attributes_count",
    )

    @api.depends("product_tmpl_id", "product_tmpl_id.attribute_line_ids")
    def _compute_template_attributes_count(self):
        for product in self.filtered(lambda x: x.product_tmpl_id):
            product.template_attributes_count = len(
                product.product_tmpl_id.attribute_line_ids
            )

    def _inverse_product_lst_price(self):
        pass

    @api.depends("fix_price")
    def _compute_lst_price(self):
        uom_model = self.env["uom.uom"]
        for product in self:
            price = product.fix_price
            if "uom" in self.env.context:
                price = product.uom_id._compute_price(
                    price, uom_model.browse(self.env.context["uom"])
                )
            product.lst_price = price

    def _compute_list_price(self):
        uom_model = self.env["uom.uom"]
        for product in self:
            price = product.fix_price
            if "uom" in self.env.context:
                price = product.uom_id._compute_price(
                    price, uom_model.browse(self.env.context["uom"])
                )
            product.list_price = price
