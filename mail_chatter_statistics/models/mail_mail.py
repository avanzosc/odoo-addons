from bs4 import BeautifulSoup
from werkzeug.urls import url_quote
import re

from odoo import models

class MailMail(models.Model):
    _inherit = "mail.mail"

    def send(self, auto_commit=False, raise_exception=False):

        for mail in self:
            is_chatter_mail = mail.mail_message_id
            
            if is_chatter_mail and mail.email_to:
                email = mail.email_to

                trace = self.env["mailing.trace"].create(
                    {
                        "mail_message_id": mail.id,
                        "email": email,
                        "message_id": mail.message_id,
                    }
                )
                mail.body_html = self._add_tracking(mail.body_html, trace.id)
                trace.write({"status": "tracking_added"})

        return super().send(auto_commit=auto_commit, raise_exception=raise_exception)

    def _add_tracking(self, body_html, trace_id):
        tracking_pixel = f'<img src="/mail/track/open/{trace_id}" \
            width="1" height="1" style="display:none"/>'
        body_html = body_html.replace("</body>", f"{tracking_pixel}</body>")
        body_html = self._replace_links_with_tracked(body_html, trace_id)
        return body_html

    def _replace_links_with_tracked(self, body_html, trace_id):
        soup = BeautifulSoup(body_html, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            original_url = a_tag["href"]
            tracked_url = (
                f"/mail/track/click/{trace_id}?redirect_url={url_quote(original_url)}"
            )
            a_tag["href"] = tracked_url

        return str(soup)
