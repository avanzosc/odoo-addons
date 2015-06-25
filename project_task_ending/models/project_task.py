# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    ending = fields.Boolean(
        string='Task Ending Type',
        help='')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    ended = fields.Boolean(
        string='Task Ended', related='stage_id.ending', store=True)

    @api.one
    def write(self, values):
        if 'stage_id' in values:
            stage = self.env['project.task.type'].browse(
                values.get('stage_id', False))
            if stage and stage.ending and not self.ended:
                values.update({
                    'date_end': fields.Datetime.now(),
                })
            if stage and not stage.ending and self.ended:
                values.update({
                    'date_end': False,
                })
        super(ProjectTask, self).write(values)
