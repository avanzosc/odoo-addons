
from odoo import _, api, fields, models

class updateProgenitorIntoMailListWizard(models.TransientModel):
    _name = "update.progenitor.into.mail.list.wizard"
    _description = "Wizard to add progenitors and students into mail list"
    
    list_type = fields.Selection(selection=[
        ('student', 'Student'),
        ('progenitor', 'Progenitor'),
        ('both', 'Both')],
        string='List type', default='both',
        required="True"
    )
    mass_mailing_list_id = fields.Many2one(
        string="Mail list",
        comodel_name="mail.mass_mailing.list", required="True",
        domain = "[('list_type', '=', list_type)]")
    
    @api.multi
    def button_update_list(self):
        self.ensure_one()
        partner_report_id = self.env['education.group.student.progenitor.report'].search([('id','=',self.env.context.get("active_id"))])
        if self.list_type == 'student':
            addStudentToList(self,partner_report_id.student_id, self.mass_mailing_list_id)
        elif self.list_type == 'progenitor':
            addProgenitorsToList(self,partner_report_id.progenitor_ids, self.mass_mailing_list_id)
        else:
            addStudentToList(self,partner_report_id.student_id, self.mass_mailing_list_id)
            addProgenitorsToList(self,partner_report_id.progenitor_ids, self.mass_mailing_list_id)

class updateStudentIntoMailListWizard(models.TransientModel):
    _name = "update.student.into.mail.list.wizard"
    _description = "Wizard to add students into mail list"
    
    mass_mailing_list_id = fields.Many2one(
        string="Mail list",
        comodel_name="mail.mass_mailing.list", required="True",
        domain = "[('list_type', '=', 'student')]")
    
    @api.multi
    def button_update_list(self):
        self.ensure_one()
        partner_report_id = self.env['education.group.student.report'].search([('id','=',self.env.context.get("active_id"))])
        addStudentToList(self,partner_report_id.student_id, self.mass_mailing_list_id)
    
    
def addStudentToList(self, student_id, list_id):
    if not partnerExistInList(self,student_id, list_id):
        if not student_id.email:
            email = str(student_id.name) + "@nomail.no"
        else:
            email = student_id.email
        if not partnerExist(self,student_id):
            mailing_contact_id = self.env['mail.mass_mailing.contact'].create({
                'email': email,
                'company_name':student_id.company_id.name,
                'name': student_id.name
                })
        else:
            mailing_contact_id = self.env['mail.mass_mailing.contact'].search([('email','=',email)])
        self.env['mail.mass_mailing.list_contact_rel'].create({
            'contact_id': mailing_contact_id.id,
            'list_id': list_id.id
        })

def addProgenitorsToList(self, progenitor_ids, list_id):
    for progenitor in progenitor_ids:
        if not partnerExistInList(self,progenitor, list_id):
            if not progenitor.email:
                email = str(progenitor.name) + "@nomail.no"
            else:
                email = progenitor.email
            if not partnerExist(self,progenitor):
                mailing_contact_id = self.env['mail.mass_mailing.contact'].create({
                    'email': email,
                    'company_name':progenitor.company_id.name,
                    'name': progenitor.name
                    })
            else:
                mailing_contact_id = self.env['mail.mass_mailing.contact'].search([('email','=',email)])
            self.env['mail.mass_mailing.list_contact_rel'].create({
                'contact_id': mailing_contact_id.id,
                'list_id': list_id.id
            })

def partnerExistInList(self, partner_id, list_id):
    list_contact_id = self.env['mail.mass_mailing.list_contact_rel'].search_count([('contact_id.email','in',(partner_id.email,str(partner_id.name)+'@nomail.no')),('list_id','=',list_id.id)])
    return list_contact_id > 0;

def partnerExist(self, partner_id):
    list_contact_id = self.env['mail.mass_mailing.contact'].search_count([('email','in',(partner_id.email,str(partner_id.name)+'@nomail.no'))])
    return list_contact_id > 0;

        