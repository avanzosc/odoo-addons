# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models
from io import BytesIO
import zipfile
import base64


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _generate_zip(self, files):
        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w",
                             compression=zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.writestr(f[0], f[1])
        zip_file = mem_zip.getvalue()
        mem_zip.close()
        return zip_file

    @api.multi
    def _action_download_attachments(self):
        files = []
        for attach in self:
            file = base64.b64decode(attach.datas)
            files.append((attach.name, file))
        zip_file = self._generate_zip(files)
        attach_id = self.create({'datas': base64.b64encode(zip_file), 'name':
            'xxx'})
        file_url = "/web/binary/saveas?model=ir.attachment&field=datas&" \
                   "filename_field=datas_fname&id=%s" % str(attach_id.id)
        return {
            'type': 'ir.actions.act_url',
            'url': file_url,
            'target': 'new'
        }

    @api.model
    def _generate_zip_from_attachments(self, res_model, res_id):
        files = []
        for attach in self.env['ir.attachment'].search(
                [('res_model', '=', str(res_model)), ('res_id', '=', res_id)]):
            file = base64.b64decode(attach.datas)
            files.append((attach.name, file))
        zip_file = self._generate_zip(files)
        file_name = "%s/%s" % ((self.env["ir.model"].search(
            [("model", "=", self._context.get("active_model"))]).name or ""),
                               fields.Datetime.now())
        attach_id = self.create({'datas': base64.b64encode(zip_file),
                                 'name': file_name})
        file_url = "/web/binary/saveas?model=ir.attachment&field=datas&" \
                   "filename_field=datas_fname&id=%s" % str(attach_id.id)
        return {
            'type': 'ir.actions.act_url',
            'url': file_url,
            'target': 'new'
        }
