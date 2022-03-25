# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SlideChannelTagCourse(models.Model):
    _name = 'slide.channel.tag.course'
    _description = 'Courses of Training itinerary'
    _order = 'tag_group_sequence, tag_sequence, sequence, slide_channel_name'
    _inherit='website.published.mixin'

    tag_sequence = fields.Integer(
        string='Sequence', related='slide_channel_tag_id.sequence')
    tag_group_sequence = fields.Integer(
        'Group sequence', related='slide_channel_tag_id.group_sequence',
        store=True)
    slide_channel_tag_id = fields.Many2one(
        string='Slide channel tag', comodel_name='slide.channel.tag')
    sequence = fields.Integer(string='Sequence', default=10)
    slide_channel_id = fields.Many2one(
        string='Course', comodel_name='slide.channel')
    slide_channel_name = fields.Char(
        string='Course name', related='slide_channel_id.name', store=True)
    technology_category_id = fields.Many2one(
        string='Technology category', store=True,
        comodel_name='slide.channel.technology.category',
        related='slide_channel_id.technology_category_id')
    technology_id = fields.Many2one(
        string='Technology', comodel_name='slide.channel.technology',
        related='slide_channel_id.technology_id', store=True)
    technology_description = fields.Text(
        string='Technology description', store=True,
        related='slide_channel_id.technology_description')
    website_url = fields.Char(
        string='Website URL', related='slide_channel_id.website_url')
