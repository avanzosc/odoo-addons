from odoo import fields, models
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        tracking=2,
        default=lambda self: self.env.user,
        domain=lambda self: [
            "|",
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id),
            ("groups_id", "in", self.env.ref("base.group_portal").id),
        ],
    )

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        values = super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        for record in self:
            sale_person = request.session.get("sale_person_id")
            if sale_person:
                person = (
                    self.env["res.users"]
                    .sudo()
                    .search([("id", "=", int(sale_person or 0))])
                )
                if person and record.user_id and record.user_id.id != person.id:
                    record.write({"user_id": person.id})

                if person and not record.user_id:
                    record.write({"user_id": person.id})
        return values
