from odoo import api, fields, models


class AccountMoveLineComparison(models.Model):
    _name = "account.move.line.comparison"
    _description = "Account Move Line Comparison"

    external_id = fields.Integer(string="External ID")
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    move_line_id = fields.Many2one(
        "account.move.line",
        string="Account Move Line",
        compute="_compute_move_line",
        store=True,
    )
    move_id = fields.Many2one(
        "account.move",
        string="Account Move",
        related="move_line_id.move_id",
        store=True,
    )
    debit_now = fields.Float(
        string="Debit Now", compute="_compute_debit_now", store=True
    )
    credit_now = fields.Float(
        string="Credit Now", compute="_compute_credit_now", store=True
    )
    amount_currency = fields.Float(
        string="Amount in Currency", compute="_compute_amount_currency", store=True
    )
    amount_currency_now = fields.Float(
        string="Amount in Currency Now",
        compute="_compute_amount_currency_now",
        store=True,
    )
    is_debit_different = fields.Boolean(
        string="Is Debit Different", compute="_compute_is_debit_different", store=True
    )
    is_credit_different = fields.Boolean(
        string="Is Credit Different", compute="_compute_is_credit_different", store=True
    )
    is_amount_currency_different = fields.Boolean(
        string="Is Amount Currency Different",
        compute="_compute_is_amount_currency_different",
        store=True,
    )

    @api.depends("external_id")
    def _compute_move_line(self):
        for rec in self:
            rec.move_line_id = self.env["account.move.line"].search(
                [("id", "=", rec.external_id)], limit=1
            )

    @api.depends("move_line_id")
    def _compute_debit_now(self):
        for rec in self:
            rec.debit_now = rec.move_line_id.debit

    @api.depends("move_line_id")
    def _compute_credit_now(self):
        for rec in self:
            rec.credit_now = rec.move_line_id.credit

    @api.depends("move_line_id")
    def _compute_amount_currency(self):
        for rec in self:
            rec.amount_currency = rec.move_line_id.amount_currency

    @api.depends("move_line_id")
    def _compute_amount_currency_now(self):
        for rec in self:
            rec.amount_currency_now = rec.move_line_id.amount_currency

    @api.depends("debit", "debit_now")
    def _compute_is_debit_different(self):
        for rec in self:
            rec.is_debit_different = rec.debit != rec.debit_now

    @api.depends("credit", "credit_now")
    def _compute_is_credit_different(self):
        for rec in self:
            rec.is_credit_different = rec.credit != rec.credit_now

    @api.depends("amount_currency", "amount_currency_now")
    def _compute_is_amount_currency_different(self):
        for rec in self:
            rec.is_amount_currency_different = (
                rec.amount_currency != rec.amount_currency_now
            )

    def copy_debit_credit_to_now(self):
        for rec in self:
            if rec.is_debit_different:
                rec.debit_now = rec.debit
            if rec.is_credit_different:
                rec.credit_now = rec.credit
            if rec.is_amount_currency_different:
                rec.amount_currency_now = rec.amount_currency

    def copy_all_debit_credit_to_now(self):
        for rec in self.env["account.move.line.comparison"].search([]):
            if rec.is_debit_different:
                rec.debit_now = rec.debit
            if rec.is_credit_different:
                rec.credit_now = rec.credit
            if rec.is_amount_currency_different:
                rec.amount_currency_now = rec.amount_currency
