'''
Created on 19/01/2011

@author: daniel
'''

from osv import fields,osv
from tools.translate import _

class res_partner(osv.osv): 

    _description = 'res partner Inheritance'
    _inherit = 'res.partner'
    _columns = {
                'postage': fields.selection([('paid','Paid'),('due','Due'),('asum','Asummed')], 'Postage'),
        }

res_partner()

class res_partner_address (osv.osv): 
    
    _description = 'res partner address Inheritance'
    _inherit = 'res.partner.address'
    _columns = {
                'box': fields.char('Post Office Box', size=64),
        }

res_partner_address()

