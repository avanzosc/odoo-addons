# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    alternative_sales_code = fields.Char(string="Alternative sales code", copy=False)
    default_code = fields.Char(copy=False)

    def button_generate_alternative_sale_code(self):
        sequence = self.env.ref(
            "product_alternative_sale_code.seq_alternative_sale_code", False
        )
        for product in self:
            product.alternative_sales_code = sequence.next_by_id()

    @api.onchange("default_code")
    def onchange_default_code(self):
        if self.barcode != self.default_code:
            self.barcode = self.default_code
            title = _("Warning for product: %s") % self.name
            message = _("You have also changed the barcode.")
            warning = {"title": title, "message": message}
            return {"warning": warning}

    @api.onchange("barcode")
    def onchange_barcode(self):
        if self.default_code != self.barcode:
            self.default_code = self.barcode
            title = _("Warning for product: %s") % self.name
            message = _("You have also changed the internal reference.")
            warning = {"title": title, "message": message}
            return {"warning": warning}

    @api.constrains("default_code", "barcode", "alternative_sales_code")
    def _check_default_code_barcode(self):
        for record in self:
            if record.default_code:
                cond = [
                    ("id", "!=", record.id),
                    "|",
                    ("default_code", "=", record.default_code),
                    "|",
                    ("barcode", "=", record.default_code),
                    ("alternative_sales_code", "=", record.default_code),
                ]
                product = self.search(cond, limit=1)
                if product:
                    raise ValidationError(
                        _("Internal reference used in product: {}").format(product.name)
                    )
            if record.barcode:
                cond = [
                    ("id", "!=", record.id),
                    "|",
                    ("default_code", "=", record.barcode),
                    "|",
                    ("barcode", "=", record.barcode),
                    ("alternative_sales_code", "=", record.barcode),
                ]
                product = self.search(cond, limit=1)
                if product:
                    raise ValidationError(
                        _("Barcode used in product: {}").format(product.name)
                    )
            if record.alternative_sales_code:
                cond = [
                    ("id", "!=", record.id),
                    "|",
                    ("default_code", "=", record.alternative_sales_code),
                    "|",
                    ("barcode", "=", record.alternative_sales_code),
                    ("alternative_sales_code", "=", record.alternative_sales_code),
                ]
                product = self.search(cond, limit=1)
                if product:
                    raise ValidationError(
                        _("Alternative sale code used in product: {}").format(
                            product.name
                        )
                    )

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
                        + ["|", ("alternative_sales_code", arg[1], arg[2])]
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

    @api.model
    def create(self, values):
        product = super().create(values)
        if product.default_code and not product.barcode:
            product.barcode = product.default_code
        elif product.barcode and not product.default_code:
            product.default_code = product.barcode
        return product

    def write(self, values):
        result = super().write(values)
        if "from_my_write" not in self.env.context:
            for product in self:
                if product.default_code and not product.barcode:
                    product.with_context(from_my_write=True).barcode = (
                        product.default_code
                    )
                if product.barcode and not product.default_code:
                    product.with_context(from_my_write=True).default_code = (
                        product.barcode
                    )
                if product.default_code != product.barcode:
                    product.with_context(from_my_write=True).barcode = (
                        product.default_code
                    )
        return result
