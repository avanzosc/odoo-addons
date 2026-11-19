# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        compute="_compute_attachment_ids",
        string="Attachments",
        store=False,
        readonly=False,
    )

    def _compute_attachment_ids(self):
        ir_attachment = self.env["ir.attachment"]
        for product in self:
            domain = [
                ("res_model", "=", "product.product"),
                ("res_id", "=", product.id),
            ]
            product.attachment_ids = ir_attachment.search(domain)

    def write(self, values):
        result = super().write(values)
        if "attachment_ids" in values:
            self._actualize_product_attachments(values)
        return result

    def _actualize_product_attachments(self, values):
        attachments = values.get("attachment_ids")
        for attachment in attachments:
            if (
                len(attachment) == 3
                and isinstance(attachment[0], int)
                and attachment[0] == 2
                and isinstance(attachment[1], int)
                and isinstance(attachment[2], bool)
                and not attachment[2]
            ):
                self._delete_attachment_from_product(attachment[1])
            if (
                len(attachment) == 3
                and isinstance(attachment[0], int)
                and attachment[0] == 0
                and isinstance(attachment[1], str)
                and isinstance(attachment[2], dict)
            ):
                self._create_attachment_from_product(attachment[2])

    def _delete_attachment_from_product(self, attachment_id):
        attachment = self.env["ir.attachment"].browse(attachment_id)
        if attachment:
            attachment.unlink()

    def _create_attachment_from_product(self, values):
        values.update({"res_model": "product.product", "res_id": self.id})
        self.env["ir.attachment"].create(values)
