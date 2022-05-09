from odoo import fields, models

class ProductFinal(models.Model):
    _name = "product.final"
    _description = "Final Product"
    _order = "code"
  
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
   
    def name_get(self):        
        result=[]
        for rec in self:
            result.append((rec.id, "[%s] - %s" % (rec.code,rec.name)))
        return result
    
    def _name_search(self, name, args=None, operator="ilike", limit=10):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("code", operator, name)]
            return self._search(domain + args, limit=limit) 
