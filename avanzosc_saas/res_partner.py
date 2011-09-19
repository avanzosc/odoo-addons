from osv import osv
from osv import fields

class res_partner(osv.osv):
    _inherit = 'res.partner'
 
    _columns = {
                'saas_server_ids':fields.one2many('saas.server', 'partner_id', 'Server List'),
    }
res_partner()