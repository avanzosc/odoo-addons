import base64
import json
from datetime import date, timedelta

from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal

FLOOR_OPTIONS = {"single": _("Single"), "top": _("Top"), "below": _("Below")}


class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        today = date.today()
        yesterday = date.today() - timedelta(days=1)
        saca_lines = (
            request.env["saca.line"]
            .sudo()
            .search(
                [
                    ("driver_id", "=", partner.id),
                ]
            )
        )
        saca_lines_count_today = saca_lines.filtered(
            lambda l: l.date and l.date <= today and l.date >= yesterday
        )
        values.update(
            {
                "saca_lines_count": len(saca_lines),
                "saca_lines_count_today": len(saca_lines_count_today),
            }
        )
        return values

    @http.route(
        ["/my/saca/lines", "/my/saca/lines/all"], type="http", auth="user", website=True
    )
    def saca_lines(self, today=False, show_all=False, **post):
        values = {}
        partner = request.env.user.partner_id
        saca_type_ids = self.get_saca_types()
        domain = [
            ("stage_id", "in", saca_type_ids),
        ]
        if today:
            today = date.today()
            yesterday = date.today() - timedelta(days=1)
            domain += [("date", "<=", today), ("date", ">=", yesterday)]
        if not show_all:
            domain += [("driver_id", "=", partner.id)]
        saca_lines = request.env["saca.line"].sudo().search(domain, order="seq")
        sacas = (
            request.env["saca"]
            .sudo()
            .search([("saca_line_ids", "in", saca_lines.ids)], order="date desc")
        )
        values.update(
            {
                "page_name": "saca",
                "today": today,
                "partner": partner,
                "sacas": sacas,
                "saca_lines": saca_lines,
                "show_all": show_all,
            }
        )
        return http.request.render("website_custom_saca.portal_my_saca_lines", values)

    @http.route(
        ["/my/saca/line/<int:saca_line_id>"], type="http", auth="user", website=True
    )
    def saca_line(
        self,
        saca_line_id=None,
        access_token=None,
        download=None,
        show_all=False,
        **post
    ):
        values = {}
        partner = request.env.user.partner_id
        saca_line = request.env["saca.line"].sudo().browse(saca_line_id)
        values_update = {}
        for arg in post:
            values_update.update({arg: post.get(arg)})
        if values_update:
            files = request.httprequest.files
            self.update_saca_line_fields(
                line=saca_line, update_vals=values_update, files=files
            )
        domain = [("saca_id", "=", saca_line.saca_id.id)]
        if not show_all:
            domain += [(("driver_id", "=", partner.id))]
        saca_lines = request.env["saca.line"].sudo().search(domain, order="seq")
        saca_line_ids = saca_lines.ids or False
        value_index = saca_line_ids.index(saca_line.id) if saca_line_ids else False
        next_saca_line_id = None
        prev_saca_line_id = None
        if value_index:
            try:
                next_saca_line_id = saca_line_ids[value_index + 1]
            except IndexError:
                next_saca_line_id = None

            try:
                prev_saca_line_id = (
                    saca_line_ids[value_index - 1] if value_index else None
                )
            except IndexError:
                prev_saca_line_id = None
        toristas = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    (
                        "category_id",
                        "=",
                        (request.env.ref("custom_descarga.torista_category").id),
                    )
                ]
            )
        )
        timesheet_ids = saca_line.timesheet_ids.filtered(
            lambda t: t.task_id.name in ["Chofer", "Carga"]
        )
        values.update(
            {
                "page_name": "saca_line",
                "saca_line": saca_line,
                "logged_user": request.env.user,
                "next_saca_line_id": next_saca_line_id,
                "prev_saca_line_id": prev_saca_line_id,
                "access_token": access_token,
                "date_today": date.today(),
                "toristas": toristas,
                "floor_options": FLOOR_OPTIONS,
                "timesheet_ids": timesheet_ids,
                "show_all": show_all,
            }
        )
        return http.request.render("website_custom_saca.portal_saca_line", values)

    @http.route(
        "/saca/line/print/<int:saca_id>",
        type="http",
        auth="user",
        website=True,
        sitemap=False,
    )
    def saca_line_print(self, saca_id, review=False, answer_token=None, **post):
        saca_line = request.env["saca.line"].sudo().browse(saca_id)
        return CustomerPortal()._show_report(
            model=saca_line,
            report_type="pdf",
            report_ref="website_custom_saca.action_report_driver_saca",
            download=True,
        )

    @http.route(
        "/saca/line/send/<int:saca_line_id>",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def saca_line_send(self, saca_line_id, **post):
        saca_line = request.env["saca.line"].sudo().browse(saca_line_id)
        saca_line.action_send_saca_mail()
        return json.dumps({"success": True, "message": "Message sent!"})

    def update_saca_line_fields(self, line, update_vals, files=None):
        for value in update_vals:
            new_val = None
            if value in ["btn_start", "btn_finish"]:
                line.set_timesheet_start_stop(value, int(update_vals.get(value)))
                break
            ttype = line.sudo()._fields[value]
            if ttype.type == "float":
                try:
                    new_val = (
                        float(update_vals.get(value))
                        if update_vals.get(value) != ""
                        else None
                    )
                except (ValueError, TypeError):
                    new_val = 0

            if ttype.type in ["integer"] or value == "torista_id":
                try:
                    new_val = (
                        int(update_vals.get(value))
                        if update_vals.get(value) != ""
                        else None
                    )
                except (ValueError, TypeError):
                    new_val = 0

            if ttype.type in ["char", "text", "selection"]:
                if update_vals.get(value) != "0":
                    new_val = update_vals.get(value)

            if ttype.type in ["boolean"]:
                new_val = update_vals.get(value)
                new_val = 1 if new_val == "on" else 0
            if new_val and getattr(line, value) != new_val:
                line.update({value: new_val})

        if not update_vals.get("forklift", None):
            line.forklift = False

    @http.route(
        ["/saca/line/<int:saca_line_id>/<int:signer_id>/accept"],
        type="json",
        auth="public",
        website=True,
    )
    def portal_saca_line_accept(
        self, saca_line_id=None, signer_id=None, *args, **kwargs
    ):
        kwargs.get("access_token")
        kwargs.get("res_id")
        signature = kwargs.get("signature")
        request.env["res.users"].browse(request.session.get("uid"))
        saca_line = request.env["saca.line"].sudo().browse(saca_line_id)
        if not signature:
            return {"error": _("Signature is missing.")}
        signer = request.env["res.partner"].sudo().browse(signer_id)
        self.sign_saca_line(saca_line, signer, signature)
        redirect_url = "/my/saca/line/" + str(saca_line_id)

        return {
            "force_refresh": True,
            "redirect_url": redirect_url,
        }

    def sign_saca_line(self, saca_line_id, signer, signature):
        if saca_line_id:
            if saca_line_id.driver_id == signer:
                saca_line_id.signature_driver = signature
                saca_line_id.date_signature_driver = date.today()

            if saca_line_id.farmer_id == signer:
                saca_line_id.signature_farm = signature
                saca_line_id.date_signature_farm = date.today()

    def get_saca_types(self):
        stage_saca = request.env.ref(
            "custom_saca_purchase.stage_saca", raise_if_not_found=False
        )
        stage_descarga = request.env.ref(
            "custom_descarga.stage_descarga", raise_if_not_found=False
        )
        return [stage_saca.id, stage_descarga.id]

    @http.route(
        ["/my/saca/line/<int:saca_line_id>/binary"],
        type="http",
        auth="public",
        csrf=False,
        methods=["POST"],
        website=True,
    )
    def save_ticket_binary(self, saca_line_id, **post):
        image_field = post.get("image_field", None)
        file = post.get("image_file")
        if saca_line_id and file:
            saca_line = request.env["saca.line"].sudo().browse(saca_line_id)

            Attachments = request.env["ir.attachment"]
            name = post.get("image_file").filename.replace(" ", "_")
            attachment = file.read()
            # DEPRECATED: file_base64 = base64.encodestring(attachment)
            file_base64 = base64.encodebytes(attachment)
            attachment_id = Attachments.sudo().create(
                {
                    "name": name,
                    "res_name": name,
                    "type": "binary",
                    "res_model": "saca.line",
                    "res_id": saca_line_id,
                    "datas": file_base64,
                }
            )

            saca_line.update({image_field: attachment_id.id})
        return request.redirect("/my/saca/line/%d" % saca_line_id)
        # return json.dumps({'success': True, 'message': "File uploaded!"})
