# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, exceptions, fields, models, _
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

    @api.model
    def _generate_zip_from_attachments(self, records,
                                       att_fields=None):
        files = []
        if att_fields:
            att_fields = self.env["ir.model.fields"].browse(att_fields)
            for attach in records:
                for field in att_fields:
                    if attach[field.name]:
                        file = base64.b64decode(attach[field.name])
                        files.append((attach.name, file))
        else:
            for attach in self.env['ir.attachment'].search(
                    [('res_model', '=', str(records._name)),
                     ('res_id', '=', records._ids)]):
                file = base64.b64decode(attach.datas)
                files.append((attach.name, file))
        if files:
            zip_file = self._generate_zip(files)
            model = [("model", "=", self._context.get("active_model"))]
            file_name = "%s/%s" % ((self.env["ir.model"].search(model).name
                                    or ""), fields.Datetime.now())
            attach_id = self.create({'datas': base64.b64encode(zip_file),
                                     'name': file_name})
            file_url = "/web/binary/saveas?model=ir.attachment&field=datas&" \
                       "filename_field=datas_fname&id=%s" % str(attach_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': file_url,
                'target': 'new'
            }
        else:
            raise exceptions.Warning(_("No files to download"))
