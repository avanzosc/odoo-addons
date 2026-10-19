import base64

from markupsafe import escape

from odoo import _, http
from odoo.http import request


class StockPickingCmrDecaController(http.Controller):
    def _gone_notice_html(self, title, body, url=None):
        link = (
            '<p><a href="%(url)s">%(url)s</a></p>' % {"url": escape(url)} if url else ""
        )
        return (
            '<!DOCTYPE html><html><head><meta charset="utf-8">'
            "<title>%(title)s</title></head><body "
            'style="font-family:sans-serif;max-width:32em;margin:4em auto;'
            'padding:0 1em;">'
            "<h1>%(title)s</h1><p>%(body)s</p>%(link)s"
            "</body></html>"
        ) % {"title": escape(title), "body": escape(body), "link": link}

    def _superseded_notice_html(self, deca):
        return self._gone_notice_html(
            _("This DeCA has been superseded"),
            _(
                "%(name)s is no longer the current document for this "
                "shipment. A new DeCA was issued to replace it:",
                name=deca.name,
            ),
            url=deca.superseded_by_id.public_url,
        )

    def _cancelled_notice_html(self, deca):
        return self._gone_notice_html(
            _("This DeCA has been cancelled"),
            _(
                "%(name)s was cancelled before its transport service "
                "started and is no longer valid for this shipment.",
                name=deca.name,
            ),
        )

    @http.route(
        "/deca/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def deca_download(self, token, **kwargs):
        """Public, login-free, single-GET PDF download: the only access
        control is the token itself (Resolución, ap. Tercero.4 forbids
        credentials, an intermediate page or a download button) -- for the
        one DeCA a given URL is actually meant to serve. A superseded
        (Método B, ap. Quinto.2) or cancelled token is deliberately
        retired, not the active document Tercero.4 is protecting, so
        pointing it at a one-line notice is not the same thing as gating
        a live download.
        """
        deca = (
            request.env["stock.picking.batch"]
            .sudo()
            .search([("token", "=", token)], limit=1)
        )
        if deca and deca.state in ("superseded", "cancelled"):
            deca._log_access(
                request.httprequest.remote_addr, request.httprequest.method, 410
            )
            notice = (
                self._superseded_notice_html(deca)
                if deca.state == "superseded"
                else self._cancelled_notice_html(deca)
            )
            return request.make_response(
                notice,
                status=410,
                headers=[("Content-Type", "text/html; charset=utf-8")],
            )
        if not deca or deca.state == "closed" or not deca.pdf_attachment_id:
            if deca:
                deca._log_access(
                    request.httprequest.remote_addr, request.httprequest.method, 404
                )
                # Odoo's dispatcher rolls back the cursor on a raised/
                # returned HTTPException (this 404), which would
                # otherwise silently discard the access log entry just
                # created above -- commit explicitly so the attempt
                # itself survives being denied.
                request.env.cr.commit()
            raise request.not_found()

        deca._log_access(
            request.httprequest.remote_addr, request.httprequest.method, 200
        )
        pdf_content = base64.b64decode(deca.pdf_attachment_id.datas)
        headers = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf_content)),
            (
                "Content-Disposition",
                http.content_disposition("%s.pdf" % deca.name),
            ),
        ]
        return request.make_response(pdf_content, headers=headers)
