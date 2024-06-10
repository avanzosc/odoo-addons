from odoo import models, fields, _

class InstalledEquipment(models.Model):
    _name = 'installed.equipment'
    _description = 'Installed Equipment'

    name = fields.Char(string=_("Equipment Name"), required=True)
