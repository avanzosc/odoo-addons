# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderCreateEventWithHour(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderCreateEventWithHour, self).setUp()
        self.move_line_model = self.env['account.move.line']
        self.task_model = self.env['project.task']
        self.sale_model = self.env['sale.order']
        self.procurement_model = self.env['procurement.order']
        self.event_model = self.env['event.event']
        self.registration_model = self.env['event.registration']
        self.wiz_append_model = self.env['wiz.event.append.assistant']
        self.wiz_delete_model = self.env['wiz.event.delete.assistant']
        account_vals = {'name': 'account procurement service project',
                        'date_start': '2016-02-01',
                        'date': '2016-02-28',
                        'start_time': 5.0,
                        'end_time': 10.0}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
        project_vals = {'name': 'project procurement service project',
                        'analytic_account_id': self.account.id,
                        'partners': [(6, 0, [self.ref('base.res_partner_1')])]}
        self.project = self.env['project.project'].create(project_vals)
        service_product = self.env.ref('product.product_product_consultant')
        service_product.write({'performance': 5.0,
                               'recurring_service': True})
        service_product.performance = 5.0
        service_product.route_ids = [
            (6, 0,
             [self.ref('procurement_service_project.route_serv_project')])]
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id': self.account.id,
            'project_by_task': 'yes'}
        sale_line_vals = {
            'product_id': service_product.id,
            'name': service_product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': service_product.uom_id.id,
            'price_unit': service_product.list_price,
            'performance': 5.0,
            'january': True,
            'february': True,
            'week4': True,
            'week5': True,
            'tuesday': True,
            'thursday': True}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_create_event_with_hour(self):
        cond = [('product_id', '!=', False)]
        move_line = self.move_line_model.search([], limit=1)
        move_line.journal_id.type = 'sale'
        move_line._prepare_analytic_line(move_line)
        self.sale_order.action_button_confirm()
        sale_line = self.sale_order.order_line[0]
        cond = [('project_id', '=', self.project.id)]
        event = self.event_model.search(cond, limit=1)
        event.assign_partners()
        registration_vals = {
            'name': 'aaaaaaa',
            'event_id': event.id,
            'partner_id': self.ref('base.res_partner_1')}
        registration = self.registration_model.create(registration_vals)
        registration._prepare_wizard_registration_open_vals()
        registration._prepare_date_start_for_track_condition(
            '2016-05-21 17:30:00')
        registration._prepare_date_end_for_track_condition(
            '2016-07-21 19:00:00')
        registration._prepare_wizard_reg_cancel_vals()
        wiz_append_vals = {
            'from_date': '2016-02-01',
            'to_date': '2016-02-28',
            'partner': self.ref('base.res_partner_2')}
        wiz = self.wiz_append_model.create(wiz_append_vals)
        wiz.with_context({'active_ids': [event.id]}).action_append()
        wiz = self.wiz_delete_model.create(wiz_append_vals)
        wiz.with_context(
            {'active_ids': [event.id]}).action_nodelete_past_and_later()
        cond = [('service_project_sale_line', '=', sale_line.id)]
        task = self.task_model.search(cond, limit=1)
        task.show_sessions_from_task()
        self.assertNotEqual(
            len(task.sessions), 0,
            'Sessions no generated')
