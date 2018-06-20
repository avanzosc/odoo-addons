# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields, tools


class ReportSalePurchaseMTO(models.Model):

    _name = 'report.sale.purchase.mto'
    _auto = False

    @api.model
    def _get_selection_sale_state(self):
        return self.env['sale.order'].fields_get(
            allfields=['state'])['state']['selection']

    @api.model
    def _get_selection_purchase_state(self):
        return self.env['purchase.order'].fields_get(
            allfields=['state'])['state']['selection']

    sale_move_id = fields.Many2one(comodel_name='stock.move',
                                   string='Sale Move')
    sale_line_id = fields.Many2one(comodel_name='sale.order.line',
                                   string='Sale Line')
    sale_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    sale_picking_id = fields.Many2one(comodel_name='stock.picking',
                                      string='Sale Picking')
    sale_state = fields.Selection(selection='_get_selection_sale_state',
                                  string='Sale State')
    purchase_move_id = fields.Many2one(comodel_name='stock.move',
                                       string='Purchase Move')
    purchase_line_id = fields.Many2one(comodel_name='purchase.order.line',
                                       string='Purchase Line')
    purchase_id = fields.Many2one(comodel_name='purchase.order',
                                  string='Purchase Order')
    purchase_picking_id = fields.Many2one(comodel_name='stock.picking',
                                          string='Purchase Picking')
    sale_date = fields.Date(string='Sale Confirm Date')
    sale_requested_date = fields.Date(string='Sale Requested Date')
    sale_commitment_date = fields.Date(string='Sale Commitment Date')
    sale_effective_date = fields.Date(string='Sale Effective Date')
    sale_user_id = fields.Many2one(comodel_name='res.users',
                                   string='Sale Staff')
    sale_partner_id = fields.Many2one(comodel_name='res.partner',
                                      string='Customer')
    purchase_date = fields.Date(string='Purchase Date')
    purchase_minimum_planned_date = fields.Date(
        string='Purchase Expected Date')
    purchase_state = fields.Selection(
        selection='_get_selection_purchase_state', string='Purchase State')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    purchase_partner_id = fields.Many2one(comodel_name='res.partner',
                                          string='Supplier')
    qty = fields.Float(string='Quantity')
    purchase_reception_date = fields.Date(
        string='Purchase Line Scheduled Date')
    purchase_incoterm_id = fields.Many2one(comodel_name='stock.incoterms',
                                           string='Purchase Incoterm')
    sale_incoterm_id = fields.Many2one(comodel_name='stock.incoterms',
                                       string='Sale Incoterm')
    shipment_date = fields.Date(string='Shipment Date')
    shipment_min_date = fields.Date(string='Shipment Scheduled Date')
    shipment_max_date = fields.Date(string='Shipment Max. Expected Date')
    reception_date = fields.Date(string='Reception Date')
    reception_min_date = fields.Date(string='Reception Scheduled Date')
    reception_max_date = fields.Date(string='Reception Max. Expected Date')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sale_purchase_mto')
        cr.execute("""
            create or replace view report_sale_purchase_mto as (
            select
                (proc.id::text || (case when psm.id is not null then
                lpad(psm.id::text, 8, '0') else '00000000' end))::bigint as id,
                sm.id as sale_move_id,
                sol.id as sale_line_id,
                sol.order_id as sale_id,
                so.state as sale_state,
                sm.picking_id as sale_picking_id,
                psm.id as purchase_move_id,
                pol.id as purchase_line_id,
                pol.order_id as purchase_id,
                psm.picking_id as purchase_picking_id,
                so.date_order as sale_date,
                so.requested_date as sale_requested_date,
                so.commitment_date as sale_commitment_date,
                so.effective_date as sale_effective_date,
                so.user_id as sale_user_id,
                so.partner_id as sale_partner_id,
                po.date_order as purchase_date,
                po.minimum_planned_date as purchase_minimum_planned_date,
                po.state as purchase_state,
                sm.product_id as product_id,
                po.partner_id as purchase_partner_id,
                sm.product_uom_qty as qty,
                po.incoterm_id as purchase_incoterm_id,
                so.incoterm as sale_incoterm_id,
                pol.date_planned as purchase_reception_date,
                psp.date_done as reception_date,
                psp.min_date as reception_min_date,
                psp.max_date as reception_max_date,
                ssp.date_done as shipment_date,
                ssp.min_date as shipment_min_date,
                ssp.max_date as shipment_max_date
            from
                sale_order_line sol left join sale_order so on
                so.id=sol.order_id left join procurement_order sproc on
                sproc.sale_line_id=sol.id
                left join stock_move sm on sm.procurement_id=sproc.id
                left join stock_picking ssp on ssp.id=sm.picking_id
                left join procurement_order proc on proc.move_dest_id = sm.id
                left join purchase_order_line pol on
                pol.id=proc.purchase_line_id
                left join purchase_order po on po.id = pol.order_id
                left join stock_move psm on psm.purchase_line_id = pol.id
                left join stock_picking psp on psp.id=psm.picking_id
            where
                ((psm.id is not null and psm.move_dest_id is not null) or
                 psm.id is null) and
                proc.purchase_line_id is not null and
                so.state not in ('cancel', 'done')
            ) """)
