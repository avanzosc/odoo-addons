from odoo import api, fields, models


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        related="create_uid.company_id",
    )

    @api.model
    def create(self, vals):
        res = super(SlideChannelPartner, self).create(vals)
        res._create_slide_channel_survey()
        return res

    def _create_slide_channel_survey(self):
        for record in self:
            slide_channel = record.channel_id
            slide_slides = slide_channel.slide_ids
            for slide in slide_slides.filtered(
                lambda s: s.slide_type == "certification" and s.by_tutor
            ):
                survey_inputs = self.env["survey.user_input"].search(
                    [
                        ("survey_id", "=", slide.survey_id.id),
                        ("event_id", "=", record.event_id.id),
                        "|",
                        ("partner_id", "=", record.partner_id.id),
                        ("student_id", "=", record.partner_id.id),
                    ]
                )
                if not survey_inputs:
                    main_responsible = (
                        record.event_id.main_responsible_id
                        if record.event_id.main_responsible_id
                        else record.event_id.second_responsible_id
                    )
                    array_m = [
                        record.event_id.main_responsible_id.partner_id.id,
                        record.event_id.second_responsible_id.partner_id.id,
                        slide_channel.user_id.partner_id.id,
                    ]
                    if record.partner_id == 1:
                        print('A')
                    if record.partner_id.id not in array_m:
                        survey_input = self.env["survey.user_input"].create(
                            {
                                "survey_id": slide.survey_id.id,
                                "event_id": record.event_id.id,
                                "student_id": record.partner_id.id,
                                "partner_id": main_responsible.partner_id.id
                                if main_responsible
                                else None,
                            }
                        )
