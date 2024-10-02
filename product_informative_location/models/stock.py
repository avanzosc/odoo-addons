# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    has_zone = fields.Boolean(string="Has zone", default=False)


class StockMove(models.Model):
    _inherit = "stock.move"

    informative_location = fields.Text(string="Informative locations")
    informative_location_description = fields.Text(
        string="Informative locations descriptions"
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id and self.picking_id.picking_type_id:
            mytext, mydescript = self._catch_informative_location()
            self.informative_location = mytext
            self.informative_location_description = mydescript

    def _catch_informative_location(self):
        lines = self.env["product.informative.location"]
        lines2 = self.env["product.informative.location"]
        my_text = ""
        my_description = ""
        code = (
            self.picking_id.picking_type_id.code
            if self.picking_id
            else self.picking_type_id.code
        )
        location_id = (
            self.picking_id.location_id if self.picking_id else self.location_id
        )
        location_dest_id = (
            self.picking_id.location_dest_id
            if self.picking_id
            else self.location_dest_id
        )
        if code in ("outgoing", "internal"):
            lines += self.product_id.mapped("product_location_ids").filtered(
                lambda x: x.location_id == location_id
            )
            if lines:
                lines = lines.sorted("sequence")
                for line in lines:
                    my_text = (
                        line.name
                        if not my_text
                        else "{}\n{}".format(my_text, line.name)
                    )
                    my_description = (
                        line.description
                        if not my_description
                        else "{}\n{}".format(my_description, line.description)
                    )
        if code in ("incoming", "internal"):
            lines2 = self.product_id.mapped("product_location_ids").filtered(
                lambda x: x.location_id == location_dest_id
            )
            if lines2:
                if my_text:
                    my_text = "{}\n---------->".format(my_text)
                    my_description = "{}\n---------->".format(my_description)
                lines2 = lines2.sorted("sequence")
                for line in lines2:
                    my_text = (
                        line.name
                        if not my_text
                        else "{}\n{}".format(my_text, line.name)
                    )
                    my_description = (
                        line.description
                        if not my_description
                        else "{}\n{}".format(my_description, line.description)
                    )
        if not lines and not lines2:
            my_text = "---------->"
            my_description = "---------->"
        elif line and not lines2:
            my_text = "{}\n---------->".format(my_text)
            my_description = "{}\n---------->".format(my_description)
        else:
            if not line and lines2:
                my_text = "---------->\n{}".format(my_text)
                my_description = "---------->\n{}".format(my_description)
        return my_text, my_description

    @api.model
    def create(self, values):
        move = super().create(values)
        if not move.informative_location:
            mytext, mydesc = move._catch_informative_location()
            if mytext or mydesc:
                move.write(
                    {
                        "informative_location": mytext,
                        "informative_location_description": mydesc,
                    }
                )
        return move

    def write(self, vals):
        result = super().write(vals)
        if (
            "informative_location" not in self.env.context
            and "informative_location" not in vals
            and (
                "product_id" in vals
                or "picking_type_id" in vals
                or "location_id" in vals
                or "location_dest_id" in vals
            )
        ):
            for move in self:
                mytext, mydesc = move._catch_informative_location()
                if (
                    mytext != move.informative_location
                    or mydesc != move.informative_location_description
                ):
                    move.with_context(informative_location=True).write(
                        {
                            "informative_location": mytext,
                            "informative_location_description": mydesc,
                        }
                    )
        return result


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    informative_location = fields.Text(
        string="Informative locations", compute="_compute_informative_locations"
    )

    def _compute_informative_locations(self):
        for inventory_line in self:
            if inventory_line.product_id and inventory_line.location_id:
                my_text = ""
                lines = inventory_line.product_id.mapped(
                    "product_location_ids"
                ).filtered(lambda x: x.location_id == inventory_line.location_id)
                if lines:
                    lines = lines.sorted("sequence")
                    for line in lines:
                        if not my_text:
                            my_text = "{}     {}".format(line.name, line.description)
                        else:
                            my_text = "{}\n{}     {}".format(
                                my_text, line.name, line.description
                            )
                inventory_line.informative_location = my_text
