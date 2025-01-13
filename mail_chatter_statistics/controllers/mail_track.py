import base64
import logging
from io import BytesIO

from PIL import Image

from odoo import http
from odoo.http import request

from odoo.addons.mail.controllers.main import MailController

_logger = logging.getLogger(__name__)


class MailController(MailController):
    @http.route()
    def mail_action_view(self, model=None, res_id=None, access_token=None, **kwargs):
        response = super(MailController, self).mail_action_view(
            model, res_id, access_token, **kwargs
        )

        if kwargs.get("mail_chatter_statistics"):
            trace_id = kwargs.get("mail_chatter_statistics_trace_id")
            if trace_id:
                _logger.info("Tracking click for trace ID: %s", trace_id)
                trace = (
                    request.env["mailing.trace"]
                    .sudo()
                    .search([("id", "=", trace_id)], limit=1)
                )
                if trace:
                    trace.track_click()

        return response


class MailTrackingController(http.Controller):
    @http.route("/mail/track/open/<int:trace_id>", type="http", auth="public")
    def track_open(self, trace_id):
        _logger.info("Tracking open for trace ID: %s", trace_id)
        trace = (
            request.env["mailing.trace"].sudo().search([("id", "=", trace_id)], limit=1)
        )

        if trace:
            trace.track_open()

        image = Image.new("RGB", (1, 1), color="white")
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()

        return http.Response(
            f"data:image/png;base64,{img_base64}", content_type="image/png"
        )
