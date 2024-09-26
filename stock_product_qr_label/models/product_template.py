# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name_for_labels = fields.Char(
        string="Name for labels", compute="_compute_name_for_labels"
    )
    user_for_label_id = fields.Many2one(
        string="User For Label",
        comodel_name="res.users",
        compute="_compute_user_for_label_id",
    )
    company_for_label_id = fields.Many2one(
        string="Company For Label",
        comodel_name="res.company",
        compute="_compute_company_for_label_id",
    )

    def _compute_name_for_labels(self):
        max_length = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_name_max_length_for_labels", default=55)
        )
        for template in self:
            name_for_labels = ""
            if max_length > len(template.name):
                name_for_labels = template.name
            else:
                name_for_labels = template.name[0:max_length]
            template.name_for_labels = name_for_labels

    def _compute_user_for_label_id(self):
        for template in self:
            template.user_for_label_id = self.env.user.id

    def _compute_company_for_label_id(self):
        for template in self:
            template.company_for_label_id = self.env.company.id
