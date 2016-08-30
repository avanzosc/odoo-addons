# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _
from subprocess import Popen, PIPE
import base64
import os


class WizSaveInvoiceAttachment(models.TransientModel):
    _name = 'wiz.save.invoice.attachment'
    _description = 'Wizard for save attachtments in folder'

    data = fields.Binary('File', readonly=True)
    name = fields.Char('Filename', readonly=True)

    @api.model
    def default_get(self, var_fields):
        attachment_obj = self.env['ir.attachment']
        res = super(WizSaveInvoiceAttachment, self).default_get(var_fields)
        process = Popen(['mktemp',  '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        my_path = stdout[:-1]
        for a in attachment_obj.browse(self.env.context.get('active_ids')):
            file_path = "{}/{}".format(stdout[:-1], a.name)
            result = a._data_get('datas', None)
            b = result.get(a.id)
            with open(file_path, "a+") as file:
                file.write(base64.b64decode(b))
        zip_name = "{}-{}".format(_('invoices_attachments'),
                                  fields.Date.context_today(self))
        params = "zip {}/{} {}/*".format(stdout[:-1], zip_name, stdout[:-1])
        process = Popen([params], stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()
        path = "{}/{}.zip".format(my_path, zip_name)
        if os.path.exists(path):
            f = open(path, 'rb')
            file_data = f.read()
            f.close()
            res.update({'data': base64.b64encode(file_data),
                        'name': "{}.zip".format(zip_name)})
        return res
