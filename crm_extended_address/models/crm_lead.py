
from odoo import fields, models

class CRMlead(models.Model):
    _inherit = 'crm.lead'
    
    comercial_name = fields.Char(string='Comercial name')
    billing_phone = fields.Char(string='Billing phone')
    billing_email = fields.Char(string='Billing email')
    
    sending_street = fields.Char(string='Sending street', readonly=False)
    sending_street2 = fields.Char(string='Sending street2')
    sending_zip = fields.Char(string='Sending zip', change_default=True)
    sending_city = fields.Char(string='Sending city')
    sending_state_id = fields.Many2one(comodel_name="res.country.state", string='Sending state')
    sending_country_id = fields.Many2one(comodel_name='res.country', string='Sending country')
    sending_phone = fields.Char(string='Sending phone')
    sending_email = fields.Char(string='Sending email')
