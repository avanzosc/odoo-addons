import base64
from io import BytesIO

import qrcode

from odoo import api, fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    qr_code = fields.Char(
        "QR Code",
        compute="_compute_qr_code",
        store=True,
    )

    @api.depends("sequence")
    def _compute_qr_code(self):
        for workorder in self:
            if workorder.sequence:
                sequence_str = str(workorder.sequence)

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(sequence_str)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

                workorder.qr_code = qr_image
            else:
                workorder.qr_code = False
