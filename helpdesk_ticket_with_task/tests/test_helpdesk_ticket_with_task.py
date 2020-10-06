# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestHelpdeskTicketWithTask(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestHelpdeskTicketWithTask, cls).setUpClass()
        cond = [('task_id', '!=', False)]
        cls.sale_line = cls.env['sale.order.line'].search(cond, limit=1)
        cond = [('sale_order_id', '=', False),
                ('task_id', '=', False)]
        cls.ticket = cls.env['helpdesk.ticket'].search(cond, limit=1)
        cls.ticket.sale_order_id = cls.sale_line.order_id.id
        cls.task_obj = cls.env['project.task']

    def test_helpdesk_ticket_with_task(self):
        cond = [('sale_line_id', '=', False),
                ('sale_order_id', '=', False)]
        tasks = self.task_obj.search(cond)
        lines = self.sale_line.order_id.mapped(
            'order_line').filtered(lambda x: x.task_id)
        if lines:
            tasks += lines.mapped('task_id')
        for task in tasks:
            self.assertIn(task, self.ticket.allowed_tasks_ids)
        self.assertEqual(len(tasks), len(self.ticket.allowed_tasks_ids))
