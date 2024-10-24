from odoo.http import Controller, request, route


class MailTrackController(Controller):
    @route("/mail/track/click/<int:trace_id>", type="http", auth="public", website=True)
    def track_click(self, trace_id, redirect_url=None, **kwargs):
        """
        Logs the click event and redirects the user to the original URL
        """
        trace = request.env["mailing.trace"].sudo().browse(trace_id)
        if trace:
            trace.write({"status": "clicked"})

        if redirect_url:
            return request.redirect(redirect_url)
        return request.redirect("/")
