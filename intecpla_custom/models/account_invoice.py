# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from datetime import datetime

from pytz import timezone, utc

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def action_invoice_open(self):
        invoices = self.filtered(lambda x: x.type == "in_invoice" and x.reference)
        if invoices:
            for invoice in invoices:
                cond = [
                    ("partner_id", "=", invoice.partner_id.id),
                    ("reference", "=", invoice.reference),
                    ("type", "=", "in_invoice"),
                    ("id", "!=", invoice.id),
                ]
                invs = self.env["account.invoice"].search(cond)
                if invs:
                    for inv in invs:
                        if (
                            inv.date_invoice.year
                            == fields.Date.context_today(self).year
                        ):
                            raise UserError(
                                _(
                                    "The invoice already exists: %s, for the "
                                    "supplier: %s, with supplier reference: %s, "
                                    "and date %s."
                                )
                                % (
                                    inv.number,
                                    inv.partner_id.name,
                                    inv.reference,
                                    inv.date_invoice,
                                )
                            )
        return super().action_invoice_open()

    def action_invoice_draft(self):
        result = True
        for invoice in self:
            if invoice.type in ("in_invoice", "in_refund"):
                result = super(
                    AccountInvoice, self.with_context(no_update_date=True)
                ).action_invoice_draft()
            else:
                result = super().action_invoice_draft()
        return result

    def write(self, vals):
        if "no_catch_notes" in self.env.context:
            vals["comment"] = " "
        if (
            "no_update_date" in self.env.context
            and "date" in vals
            and not vals.get("date")
        ):
            vals.pop("date")
        return super().write(vals)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    sale_order_section = fields.Char(string="Sale order section")
    repair_order_section = fields.Text(string="Repair order section")
    with_sale_order_section = fields.Boolean(
        string="With sale order section", default=False
    )
    with_repair_order_section = fields.Boolean(
        string="With repair order section", default=False
    )

    @api.model
    def create(self, values):
        line_obj = self.env["account.invoice.line"]
        if (
            "create_sale_order_section" not in self.env.context
            and "create_mrp_order_section" not in self.env.context
            and "origin" in values
            and values.get("origin")
            and "sale_line_ids" not in values
        ):
            cond = [("name", "=", values.get("origin"))]
            repair = self.env["repair.order"].search(cond, limit=1)
            if repair:
                date_repair = self._convert_to_local_date(
                    repair.date_repair, repair.user_id
                )
                repair_order_section = "Repair: {}, date: {}\n".format(
                    repair.name, date_repair
                )
                values["repair_order_section"] = repair_order_section
                my_origin = values.get("origin")
                cond = [
                    ("repair_order_section", "=", repair_order_section),
                    ("origin", "=", my_origin),
                    ("invoice_id", "=", values.get("invoice_id")),
                ]
                my_line = line_obj.search(cond)
                if not my_line:
                    values = line_obj.create_line_with_repair_order_info(
                        repair, repair_order_section, my_origin, values
                    )
        if (
            "create_sale_order_section" not in self.env.context
            and "create_mrp_order_section" not in self.env.context
            and "origin" in values
            and values.get("origin")
            and "sale_line_ids" in values
        ):
            cond = [("name", "=", values.get("origin"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale:
                sale_date = self._convert_to_local_date(sale.date_order, sale.user_id)
                sale_order_section = "Order: {}, date: {}\n".format(
                    sale.name, sale_date
                )
                values["sale_order_section"] = sale_order_section
                my_origin = values.get("origin")
                cond = [
                    ("sale_order_section", "=", sale_order_section),
                    ("origin", "=", my_origin),
                    ("invoice_id", "=", values.get("invoice_id")),
                ]
                my_line = line_obj.search(cond)
                if not my_line:
                    values = line_obj.create_line_with_sale_order_info(
                        sale, sale_order_section, my_origin, values
                    )
        if "invoice_id" in values and values.get("invoice_id", False):
            cond = [("invoice_id", "=", values.get("invoice_id"))]
            my_line = self.search(cond)
            if not my_line:
                values["sequence"] = 10
            else:
                my_sequence = 0
                for line in my_line:
                    if line.sequence > my_sequence:
                        my_sequence = line.sequence
                my_sequence += 10
                values["sequence"] = my_sequence
        line = super().create(values)
        return line

    def create_line_with_sale_order_info(
        self, sale, sale_order_section, my_origin, values
    ):
        sale_date = self._convert_to_local_date(sale.date_order, sale.user_id)
        my_name = _("Order: {}, date: {}").format(sale.name, sale_date)
        cond = [("invoice_id", "=", values.get("invoice_id"))]
        my_line = self.search(cond)
        if not my_line:
            vals = {
                "name": my_name,
                "sale_order_section": sale_order_section,
                "with_sale_order_section": True,
                "sequence": 1,
                "origin": my_origin,
                "display_type": "line_section",
                "invoice_id": values.get("invoice_id"),
                "sale_line_ids": values.get("sale_line_ids"),
            }
            self.with_context(create_sale_order_section=True).create(vals)
            values["sequence"] = 2
            return values
        my_sequence = 0
        for line in my_line:
            if line.sequence > my_sequence:
                my_sequence = line.sequence
        my_sequence += 1
        vals = {
            "name": my_name,
            "sale_order_section": sale_order_section,
            "with_sale_order_section": True,
            "sequence": my_sequence,
            "origin": my_origin,
            "display_type": "line_section",
            "invoice_id": values.get("invoice_id"),
            "sale_line_ids": values.get("sale_line_ids"),
        }
        self.with_context(create_sale_order_section=True).create(vals)
        my_sequence += 1
        values["sequence"] = my_sequence
        return values

    def create_line_with_repair_order_info(
        self, repair, repair_order_section, my_origin, values
    ):
        date_repair = self._convert_to_local_date(repair.date_repair, repair.user_id)
        my_name = _("Repair: {}, date: {}").format(repair.name, date_repair)
        cond = [("invoice_id", "=", values.get("invoice_id"))]
        my_line = self.search(cond)
        if not my_line:
            vals = {
                "name": my_name,
                "repair_order_section": repair_order_section,
                "with_repair_order_section": True,
                "sequence": 1,
                "origin": my_origin,
                "display_type": "line_section",
                "invoice_id": values.get("invoice_id"),
            }
            notes = ""
            if repair.internal_notes:
                notes = _("Notes: {}").format(repair.internal_notes)
            if repair.quotation_notes:
                if not notes:
                    notes = _("Notes: {}").format(repair.quotation_notes)
                else:
                    notes = "{}\n{}".format(notes, repair.quotation_notes)
            if notes:
                vals["name"] = "{}\n{}".format(my_name, notes)
            self.with_context(create_mrp_order_section=True).create(vals)
            values["sequence"] = 2
            return values
        my_sequence = 0
        for line in my_line:
            if line.sequence > my_sequence:
                my_sequence = line.sequence
        my_sequence += 1
        vals = {
            "name": my_name,
            "repair_order_section": repair_order_section,
            "with_repair_order_section": True,
            "sequence": my_sequence,
            "origin": my_origin,
            "display_type": "line_section",
            "invoice_id": values.get("invoice_id"),
        }
        notes = ""
        if repair.internal_notes:
            notes = _("Notes: {}").format(repair.internal_notes)
        if repair.quotation_notes:
            if not notes:
                notes = _("Notes: {}").format(repair.quotation_notes)
            else:
                notes = "{}\n{}".format(notes, repair.quotation_notes)
        if notes:
            vals["name"] = "{}\n{}".format(my_name, notes)
        self.with_context(create_mrp_order_section=True).create(vals)
        my_sequence += 1
        values["sequence"] = my_sequence
        return values

    def _ir_cron_fix_sale_order_section(self):
        cond = [
            ("sale_order_section", "ilike", "%Order: %date: %"),
            ("invoice_id.origin", "!=", False),
        ]
        lines = self.search(cond)
        for line in lines:
            cond = [("name", "=", line.invoice_id.origin)]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale:
                sale_date = self._convert_to_local_date(sale.date_order, sale.user_id)
                sale_order_section = _("Order: {}, date: {}").format(
                    sale.name, sale_date
                )
                if line.sale_order_section != sale_order_section:
                    old_sale_section = line.sale_order_section
                    line.sale_order_section = sale_order_section
                    cond = [
                        ("invoice_id", "=", line.invoice_id.id),
                        ("name", "=", old_sale_section),
                    ]
                    section_line = self.search(cond, limit=1)
                    if not section_line:
                        old_sale_section = old_sale_section.replace("Order:", "Pedido:")
                        old_sale_section = old_sale_section.replace("date:", "fecha:")
                        cond = [
                            ("invoice_id", "=", line.invoice_id.id),
                            ("name", "=", old_sale_section),
                        ]
                        section_line = self.search(cond, limit=1)
                        if not section_line:
                            old_sale_section = old_sale_section.replace("\n", "")
                            cond = [
                                ("invoice_id", "=", line.invoice_id.id),
                                ("name", "=", old_sale_section),
                            ]
                            section_line = self.search(cond, limit=1)
                    if section_line:
                        section_line.name = sale_order_section
        cond = [
            ("repair_order_section", "ilike", "%Repair: %date: %"),
            ("invoice_id.origin", "!=", False),
        ]
        lines = self.search(cond)
        modificados1 = 0
        modificados2 = 0
        for line in lines:
            cond = [("name", "=", line.invoice_id.origin)]
            repair = self.env["repair.order"].search(cond, limit=1)
            if repair:
                date_repair = self._convert_to_local_date(
                    repair.date_repair, repair.user_id
                )
                repair_order_section = _("Repair: {}, date: {}").format(
                    repair.name, date_repair
                )
                if line.repair_order_section != repair_order_section:
                    modificados1 += 1
                    old_repair_section = line.repair_order_section
                    line.repair_order_section = repair_order_section
                    cond = [
                        ("invoice_id", "=", line.invoice_id.id),
                        ("name", "=", old_repair_section),
                    ]
                    section_line = self.search(cond, limit=1)
                    if not section_line:
                        old_repair_section = old_repair_section.replace(
                            "Repair:", "Reparación:"
                        )
                        old_repair_section = old_repair_section.replace(
                            "date:", "fecha:"
                        )
                        cond = [
                            ("invoice_id", "=", line.invoice_id.id),
                            ("name", "=", old_repair_section),
                        ]
                        section_line = self.search(cond, limit=1)
                        if not section_line:
                            old_repair_section = old_repair_section.replace("\n", "")
                            cond = [
                                ("invoice_id", "=", line.invoice_id.id),
                                ("name", "=", old_repair_section),
                            ]
                            section_line = self.search(cond, limit=1)
                    if section_line:
                        modificados2 += 1
                        section_line.name = repair_order_section

    def _convert_to_local_date(self, mydate, user):
        if not mydate:
            return ""
        tz = user.tz if user.tz else self.env.user.tz
        mydate = mydate.replace(tzinfo=utc)
        mydate = mydate.astimezone(timezone(tz)).replace(tzinfo=None)
        return datetime.strptime(str(mydate), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")
