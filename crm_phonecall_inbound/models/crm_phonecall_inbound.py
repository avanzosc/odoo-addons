# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class CrmPhonecallInbound(models.Model):
    _name = 'crm.phonecall.inbound'
    _description = 'Phone call inbound'

    phonecall_ids = fields.One2many(
        string='Phone calls', comodel_name='crm.phonecall.times',
        inverse_name='phonecall_inbound_id')
    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="Sales Team",
        index=True,
        help="Sales team to which Case belongs to.")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    description = fields.Text()
    state = fields.Selection(
        [
            ("open", "Confirmed"),
            ("cancel", "Cancelled"),
            ("pending", "Pending"),
            ("done", "Held"),
        ],
        string="Status",
        tracking=3,
        default="open",
        help="The status is set to Confirmed, when a case is created.\n"
        "When the call is over, the status is set to Held.\n"
        "If the call is not applicable anymore, the status can be set "
        "to Cancelled.",
    )
    email_from = fields.Char(
        string="Email", help="These people will receive email.")
    name = fields.Char(string="Call Summary", required=True)
    active = fields.Boolean(required=False, default=True)
    partner_phone = fields.Char(string="Phone")
    partner_mobile = fields.Char("Mobile")
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High")],
        string="Priority",
        default="1",
    )
    opportunity_id = fields.Many2one(
        comodel_name="crm.lead", string="Lead/Opportunity")
    direction = fields.Selection(
        [("in", "In"), ("out", "Out")], default="in", required=True
    )
    show_init_call = fields.Boolean(
        string='Show init call button', compute='_compute_show_init_call')

    def _compute_show_init_call(self):
        for inbound in self:
            if not inbound.phonecall_ids:
                inbound.show_init_call = True
            else:
                found = inbound.phonecall_ids.filtered(
                    lambda x: not x.date_closed)
                if found:
                    inbound.show_init_call = False
                else:
                    inbound.show_init_call = True

    @api.onchange("partner_id")
    def on_change_partner_id(self):
        """Contact number details should be change based on partner."""
        if self.partner_id:
            self.partner_phone = self.partner_id.phone
            self.partner_mobile = self.partner_id.mobile

    def action_button_initiate_call(self):
        initiate_call_vals = {
            'phonecall_inbound_id': self.id,
            "date_open": fields.Datetime.now(),
            "duration": '0:00:00'}
        return self.env['crm.phonecall.times'].create(initiate_call_vals)

    def action_button_end_call(self):
        line = self.phonecall_ids.filtered(lambda x: not x.date_closed)
        if line:
            line.write({'date_closed': fields.Datetime.now()})

    def create_lead_opportunity(self):
        vals = {'name': self.name,
                'description': self.description,
                'team_id': self.team_id,
                'priority': self.priority}
        if self.partner_id:
            vals.update({'partner_id': self.partner_id.id,
                         'phone': self.partner_phone,
                         'mobile': self.partner_mobile,
                         'email_from': self.partner_id.email,
                         'type': 'opportunity'})
        if not self.partner_id:
            vals['type'] = 'lead'
        lead_oppor = self.env['crm.lead'].create(vals)
        self.opportunity_id = lead_oppor.id
