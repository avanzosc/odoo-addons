from osv import osv
from osv import fields

class res_partner(osv.osv):
    _inherit = 'res.partner'
 
    _columns = {
        'server_ip': fields.char('Server IP', size=15),
        'ssh_user': fields.char('SSH User', size=64),
        'ssh_pass': fields.char('SSH Password', size=64),   
        'postgres_user': fields.char('Postgres User', size=64),
        'postgres_pass': fields.char('Postgres Password', size=64),
        'super_admin': fields.char('Super Admin', size=64),
        'saas_db_ids':fields.one2many('saas.db', 'partner_id', 'Database List'),
    }
res_partner()