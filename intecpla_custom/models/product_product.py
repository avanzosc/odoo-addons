# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductProduct(models.Model):
    _inherit = "product.product"

    min_threshold_percentage_between_costs_id = fields.Many2one(
        string="Min. Threshold percentage between costs",
        comodel_name="threshold.percentage.between.costs",
        copy=False,
    )
    max_threshold_percentage_between_costs_id = fields.Many2one(
        string="Max. Threshold percentage between costs",
        comodel_name="threshold.percentage.between.costs",
        copy=False,
    )
    product_color = fields.Selection(
        string="Product color",
        selection=[
            ("none", _("Without color")),
            ("green", _("Green")),
            ("red", _("Red")),
            ("orange", _("Orange")),
        ],
        compute="_compute_product_color",
        store=True,
        related=False,
    )
    notes_for_cost_sale_price = fields.Text(
        string="Notes for calculating Target Cost and Sale Price",
        copy=False,
        translate=False,
    )

    @api.depends(
        "min_threshold_percentage_between_costs_id",
        "min_threshold_percentage_between_costs_id.threshold_percentage",
        "max_threshold_percentage_between_costs_id",
        "max_threshold_percentage_between_costs_id.threshold_percentage",
        "percentage_between_costs",
        "manual_pvp",
    )
    def _compute_product_color(self):
        for product in self:
            if product.manual_pvp:
                color = "none"
            else:
                min_threshold = product.min_threshold_percentage_between_costs_id
                max_threshold = product.max_threshold_percentage_between_costs_id
                min_percentage = (
                    min_threshold.threshold_percentage if min_threshold else 0
                )
                max_percentage = (
                    max_threshold.threshold_percentage if max_threshold else 0
                )
                if product.percentage_between_costs > max_percentage:
                    color = "green"
                if product.percentage_between_costs < min_percentage:
                    color = "red"
                else:
                    if product.percentage_between_costs <= max_percentage:
                        color = "orange"
            product.product_color = color

    def name_get(self):
        # TDE: this could be cleaned a bit I think

        def _name_get(d):
            name = d.get("name", "")
            code = (
                self._context.get("display_default_code", True)
                and d.get("default_code", False)
                or False
            )
            if code:
                name = "[%s] %s" % (code, name)
            return (d["id"], name)

        partner_id = self._context.get("partner_id")
        if partner_id:
            partner_ids = [
                partner_id,
                self.env["res.partner"].browse(partner_id).commercial_partner_id.id,
            ]
        else:
            pass
        self.check_access_rights("read")
        self.check_access_rule("read")
        result = []
        self.sudo().read(
            [
                "name",
                "default_code",
                "product_tmpl_id",
                "attribute_value_ids",
                "attribute_line_ids",
            ],
            load=False,
        )
        self.sudo().mapped("product_tmpl_id").ids
        for product in self.sudo():
            variable_attributes = product.attribute_line_ids.filtered(
                lambda l: len(l.value_ids) > 1
            ).mapped("attribute_id")
            variant = product.attribute_value_ids._variant_name(variable_attributes)
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            mydict = {
                "id": product.id,
                "name": name,
                "default_code": product.default_code,
            }
            result.append(_name_get(mydict))
        return result

    @api.model_create_multi
    def create(self, vals_list):
        min_threshold_percentage_between_costs = self.env.ref(
            "intecpla_custom.minimum_threshold_percentage_between_costs"
        )
        max_threshold_percentage_between_costs = self.env.ref(
            "intecpla_custom.maximum_threshold_percentage_between_costs"
        )
        products = super().create(vals_list)
        for product in products:
            product.write(
                {
                    "min_threshold_percentage_between_costs_id": min_threshold_percentage_between_costs.id,
                    "max_threshold_percentage_between_costs_id": max_threshold_percentage_between_costs.id,
                }
            )
        return products

    def button_view_product_from_product_editable_tree(self):
        self.ensure_one()
        action = self.env.ref(
            "intecpla_custom.action_product_view_from_product_editable"
        )
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        action_dict["context"]["active_id"] = self.id
        action_dict["context"]["active_ids"] = self.ids
        action_dict["res_id"] = self.id
        domain = expression.AND(
            [[("id", "=", self.id)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def _ir_cron_english_translation_in_product(self):
        cond = [
            ("name", "=", "product.product,name2"),
            ("type", "=", "model"),
            ("value", "=", "*****"),
            ("state", "=", "to_translate"),
            ("lang", "=", "en_US"),
        ]
        translations = self.env[("ir.translation")].search(cond)
        for translation in translations:
            if translation.source and translation.source != "*****":
                translation.write({"value": translation.source, "state": "translated"})

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        args = expression.normalize_domain(args)
        for arg in args:
            if isinstance(arg, (list, tuple)):
                if arg[0] == "default_code":
                    index = args.index(arg)
                    args = (
                        args[:index]
                        + ["|", ("description", arg[1], arg[2])]
                        + args[index:]
                    )
                    break
        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
