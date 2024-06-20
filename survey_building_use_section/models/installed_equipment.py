from odoo import fields, models


class InstalledEquipment(models.Model):
    _name = "installed.equipment"
    _description = "Installed Equipment"

    name = fields.Char(
        "Equipment Name", 
        required=True
    )
