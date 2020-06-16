# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class Report(models.Model):
    _inherit = 'report'

    @api.v7
    def print_document(self, cr, uid, ids, report_name, html=None,
                       data=None, context=None):
        if not context:
            context = {}
        for id in ids:
            if 'active_model' in context:
                active_model = context.get('active_model')
                partner_id = False
                if active_model == 'res.partner':
                    partner_id = id
                else:
                    try:
                        partner_id = self.pool[
                            active_model].browse(
                                cr, uid, id, context=context).partner_id.id
                    except:
                        pass
                conf_obj = self.pool['res.partner.report.configurator']
                report_obj = self.pool['ir.actions.report.xml']
                report_id = report_obj.search(
                    cr, uid, [('model', '=', active_model),
                              ('report_name', '=', report_name)], limit=1,
                    context=context)
                conf_id = conf_obj.search(
                    cr, uid, [('partner_id', '=', partner_id),
                              ('report_id', '=', report_id)], limit=1,
                    context=context)
                configurator = conf_obj.browse(
                    cr, uid, conf_id, context=context)
                context['report_copies'] = configurator.copy_num
            return super(Report, self).print_document(
                cr, uid, [id], report_name, html=html, data=data,
                context=context)


class ResPartnerReportConfigurator(models.Model):
    _name = "res.partner.report.configurator"

    report_id = fields.Many2one(
        comodel_name="ir.actions.report.xml", string="Report",
        domain="[('report_type', 'in', ['qweb-pdf'])]")
    report_model = fields.Char(
        string="Report Model", related="report_id.model", store=True)
    copy_num = fields.Integer(string="# Copies", default=1)
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner")


class ResPartner(models.Model):
    _inherit = "res.partner"

    report_ids = fields.One2many(
        comodel_name="res.partner.report.configurator",
        inverse_name="partner_id", string="Reports")
    childs_report_ids = fields.One2many(
        comodel_name="res.partner.report.configurator", string="Reports",
        compute="_compute_childs_reports")

    @api.depends('child_ids', 'child_ids.report_ids')
    def _compute_childs_reports(self):
        for partner in self:
            child_report_ids = []
            for child in partner.child_ids:
                child_report_ids += child.report_ids.ids
            partner.childs_report_ids = child_report_ids
