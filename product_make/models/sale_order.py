# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    makes_in_orders = fields.Char(
        string="Makes", compute="_compute_makes_in_orders", store=True, copy=True
    )
    commercial_make_id = fields.Many2one(
        string="Commercial Make", comodel_name="product.make", copy=True
    )
    allowed_commercial_make_ids = fields.Many2many(
        string="Allowed Commercial Makes", comodel_name="product.make", copy=True
    )
    num_allowed_commercial_make = fields.Integer(
        string="Num Allowed Commercial Makes", copy=True
    )
    relation_id = fields.Many2one(
        string="Relation",
        comodel_name="res.partner.relation",
        related="partner_id.relation_id",
        store=True,
    )
    classification_id = fields.Many2one(
        string="Input channel",
        comodel_name="res.partner.classification",
        related="partner_id.classification_id",
        store=True,
    )
    market_id = fields.Many2one(
        string="Sale channel",
        comodel_name="res.partner.market",
        related="partner_id.market_id",
        compute_sudo=True,
        store=True,
        compute=False,
        copy=False,
    )
    market_sector_id = fields.Many2one(
        string="Market niche",
        comodel_name="res.partner.market.sector",
        related="partner_id.market_sector_id",
        store=True,
    )
    team_id = fields.Many2one(default=False)

    @api.depends("order_line", "order_line.make_id", "order_line.make_id.name")
    def _compute_makes_in_orders(self):
        for sale in self:
            makes = ""
            for line in sale.order_line.filtered(lambda x: x.make_id):
                if line.make_id.name not in makes:
                    if not makes:
                        makes = line.make_id.name
                    else:
                        makes = f"{makes}, {line.make_id.name}"
            sale.makes_in_orders = makes

    def action_makes_in_lines(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: not x.make_id)
            for line in lines:
                line.put_makes_in_line()

    def write(self, vals):
        if len(vals) != 1 or len(vals) == 1 and "order_line" not in vals:
            recompute_delivery = True
        if len(vals) == 1 and "order_line" in vals and vals.get("order_line", False):
            recompute_delivery = self._recompute_delivery(vals)
        if len(vals) == 1 and "team_id" in vals and vals.get("team_id", False):
            recompute_delivery = False
        res = super(
            SaleOrder, self.with_context(recompute_delivery=recompute_delivery)
        ).write(vals)
        return res

    def _recompute_delivery(self, vals):
        recompute_delivery = False
        order_line = vals.get("order_line", [])
        for line in order_line:
            if len(line) != 3:
                recompute_delivery = True
                break
            operation_type, _, data = line
            if operation_type not in (1, 4):
                recompute_delivery = True
                break
            if operation_type == 1:
                if (
                    not isinstance(data, dict)
                    or len(data) != 1
                    or "make_id" not in data
                ):
                    recompute_delivery = True
                    break
        return recompute_delivery

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if not self.partner_id:
            return result
        info = self.partner_id.get_partner_makes_info()
        self.commercial_make_id = info.get("commercial_make_id")
        self.allowed_commercial_make_ids = info.get("allowed_commercial_make_ids")
        self.num_allowed_commercial_make = info.get("num_allowed_commercial_make")
        return result

    def action_put_commercial_make_in_sales(self):
        for sale in self:
            make = sale._find_unique_make()
            if make:
                partner_make = sale._find_commercial_make_in_partner(make)
                if partner_make:
                    sale._treat_pickings_commercial_make(make)
                    sale._treat_invoices_commercial_make(make)

    def _find_unique_make(self):
        lines_with_make = self.order_line.filtered(
            lambda x: x.make_id and x.display_type not in ("line_section", "line_note")
        )
        if not lines_with_make:
            return False
        make = lines_with_make[0].make_id
        if all(line.make_id == make for line in lines_with_make):
            if len(lines_with_make) == len(
                self.order_line.filtered(
                    lambda x: x.display_type not in ("line_section", "line_note")
                )
            ):
                return make
        return False

    def _find_commercial_make_in_partner(self, make):
        if self.partner_id.make_saleperson_ids:
            partner_makes = self.env["product.make"]
            for make_saleperson in self.partner_id.make_saleperson_ids:
                partner_makes += make_saleperson.make_id
            if make in partner_makes:
                self.write(
                    {
                        "commercial_make_id": make.id,
                        "num_allowed_commercial_make": len(partner_makes),
                        "allowed_commercial_make_ids": [(6, 0, partner_makes.ids)],
                    }
                )
                self.order_line.write({"allowed_make_ids": make.ids})
                return make
        return False

    def _treat_pickings_commercial_make(self, make):
        for picking in self.picking_ids:
            num_lines = len(picking.move_ids_without_package)
            num_lines_with_make = 0
            picking_make = self.env["product.make"]
            lines_with_make = picking.move_ids_without_package.filtered(
                lambda z: z.make_id
            )
            for line_with_make in lines_with_make:
                if line_with_make.make_id == make:
                    if not picking_make:
                        picking_make = line_with_make.make_id
                        num_lines_with_make += 1
                    else:
                        if picking_make == line_with_make.make_id:
                            num_lines_with_make += 1
            if num_lines == num_lines_with_make:
                picking.write(
                    {
                        "commercial_make_id": self.commercial_make_id.id,
                        "num_allowed_commercial_make": self.num_allowed_commercial_make,
                        "allowed_commercial_make_ids": [
                            (6, 0, self.allowed_commercial_make_ids.ids)
                        ],
                    }
                )
                picking.move_ids_without_package.write({"allowed_make_ids": make.ids})

    def _treat_invoices_commercial_make(self, make):
        for invoice in self.invoice_ids:
            num_lines = len(
                invoice.invoice_line_ids.filtered(
                    lambda x: x.display_type not in ("line_section", "line_note")
                )
            )
            num_lines_with_make = 0
            picking_make = self.env["product.make"]
            lines_with_make = invoice.invoice_line_ids.filtered(
                lambda z: z.make_id
                and z.display_type not in ("line_section", "line_note")
            )
            for line_with_make in lines_with_make:
                if line_with_make.make_id == make:
                    if not picking_make:
                        picking_make = line_with_make.make_id
                        num_lines_with_make += 1
                    else:
                        if picking_make == line_with_make.make_id:
                            num_lines_with_make += 1
            if num_lines == num_lines_with_make:
                invoice.write(
                    {
                        "commercial_make_id": self.commercial_make_id.id,
                        "num_allowed_commercial_make": self.num_allowed_commercial_make,
                        "allowed_commercial_make_ids": [
                            (6, 0, self.allowed_commercial_make_ids.ids)
                        ],
                    }
                )
                invoice.invoice_line_ids.write({"allowed_make_ids": make.ids})

    def _prepare_invoice(self):
        self.ensure_one()
        vals = super()._prepare_invoice()
        if self.commercial_make_id:
            vals["commercial_make_id"] = self.commercial_make_id.id
        if self.num_allowed_commercial_make:
            vals["num_allowed_commercial_make"] = self.num_allowed_commercial_make
        if self.allowed_commercial_make_ids:
            vals["allowed_commercial_make_ids"] = [
                (6, 0, self.allowed_commercial_make_ids.ids)
            ]
        return vals

    def update_division_in_sales(self):
        for sale in self:
            make = sale.order_line.mapped("make_id") if sale.order_line else False
            invalid_lines = sale.order_line.filtered(
                lambda x: not x.make_id
                and x.display_type not in ("line_section", "line_note")
            )
            if invalid_lines:
                raise ValidationError(_("Check sales lines, some do not have a brand."))

            team = False
            if sale.market_id and len(make) == 1:
                team = self.env["crm.team"].search(
                    [
                        ("market_id", "=", sale.market_id.id),
                        ("product_make_id", "=", make.id),
                    ],
                    limit=1,
                )
            team_id = team.id if team else False
            if sale.team_id != team:
                sale.team_id = team_id
            sale.picking_ids.write({"team_id": team_id})
            sale.invoice_ids.write({"team_id": team_id})

    def action_open_delivery_wizard(self):
        result = super().action_open_delivery_wizard()
        result["context"]["default_make_id"] = self.commercial_make_id.id
        result["context"]["default_carrier_id"] = False
        return result
