# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    price_cost_changed = fields.Boolean(string="Price/Cost Changed", default=False)
    sale_configuration = fields.Boolean(
        string="Sale conf: Base + Attributes", default=True
    )
    manual_pvp = fields.Boolean(string="Manual PSP", default=False, copy=False)
    generate_last_price_change_date = fields.Boolean(
        string="Generate last price change date", default=False, copy=False
    )
    only_read_prices = fields.Boolean(
        string="Only read prices", compute="_compute_only_read_prices"
    )
    my_standard_price = fields.Float(
        string="Total cost (base + extra)",
        default=1.0,
        digits="Product Price",
        help="Price at which the product is sold to customers.",
    )
    my_list_price = fields.Float(
        string="Sales Price",
        default=1.0,
        digits="Product Price",
        help="Price at which the product is sold to customers.",
    )
    standard_price = fields.Float(string="Total cost (base + extra)")
    base_cost = fields.Float(string="Base cost", copy=False, default=0.0)
    extra_cost = fields.Float(string="Extra cost", copy=False, default=0.0)
    product_category_sale_price_id = fields.Many2one(
        string="Product category sale price",
        comodel_name="product.category.sale.price",
        copy=False,
    )
    target_cost = fields.Float(string="Target cost", copy=False, default=0.0)
    percentage_between_costs = fields.Float(
        string="Percentage between costs",
        digits=(16, 2),
        compute="_compute_percentage_between_costs",
        copy=False,
        store=True,
    )
    last_price_change_date = fields.Date(string="Last price change date", copy=False)
    separator_1 = fields.Char(string="||", default="||")
    new_extra_cost = fields.Float(string="New extra cost", copy=False, default=0.0)
    last_change_date_new_extra_cost = fields.Date(
        string="Last change date new extra cost", readonly=True
    )
    new_target_cost = fields.Float(string="New target cost", copy=False, default=0.0)
    new_product_category_sale_price_id = fields.Many2one(
        string="New Product category sale price",
        comodel_name="product.category.sale.price",
        copy=False,
    )
    new_sale_price = fields.Float(
        string="New sale price", digits="Product Price", default=0.0
    )
    my_new_sale_price = fields.Float(
        string="New sale price", digits="Product Price", default=0.0
    )
    last_new_sale_price_change_date = fields.Date(
        string="Last change date new sale price"
    )
    separator_2 = fields.Char(string="||", default="||")

    @api.depends("target_cost", "standard_price")
    def _compute_percentage_between_costs(self):
        for template in self:
            percentage_between_costs = -100
            if template.target_cost and template.standard_price:
                percentage_between_costs = (
                    (template.target_cost / template.standard_price) - 1
                ) * 100
            template.percentage_between_costs = percentage_between_costs

    def _compute_only_read_prices(self):
        group = self.env.ref(
            "product_sale_configuration.allow_change_sale_price", False
        )
        for product in self:
            only_read = True
            if self.env.user.id in group.users.ids:
                only_read = False
            product.only_read_prices = only_read

    @api.onchange("lst_price")
    def _onchange_lst_price(self):
        for product in self:
            product.price_cost_changed = True
            if product.manual_pvp:
                product.my_list_price = product.lst_price

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
        if self.env.user.id != 1 and self.env.user.id not in group.users.ids:
            raise ValidationError(
                _(
                    "You do not have permission to change the sale price of the"
                    " product."
                )
            )
        for product in self.filtered(lambda x: x.template_attributes_count == 0):
            product.price_cost_changed = True
            if (
                "change_manual_pvp" in self.env.context
                or "change_new_target_data" not in self.env.context
            ):
                with_lst_price = True if product.lst_price else False
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
                product.lst_price = imp
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
            values["lst_price"] = values.get("my_list_price")
        if "my_standard_price" in values:
            values["standard_price"] = values.get("my_standard_price")
        product = super().create(values)
        if product.product_tmpl_id.product_variant_count == 1:
            if "product_created_from_template" not in self.env.context:
                product.put_product_info_in_template()
        return product

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
            values["lst_price"] = values.get("my_list_price")
        if "my_standard_price" in values:
            values["standard_price"] = values.get("my_standard_price")
        if "lst_price" in values:
            values.update({"list_price": values.get("lst_price")})
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
        if found and "product_created_from_template" not in self.env.context:
            for product in self:
                if product.product_tmpl_id.product_variant_count == 1:
                    product.put_product_info_in_template()
        return result

    def put_product_info_in_template(self):
        vals = {}
        template = self.product_tmpl_id
        if template.standard_price != self.standard_price:
            vals["standard_price"] = self.standard_price
        if (
            template.product_category_sale_price_id
            != self.product_category_sale_price_id
        ):
            vals["product_category_sale_price_id"] = (
                self.product_category_sale_price_id.id
                if self.product_category_sale_price_id
                else None
            )
        if template.base_cost != self.base_cost:
            vals["base_cost"] = self.base_cost
        if template.extra_cost != self.extra_cost:
            vals["extra_cost"] = self.extra_cost
        if template.target_cost != self.target_cost:
            vals["target_cost"] = self.target_cost
        if template.manual_pvp != self.manual_pvp:
            vals["manual_pvp"] = self.manual_pvp
        if template.my_standard_price != self.my_standard_price:
            vals["my_standard_price"] = self.my_standard_price
        if template.my_list_price != self.my_list_price:
            vals["my_list_price"] = self.my_list_price
        if template.list_price != self.lst_price:
            vals["list_price"] = self.my_list_price
        if template.new_extra_cost != self.new_extra_cost:
            vals["new_extra_cost"] = self.new_extra_cost
        if template.new_target_cost != self.new_target_cost:
            vals["new_target_cost"] = self.new_target_cost
        if (
            template.new_product_category_sale_price_id
            != self.new_product_category_sale_price_id
        ):
            vals["newproduct_category_sale_price_id"] = (
                self.new_product_category_sale_price_id.id
                if self.new_product_category_sale_price_id
                else None
            )
        if template.new_sale_price != self.new_sale_price:
            vals["new_sale_price"] = self.new_sale_price
        if template.my_new_sale_price != self.my_new_sale_price:
            vals["my_new_sale_price"] = self.my_new_sale_price
        template.write(vals)
        if (
            template.last_new_sale_price_change_date
            != self.last_new_sale_price_change_date
        ):
            template.last_new_sale_price_change_date = (
                self.last_new_sale_price_change_date
            )
        if template.last_price_change_date != self.last_price_change_date:
            template.last_price_change_date = self.last_price_change_date
        if (
            template.last_change_date_new_extra_cost
            != self.last_change_date_new_extra_cost
        ):
            template.last_change_date_new_extra_cost = (
                self.last_change_date_new_extra_cost
            )
