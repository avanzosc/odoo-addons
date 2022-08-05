# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    farm_numexp = fields.Char(string='Rega')
    ates = fields.Char(string='Ates')
    distance = fields.Float(string='Distance')
    chicken_supplier = fields.Boolean(
        string="Is Live Chicken Supplier?", default=False)
    chicken_supplier_id = fields.Many2one(
        string="Chicken Supplier", comodel_name="res.partner")
    is_supplier = fields.Boolean(
        string="Is Supplier?", compute="_compute_is_supplier", store=True)
    is_farmer = fields.Boolean(
        string="Is Farmer?", compute="_compute_is_supplier", store=True)
    farm = fields.Boolean(
        string="Is a Farm?", compute="_compute_is_supplier", store=True)
    main_scale = fields.Many2one(string="Scale", comodel_name="main.scale")

    @api.depends("contact_type_id")
    def _compute_is_supplier(self):
        for partner in self:
            try:
                farm = self.env.ref("custom_saca.type_farm").id
                supplier = self.env.ref("custom_saca.type_supplier").id
                farmer = self.env.ref("custom_saca.type_farmer").id
            except Exception:
                supplier = False
                farmer = False
                farm = False
            if supplier == partner.contact_type_id.id:
                partner.is_supplier = True
                partner.is_farmer = False
                partner.chicken_supplier_id = False
                partner.farm = False
            elif farmer == partner.contact_type_id.id:
                partner.is_farmer = True
                partner.is_supplier = False
                partner.chicken_supplier = False
                partner.chicken_supplier_id = False
                partner.farm = False
            elif farm == partner.contact_type_id.id:
                partner.farm = True
                partner.is_supplier = False
                partner.is_farmer = False
                partner.chicken_supplier_id = False
            else:
                partner.is_farmer = False
                partner.is_supplier = False
                partner.chicken_supplier = False
                partner.chicken_supplier_id = False
