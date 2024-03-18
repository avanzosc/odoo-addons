from odoo import http
from odoo.addons.web.controllers.main import ReportController
import json


class PrtReportController(ReportController):
    @http.route()
    def report_download(self, data, token):
        res = super(PrtReportController, self).report_download(data, token)
        if json.loads(data)[2] in ('open', 'print'):
            res.headers['Content-Disposition'] = res.headers['Content-Disposition'].replace('attachment', 'inline')
        return res
