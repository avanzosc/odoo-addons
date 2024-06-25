from datetime import datetime

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    enroll = fields.Selection(
        [("public", "Public"), ("invite", "On Invitation")],
        default="public",
        string="Enroll Policy",
        required=True,
        help="Condition to enroll: everyone, on invite, " "on payment (sale bridge).",
    )
    visibility = fields.Selection(
        [("public", "Public"), ("members", "Members Only")],
        default="public",
        string="Visibility",
        required=True,
        help="Applied directly as ACLs. Allow to hide channels"
        " and their content for non members.",
    )

    @api.onchange("date_begin", "date_end")
    def compute_unpublish_website(self):
        today = datetime.today()
        for record in self:
            if (not record.date_begin or record.date_begin <= today) and (
                not record.date_end or record.date_end >= today
            ):
                record.website_published = True
            else:
                record.website_published = False
                record.update_data_unpublish()

    def cron_compute_unpublish_website(self):
        events = self.env["event.event"].search(
            [
                #  ('website_published', '=', True)
            ]
        )
        events.compute_unpublish_website()

    def update_data_unpublish(self):
        for event in self:
            event.stage_id = self.env.ref("website_event_track.event_track_stage3").id
            event.make_participants_done()
            event.finish_responsible_courses()

    def make_participants_done(self):
        registration_ids = self.env["event.registration"].search(
            [("event_id", "=", self.id), ("state", "in", ["draft", "open"])]
        )
        for registration in registration_ids:
            registration.action_set_done()

    def finish_responsible_courses(self):
        for event in self:
            partner_ids = self.env["res.partner"].search(
                [
                    (
                        "id",
                        "in",
                        [
                            event.user_id.partner_id.id,
                            event.main_responsible_id.partner_id.id,
                            event.second_responsible_id.partner_id.id,
                        ],
                    )
                ]
            )
            event.finish_event_participant_course(partner_ids)

    def finish_event_participant_course(self, partner_ids):
        self.ensure_one()
        if partner_ids:
            partner_courses = self.env["slide.channel.partner"].search(
                [
                    ("event_id", "=", False),
                    ("partner_id", "in", partner_ids.ids),
                    ("channel_id", "in", self.slides_ids.ids),
                ]
            )
            for course in partner_courses:
                course.update({"real_date_end": self.date_end.date()})


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    sequence = fields.Integer(string="Sequence", default=10)
