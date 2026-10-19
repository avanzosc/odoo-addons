from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    latitude_dms = fields.Char(
        string="Latitude (DMS)",
        compute="_compute_latitude_dms",
        store=True,
    )

    longitude_dms = fields.Char(
        string="Longitude (DMS)",
        compute="_compute_longitude_dms",
        store=True,
    )

    def _get_raw_value_from_geolocation(self, dd):
        d = int(dd)
        m = int((dd - d) * 60)
        s = (dd - d - m / 60) * 3600.0
        z = round(s, 2)
        return "%sº %s' %s\"" % (abs(d), abs(m), abs(z))

    def _get_latitude_raw_value(self, dd):
        return "%s %s" % (
            "N" if int(dd) >= 0 else "S",
            self._get_raw_value_from_geolocation(dd),
        )

    def _get_longitude_raw_value(self, dd):
        return "%s %s" % (
            "E" if int(dd) >= 0 else "W",
            self._get_raw_value_from_geolocation(dd),
        )

    @api.depends("partner_latitude")
    def _compute_latitude_dms(self):
        for partner in self:
            partner.latitude_dms = (
                partner.partner_latitude
                and self._get_latitude_raw_value(partner.partner_latitude)
            )

    @api.depends("partner_longitude")
    def _compute_longitude_dms(self):
        for partner in self:
            partner.longitude_dms = (
                partner.partner_longitude
                and self._get_longitude_raw_value(partner.partner_longitude)
            )
