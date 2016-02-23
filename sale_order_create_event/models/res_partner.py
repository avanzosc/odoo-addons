# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sessions_tasks = fields.Many2many(
        comodel_name="project.task", relation="task_session_partners_relation",
        column1="session_partner_id", column2="session_task_id",
        string="Task of sessions")
