from . import controllers
from . import models

# __init__.py
from bs4 import BeautifulSoup
from urllib.parse import unquote
import logging
from odoo import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    MailMail = env["mail.mail"]

    tracked_mails = MailMail.search([("body_html", "ilike", "/mail/track/click/")])

    for mail in tracked_mails:
        body_html = mail.body_html
        soup = BeautifulSoup(body_html, "html.parser")

        for a_tag in soup.find_all("a", href=True):
            tracked_url = a_tag["href"]
            if "/mail/track/click/" in tracked_url:
                original_url = unquote(tracked_url.split("redirect_url=")[-1])
                a_tag["href"] = original_url

        mail.body_html = str(soup)

    _logger = logging.getLogger(__name__)
    _logger.info(
        "Enlaces de rastreo revertidos exitosamente en los registros de mail.mail."
    )
