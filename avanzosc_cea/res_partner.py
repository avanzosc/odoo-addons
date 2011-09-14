from osv import osv
from osv import fields

class res_partner(osv.osv):
    _inherit = 'res.partner.address'
 
    _columns = {
        'cea': fields.char('CEA', size=20),
        'cee': fields.char('CEE', size=20),
    }
res_partner()
