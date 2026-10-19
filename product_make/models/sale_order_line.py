# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    make_id = fields.Many2one(string="Make", comodel_name="product.make", copy=True)
    allowed_make_ids = fields.Many2many(
        string="Allowed makes", comodel_name="product.make", copy=True
    )
    team_id = fields.Many2one(
        string="Division",
        comodel_name="crm.team",
        copy=True,
    )

    def catch_product_makes(self):
        self.product_id_change()

    @api.onchange("product_id")
    def product_id_change_put_makes(self):
        if self.product_id:
            self.put_makes_in_line()

    def put_makes_in_line(self):
        commercial_make_id = self.env.context.get("commercial_make_id")
        if commercial_make_id is not None:
            if not commercial_make_id:
                raise exceptions.ValidationError(
                    _("You must select a commercial make on the sales order.")
                )
            commercial_make = self.env["product.make"].browse(commercial_make_id)
        elif self.order_id.commercial_make_id:
            commercial_make = self.order_id.commercial_make_id
        else:
            commercial_make = False
        if commercial_make:
            matching_make = next(
                (
                    make
                    for make in self.product_id.product_tmpl_id.product_make_ids
                    if make == commercial_make
                ),
                None,
            )
            if matching_make:
                self.allowed_make_ids = [(6, 0, [matching_make.id])]
                self.make_id = matching_make.id
            else:
                raise exceptions.ValidationError(
                    _("The product: %(product)s, does not have the make: %(make)s.")
                    % {"product": self.product_id.name, "make": commercial_make.name}
                )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines.filtered(
            lambda x: not x.make_id
            and x.display_type not in ("line_section", "line_note")
        ):
            line.put_makes_in_line()
            line.order_id.update_division_in_sales()
        return lines
