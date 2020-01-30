# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

    qty_pending_delivery = fields.Float(
        string='Pending delivery qty', readonly=True)
    qty_pending_invoicing = fields.Float(
        string='Pending invoicing qty', readonly=True)
    amount_pending_delivery = fields.Float(
        string='Amount pending delivery', readonly=True)
    amount_pending_invoicing = fields.Float(
        string='Amount pending invoicing', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
            sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
            sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
            sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
            sum(l.qty_pending_delivery / u.factor * u2.factor) as
            qty_pending_delivery,
            sum(l.qty_pending_invoicing / u.factor * u2.factor) as
            qty_pending_invoicing,
            sum(l.price_total / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_total,
            sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_subtotal,
            sum(l.amount_pending_delivery / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END)
            as amount_pending_delivery,
            sum(l.amount_pending_invoicing / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END)
            as amount_pending_invoicing,
            sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END) as
            untaxed_amount_to_invoice,
            sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0)
            WHEN 0 THEN 1.0 ELSE s.currency_rate END) as
            untaxed_amount_invoiced,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.confirmation_date as confirmation_date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            extract(epoch from avg(date_trunc('day',s.date_order)-
            date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2)
            as delay,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.commercial_partner_id as commercial_partner_id,
            sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
            sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
            l.discount as discount,
            sum((l.price_unit * l.discount / 100.0 /
            CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE
            s.currency_rate END)) as discount_amount,
            s.id as order_id
        """
        for field in fields.values():
            select_ += field
        from_ = """
                sale_order_line l
                      join sale_order s on (l.order_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                       left join product_product p on (l.product_id=p.id)
                       left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                %s
        """ % from_clause
        groupby_ = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.confirmation_date,
            s.partner_id,
            s.user_id,
            s.state,
            s.company_id,
            s.pricelist_id,
            s.analytic_account_id,
            s.team_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.commercial_partner_id,
            l.discount,
            s.id %s
        """ % (groupby)
        return (
            '%s (SELECT %s FROM %s WHERE l.product_id IS NOT NULL GROUP BY %s)'
            % (with_, select_, from_, groupby_))
