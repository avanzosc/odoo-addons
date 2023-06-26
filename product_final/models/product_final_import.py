# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductFinalImport(models.Model):
    _name = "product.final.import"
    _inherit = "base.import"
    _description = "Wizard to import final products"

    import_line_ids = fields.One2many(
        comodel_name="product.final.import.line",
    )
    product_count = fields.Integer(
        string="# Products",
        compute="_compute_product_count",
    )
    product_final_count = fields.Integer(
        string="# Product Final",
        compute="_compute_product_final_count",
    )
    location_count = fields.Integer(
        string="# Locations",
        compute="_compute_location_count",
    )

    def _get_line_values(self, row_values=None):
        self.ensure_one()
        if row_values is None:  # 👍
            row_values = []
        values = super()._get_line_values(row_values=row_values)
        product_code = row_values.get("Ref", "")
        product_final_code = row_values.get("CPF", "")
        position = row_values.get("Pos", "")
        comments = row_values.get("Comments", "")
        log_info = ""
        values.update(
            {
                "product_default_code": product_code,
                "product_final_code": product_final_code,
                "position": position,
                "comments": comments,
                "log_info": log_info,
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

    def _compute_product_final_count(self):
        for record in self:
            record.product_final_count = len(
                record.mapped("import_line_ids.product_final_id"))

    def button_open_product_final(self):
        self.ensure_one()
        product_final = self.mapped("import_line_ids.product_final_id")
        action = self.env.ref("product_final.action_product_final")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", product_final.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def _compute_location_count(self):
        for record in self:
            record.location_count = len(
                record.mapped("import_line_ids.product_location_exploded_id"))

    def button_open_location(self):
        self.ensure_one()
        locations = self.mapped("import_line_ids.product_location_exploded_id")
        action = self.env.ref("product_final.action_product_location_exploded")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", locations.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ProductFinalImportLine(models.Model):
    _name = "product.final.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import final products"

    import_id = fields.Many2one(
        comodel_name="product.final.import",
    )
    action = fields.Selection(
        string="Action",
        selection=[
            ("create", "Create"),
            ("update", "Update"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    product_final_code = fields.Char(string="Final Product Code")
    # product_final_name = fields.Char(string="CPF Description")
    product_final_id = fields.Many2one(
        comodel_name="product.final",
        string="Final Product",
    )
    position = fields.Char(string="Position")
    product_default_code = fields.Char(string="Internal Reference")
    # product_name = fields.Char(string="Product Name")
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    product_location_exploded_id = fields.Many2one(
        comodel_name="product.location.exploded",
        string="Products Exploded Location",
    )
    comments = fields.Text(string="Comments")
    change_comments = fields.Boolean(
        string="Comment Modified",
        compute="_compute_change_comments",
    )

    @api.depends("comments", "product_location_exploded_id",
                 "product_location_exploded_id.comments")
    def _compute_change_comments(self):
        for record in self:
            different_comment = False
            if (record.product_location_exploded_id and
                    record.product_location_exploded_id.comments != record.comments):
                different_comment = True
            record.change_comments = different_comment

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_infos = []
            log_message = ""
            product, log_info = line._check_product()
            if log_info:
                log_infos.append(log_info)
            product_final, log_info = line._check_product_final()
            if log_info:
                log_infos.append(log_info)
            exploded_location, log_info = line._check_exploded_location()
            if log_info:
                log_infos.append(log_info)
            state = "error" if len(log_infos) else "pass"
            if log_infos:
                log_message = _("Error: {}").format(", ".join(log_infos))
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_id": product and product.id,
                        "product_final_id": product_final and product_final.id,
                        "product_location_exploded_id": (
                            exploded_location and exploded_location.id
                        ),
                        "log_info": log_message,
                        "state": state,
                    },
                )
            )
        return line_values

    def action_process(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            exploded_location, log_info = line._create_exploded_location()
            state = "error" if log_info else "done"
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "product_location_exploded_id": (
                            exploded_location and exploded_location.id
                        ),
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_product(self):
        self.ensure_one()
        product_obj = self.env["product.product"]
        search_domain = [("default_code", "=", self.product_default_code)]
        log_info = ""
        products = product_obj.search(search_domain)
        if not products:
            log_info = _("Product with code {} does not exist").format(
                self.product_default_code
            )
        elif len(products) > 1:
            log_info = _("More than one product found for code {}").format(
                self.product_default_code
            )
            products = product_obj
        return products[:1], log_info

    def _check_product_final(self):
        self.ensure_one()
        product_final_obj = self.env["product.final"]
        search_domain = [("code", "=", self.product_final_code)]
        log_info = ""
        product_finals = product_final_obj.search(search_domain)
        if not product_finals:
            log_info = _("Final product with code {} does not exist").format(
                self.product_final_code
            )
        return product_finals[:1], log_info

    def _check_exploded_location(self):
        self.ensure_one()
        log_info = ""
        exploded_location_obj = self.env["product.location.exploded"]
        search_domain = [
            ("product_id", "=", self.product_id.id),
            ("product_final_id", "=", self.product_final_id.id),
            ("position", "=", self.position),
        ]
        exploded_locations = exploded_location_obj.search(search_domain)
        # if exploded_locations:
        #     log_info = _("Error: Unit of measure not found")
        return exploded_locations[:1], log_info

    def _create_exploded_location(self):
        self.ensure_one()
        exploded_location, log_info = self._check_exploded_location()
        if not exploded_location and not log_info:
            exploded_location_obj = self.env["product.location.exploded"]
            exploded_location = exploded_location_obj.create(
                {
                    "product_id": self.product_id.id,
                    "product_final_id": self.product_final_id.id,
                    "position": self.position,
                    "comments": self.comments,
                }
            )
            log_info = ""
        return exploded_location, log_info

    def button_open_location(self):
        self.ensure_one()
        action = self.env.ref("product_final.action_product_location_exploded")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "=", self.product_location_exploded_id.id)],
             safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict
