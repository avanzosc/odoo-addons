# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, exceptions, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("move_id", "move_id.commercial_make_id")
    def _compute_make_id(self):
        for line in self.filtered(
            lambda x: x.move_id and x.move_id.move_type in ("out_invoice", "out_refund")
        ):
            line.make_ids = [(5, 0, 0)]
            if line.move_id.commercial_make_id:
                line.make_ids = [(6, 0, line.move_id.commercial_make_id.ids)]
                line.make_literal = line.move_id.commercial_make_id.name
            else:
                price_subtotal = (
                    line.credit
                    if line.move_id.move_type == "out_invoice"
                    else line.debit
                )
                invoice_lines = line.move_id.invoice_line_ids.filtered(
                    lambda x, current_line=line, subtotal=price_subtotal: (
                        x.product_id == current_line.product_id
                        and x.price_subtotal == subtotal
                    )
                )
                invoice_line = False
                for invline in invoice_lines:
                    invoice_line_with_makes = invline.filtered(lambda x: x.make_id)
                    if len(invoice_lines) == len(invoice_line_with_makes):
                        make = invoice_line_with_makes[0].make_id
                        equals = 0
                        for il in invoice_line_with_makes:
                            if il.make_id == make:
                                equals += 1
                        if equals == len(invoice_line_with_makes):
                            invoice_line = invoice_line_with_makes[0]
                make_literal = ""
                make_ids = [(6, 0, [])]
                if invoice_line and len(invoice_line) == 1 and invoice_line.make_id:
                    make_literal = invoice_line.make_id.name
                    make_ids = [(6, 0, [invoice_line.make_id.id])]
                line.make_literal = make_literal
                line.make_ids = make_ids

    make_ids = fields.Many2many(
        string="Makes",
        comodel_name="product.make",
        store=True,
        compute="_compute_make_id",
        relation="rel_account_move_line_make",
        column1="account_move_line_id",
        column2="make_id",
    )
    journal_type = fields.Selection(
        string="Journal type", related="journal_id.type", store=True
    )
    make_literal = fields.Char(string="Make", compute="_compute_make_id", store=True)
    invoice_state = fields.Selection(
        string="Status", related="move_id.state", store=True
    )
    invoice_type = fields.Selection(
        string="Invoice type", related="move_id.move_type", store=True
    )
    make_id = fields.Many2one(string="Make", comodel_name="product.make")
    allowed_make_ids = fields.Many2many(
        string="Allowed makes", comodel_name="product.make"
    )
    team_id = fields.Many2one(string="Division", comodel_name="crm.team", copy=False)

    @api.onchange("product_id")
    def _onchange_product_id_put_makes_in_lines(self):
        self.put_makes_in_line()

    def put_makes_in_line(self):
        commercial_make = False
        if "commercial_make_id" in self.env.context:
            if not self.env.context.get("commercial_make_id", False):
                raise exceptions.ValidationError(
                    _(" You must select a commercial make on the invoice.")
                )
            commercial_make = self.env["product.make"].browse(
                self.env.context.get("commercial_make_id")
            )
        else:
            if self.move_id.commercial_make_id:
                commercial_make = self.move_id.commercial_make_id
        if self.move_id.move_type not in ("out_invoice", "out_refund"):
            self.move_id.commercial_make_id = False
            self.move_id.num_allowed_commercial_make = 0
            self.move_id.allowed_commercial_make_ids = [(6, 0, [])]
            return
        if commercial_make and self.product_id:
            found = False
            for product_make in self.product_id.product_tmpl_id.product_make_ids:
                if commercial_make == product_make:
                    self.allowed_make_ids = [(6, 0, product_make.ids)]
                    self.make_id = product_make.id
                    found = True
            if not found:
                raise exceptions.ValidationError(
                    _("The product : %(product)s, does not have the make: %(make)s.")
                    % {"product": self.product_id.name, "make": commercial_make.name}
                )

    @api.model_create_multi
    def create(self, values):
        lines = super().create(values)
        for line in lines.filtered(
            lambda x: x.move_id and x.move_id.move_type in ("out_invoice", "out_refund")
        ):
            line.team_id = line.move_id.team_id.id if line.move_id.team_id else False
        for line in lines.filtered(
            lambda x: not x.make_id and x.display_type == "product"
        ):
            line.put_makes_in_line()
            line.move_id.update_division_in_invoices()
        return lines
