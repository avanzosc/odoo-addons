# -*- coding: utf-8 -*-
# (c) 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.osv import orm
from openerp.tools.translate import _


class ProjectTask(orm.Model):
    _inherit = 'project.task'

    def do_delegate(self, cr, uid, ids, delegate_data=None, context=None):
        """ Delegate Task to another users. """
        if delegate_data is None:
            delegate_data = {}
        assert delegate_data['user_id'],\
            _("Delegated User should be specified")
        delegated_tasks = {}
        if not delegate_data.get('split_in'):
            delegated_tasks = super(ProjectTask, self).do_delegate(
                cr, uid, ids, delegate_data=delegate_data, contex=context)
        else:
            for task in self.browse(cr, uid, ids, context=context):
                for i in range(delegate_data['split_in']):
                    delegated_task_id = self.copy(cr, uid, task.id, {
                        'name': delegate_data['name'],
                        'user_id': False,
                        'project_id': (delegate_data['project_id'] and
                                       delegate_data['project_id'][0] or
                                       False),
                        'stage_id': task.stage_id.id,
                        'planned_hours': delegate_data['planned_hours'] or 0.0,
                        'remaining_hours': (delegate_data['planned_hours'] or
                                            0.0),
                        'parent_ids': [(6, 0, [task.id])],
                        'description': (
                            delegate_data['new_task_description'] or ''),
                        'child_ids': [],
                        'work_ids': [],
                    }, context=context)
                    self._delegate_task_attachments(cr, uid, task.id,
                                                    delegated_task_id,
                                                    context=context)
                remain = (delegate_data['split_in'] *
                          delegate_data['planned_hours_me'])
                task.write({
                    'name': delegate_data['prefix'],
                    'remaining_hours': remain})
                delegated_tasks[task.id] = delegated_task_id
        return delegated_tasks
