# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class IrActionsReportXml(models.Model):
    _inherit = "ir.actions.report.xml"

    report_copies = fields.Integer(string="# Copies", default=1)
