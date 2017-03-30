# -*- coding: utf-8 -*-
# (c) 2016 Oihane Crucelaegui - AvanzOSC
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    partners = fields.Many2many(comodel_name='res.partner',
                                relation='projet_partner_rel',
                                column1='project',
                                column2='partner')
