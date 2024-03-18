import hashlib
from random import choice

from odoo import api, fields, models
from odoo.tools import pycompat


def _attachment2url(att):
    sha = hashlib.md5(pycompat.to_text(att.datas).encode("utf-8")).hexdigest()[0:7]
    return "/web/image/{}-{}".format(att.id, sha)


class IRAttachmentBackground(models.Model):
    _inherit = "ir.attachment"

    use_as_background = fields.Boolean("Use as login page background", default=False)

    @api.multi
    def check(self, mode, values=None):
        ids = self.ids
        cr = self.env.cr
        if ids and mode == "read":
            if isinstance(ids, int):
                ids = [ids]
            ids = ids[:]  # make a copy
            cr.execute(
                "SELECT id,use_as_background FROM ir_attachment WHERE id = ANY (%s)",
                (ids,),
            )
            for attachment_id, use_as_background in cr.fetchall():
                if use_as_background:
                    ids.remove(attachment_id)
            if not ids:
                return
        return super(IRAttachmentBackground, self).check(mode, values=values)

    def _get_background_images_domain(self):
        return [("use_as_background", "=", True)]

    @api.model
    def get_background_pic(self):
        pictures = self.search(self._get_background_images_domain())
        if pictures:
            p = choice(pictures)
            picture_url = p.url or _attachment2url(p)
            return picture_url
        else:
            return False
