# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _account_info_for_create_task_service_project(self, vals, procurement):
        vals = super(
            ProjectTask, self)._account_info_for_create_task_service_project(
            vals, procurement)
        if (procurement.sale_line_id.order_id.project_id.date_start and
                procurement.sale_line_id.order_id.project_id.start_time):
            date_start = self._convert_date_to_local_format(
                procurement.sale_line_id.order_id.project_id.date_start).date()
            time = procurement.sale_line_id.order_id.project_id.start_time
            vals['date_start'] = self._put_utc_format_date(date_start, time)
        if (procurement.sale_line_id.order_id.project_id.date and
                procurement.sale_line_id.order_id.project_id.end_time):
            date_end = self._convert_date_to_local_format(
                procurement.sale_line_id.order_id.project_id.date).date()
            time = procurement.sale_line_id.order_id.project_id.end_time
            vals['date_end'] = self._put_utc_format_date(date_end, time)
        return vals

    def _prepare_session_data_from_task(self, event, num_session, date):
        vals = super(ProjectTask, self)._prepare_session_data_from_task(
            event, num_session, date)
        time = self.service_project_sale_line.order_id.project_id.start_time
        vals['date'] = self._put_utc_format_date(date, time)
        return vals
