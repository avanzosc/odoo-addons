# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from markupsafe import Markup, escape

from odoo import _, api, models


class Contact(models.AbstractModel):
    _inherit = "ir.qweb.field.contact"

    @api.model
    def get_available_options(self):
        options = super().get_available_options()
        contact_fields = options.get("fields")
        contact_fields.add({"field_name": "eori", "label": _("EORI Number")})
        options.update(
            fields=dict(
                type="array",
                params=dict(type="selection", params=contact_fields),
                string=_("Displayed fields"),
                description=_("List of contact fields to display in the widget"),
                default_value=[
                    param.get("field_name")
                    for param in contact_fields
                    if param.get("default")
                ],
            ),
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        if not value:
            return ""

        opf = options.get("fields") or ["name", "address", "phone", "mobile", "email"]
        if "eori" not in opf:
            return super().value_to_html(value, options)

        sep = options.get("separator")
        if sep:
            opsep = escape(sep)
        elif options.get("no_tag_br"):
            # escaped joiners will auto-escape joined params
            opsep = escape(", ")
        else:
            opsep = Markup("<br/>")

        value = value.sudo().with_context(show_address=True)
        name_get = value.name_get()[0][1]
        # Avoid having something like:
        # name_get = 'Foo\n  \n' -> This is a res.partner with a name and no address
        # That would return markup('<br/>') as address. But there is no address set.
        if any(elem.strip() for elem in name_get.split("\n")[1:]):
            address = opsep.join(name_get.split("\n")[1:]).strip()
        else:
            address = ""
        val = {
            "name": name_get.split("\n")[0],
            "address": address,
            "phone": value.phone,
            "mobile": value.mobile,
            "city": value.city,
            "country_id": value.country_id.display_name,
            "website": value.website,
            "email": value.email,
            "vat": value.vat,
            "vat_label": value.country_id.vat_label or _("VAT"),
            "eori": value.eori_code,
            "fields": opf,
            "object": value,
            "options": options,
        }
        return self.env["ir.qweb"]._render("base.contact", val, minimal_qcontext=True)
