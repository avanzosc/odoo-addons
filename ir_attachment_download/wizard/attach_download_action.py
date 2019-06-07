# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class AttachDownloadAction(models.Model):
    _name = "attach.download.action"

    name = fields.Char(string="Action Name")
    model_id = fields.Many2one(comodel_name="ir.model")
    attach_fields = fields.Many2many(comodel_name="ir.model.fields")
    select_field = fields.Boolean(string="Select Field")
    binary_fields = fields.Boolean(string="Binary Fields")

    @api.model
    def default_get(self, fields):
        res = super(AttachDownloadAction, self).default_get(fields)
        model = self.env['ir.model'].browse(
            self._context.get('active_id'))
        res.update({
            'model_id': model.id,
            'binary_fields': model.field_id.filtered(
                lambda x: x.ttype == 'binary') and True or False
        })
        return res

    @api.multi
    def create_action_server(self):
        self.ensure_one()
        if self.select_field:
            code = ("if object:\n"
                    "    action = object.env["
                    "'ir.attachment']._generate_zip_from_attachments("
                    "object._model, context.get('active_ids', []), "
                    "att_fields=%s)" % str(self.attach_fields._ids))
        else:
            code = ("if object:\n"
                    "    action = object.env["
                    "'ir.attachment']._generate_zip_from_attachments("
                    "object._model, context.get('active_ids', []))")
        action = self.env['ir.actions.server'].create({
            "name": self.name,
            "model_id": self.model_id.id,
            "state": "code",
            "condition": True,
            "code": code,
        })
        self.env['ir.values'].create({
            'name': self.name,
            'model': self.model_id.model,
            'key': "action",
            'key2': "client_action_multi",
            'value': 'ir.actions.server,%d' % action.id
        })
