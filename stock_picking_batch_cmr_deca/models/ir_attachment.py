from odoo import _, models
from odoo.exceptions import UserError

# Only a write touching one of these can actually change what a PDF/QR
# *is* -- everything else ir.attachment exposes (thumbnail, description,
# index_content, ...) is cosmetic or Odoo's own bookkeeping. Odoo's PDF
# preview widget, for instance, writes "thumbnail" on this same
# attachment right after every issue (mail/controllers/attachment.py,
# update_thumbnail) -- guarding every field would block that ordinary
# UI action, not just real tampering.
CONTENT_FIELDS = {
    "datas",
    "raw",
    "db_datas",
    "store_fname",
    "checksum",
    "file_size",
    "mimetype",
}


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _deca_guarded(self):
        """The subset of self that is the pdf_attachment_id/qr_attachment_id
        of a non-draft DeCA -- these two files are the ones Verify
        Integrity vouches for (l10n_es_deca.py, pdf_sha256), and
        l10n.es.deca's own write()/unlink() guard cannot protect them
        since ir.attachment is a different model: without this, anyone
        with write access to Attachments could silently swap the PDF a
        driver's QR points to without ever touching the DeCA record.
        Deliberately scoped to just these two fields, not every
        attachment linked to the DeCA (res_model/res_id), so a chatter
        file unrelated to the legal document (e.g. a photo of a
        breakdown) stays freely editable/removable.
        """
        if not self:
            return self.browse()
        decas = (
            self.env["stock.picking.batch"]
            .sudo()
            .search(
                [
                    ("deca_state", "!=", "draft"),
                    "|",
                    ("pdf_attachment_id", "in", self.ids),
                    ("qr_attachment_id", "in", self.ids),
                ]
            )
        )
        guarded_ids = set(decas.pdf_attachment_id.ids) | set(decas.qr_attachment_id.ids)
        return self.filtered(lambda a: a.id in guarded_ids)

    def write(self, vals):
        if (
            CONTENT_FIELDS.intersection(vals)
            and not self.env.context.get("deca_internal_write")
            and self._deca_guarded()
        ):
            raise UserError(
                _(
                    "This file belongs to an issued DeCA and cannot be "
                    "edited directly: register a modification on the DeCA "
                    "instead."
                )
            )
        return super().write(vals)

    def unlink(self):
        if not self.env.context.get("deca_internal_write") and self._deca_guarded():
            raise UserError(
                _("This file belongs to an issued DeCA and cannot be deleted.")
            )
        return super().unlink()
