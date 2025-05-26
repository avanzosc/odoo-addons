import logging

from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):
    @route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        res = super().home(**kw)
        user_id = request.env["res.users"].browse(request.uid)
        allowed_urls = user_id.company_id.portal_custom_entry_show
        _logger.info("Allowed URLs: %s", allowed_urls.mapped("url"))

        urls = request.env["ir.model.url"].sudo().search([])
        _logger.info("Found ir.model.url records: %s", urls)

        saca_url_count_info = []

        for doc in urls:
            model_name = doc.ir_model_id.model
            _logger.info("Processing doc ID %s with model %s", doc.id, model_name)

            if model_name:
                line_field = (
                    "line_ids"
                    if model_name == "saca"
                    else "order_line"
                    if model_name in ("sale.order", "purchase.order")
                    else "invoice_line_ids"
                    if model_name == "account.move"
                    else None
                )
                record = (
                    request.env[model_name]
                    .sudo()
                    .search([("id", "=", doc.res_id)], limit=1)
                    if hasattr(doc, "res_id")
                    else request.env[model_name].sudo().search([], limit=1)
                )
                _logger.info("Record found for model %s: %s", model_name, record)

                if (
                    record
                    and line_field
                    and hasattr(record, line_field)
                    and record[line_field]
                ):
                    saca_url_count_info.append(
                        {
                            "id": doc.id,
                            "title": doc.name,
                            "url": doc.url,
                            "count": len(record[line_field]),
                        }
                    )
                    _logger.info(
                        "Added doc to saca_url_count_info: %s", saca_url_count_info[-1]
                    )
                else:
                    _logger.debug(
                        "Skipped doc ID %s: No record, no %s, or empty lines",
                        doc.id,
                        line_field,
                    )

        _logger.info("Final saca_url_count_info: %s", saca_url_count_info)

        visible_urls = []
        for info in saca_url_count_info:
            if info["url"] in allowed_urls.mapped("url") and info["count"] > 0:
                visible_urls.append(info["url"])

        visible_urls += [
            url
            for url in allowed_urls.mapped("url")
            if "/saca/" not in url and url not in visible_urls
        ]

        _logger.info("Visible URLs: %s", visible_urls)

        res.qcontext.update(
            {
                "allowed_urls": allowed_urls.mapped("url"),
                "saca_url_count_info": saca_url_count_info,
                "visible_urls": visible_urls,
            }
        )
        _logger.info("Updated qcontext: %s", res.qcontext)

        return res
