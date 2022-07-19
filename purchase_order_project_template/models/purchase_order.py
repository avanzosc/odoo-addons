# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_template_id = fields.Many2one(
        string="Project template", comodel_name="project.project", copy=False)
    project_id = fields.Many2one(
        string="Project", comodel_name="project.project", copy=False)

    @api.multi
    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        for purchase in self.filtered(
            lambda x: x.state not in ('draft', 'sent') and
                x.project_template_id and not x.project_id):
            purchase._create_project_from_project_template()
        return result

    def _create_project_from_project_template(self):
        project_obj = self.env['project.project']
        result = self.project_template_id.create_project_from_template()
        project = project_obj.browse(result.get('res_id'))
        project_name = project.name
        name = project_name.replace(" (COPY)", "")
        project.name = "{} - {}".format(name, self.name)
        self.project_id = project.id
        project.write({'origin_purchase_id': self.id,
                       'partner_id': self.partner_id.id
                       })

    def create_project_from_project_template(self):
        for purchase in self.filtered(
            lambda x: x.state not in ('draft', 'sent') and
                x.project_template_id and not x.project_id):
            purchase._create_project_from_project_template()
