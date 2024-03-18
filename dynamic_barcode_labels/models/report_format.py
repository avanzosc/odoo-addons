# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

from odoo import models, fields


class report_paperformat(models.Model):
    _inherit = "report.paperformat"
    custom_report = fields.Boolean('Temp Formats', default=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
