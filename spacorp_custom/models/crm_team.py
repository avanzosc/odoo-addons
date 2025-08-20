# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    market_id = fields.Many2one(
        string="Sale channel",
        comodel_name="res.partner.market",
        copy=False,
    )
    product_make_id = fields.Many2one(
        string="Make",
        comodel_name="product.make",
        copy=False,
    )

    def load_division_in_sales(self):
        cond = []
        teams = self.env["crm.team"].search(cond)
        for team in teams.filtered(lambda x: x.market_id and x.product_make_id):
            my_sales = self.env["sale.order"]
            cond = [("market_id", "=", team.market_id.id)]
            sales = self.env["sale.order"].search(cond)
            for sale in sales:
                if sale.order_line:
                    make = sale.order_line.mapped("make_id")
                    if make and len(make) == 1 and make == team.product_make_id:
                        if sale.team_id != team:
                            my_sales += sale
            for sale in my_sales:
                sale.with_context(no_repeat_update_division=True).team_id = team.id
                self._cr.commit()
            pickings = self.env["stock.picking"].search(cond)
            for picking in pickings:
                picking.update_division_in_pickings()
                self._cr.commit()
            invoices = self.env["account.invoice"].search(cond)
            for invoice in invoices:
                invoice.update_division_in_invoices()
                self._cr.commit()
