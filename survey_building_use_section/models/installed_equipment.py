from odoo import models, fields

class InstalledEquipment(models.Model):
    _name = 'installed.equipment'
    _description = 'Installed Equipment'

    name = fields.Char(string="Equipment Name", required=True)
