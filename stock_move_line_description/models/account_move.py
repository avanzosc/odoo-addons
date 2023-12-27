from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("sale_line_ids")
    def compute_account_move_line_description(self):
        for record in self:
            str_name = "" if record.sale_line_ids else record.name
            for line in record.sale_line_ids:
                if len(record.sale_line_ids) > 1:
                    str_name += " - "
                str_name += line.name
            record.name = str_name

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.sale_line_ids:
            res.compute_account_move_line_description()
        return res
