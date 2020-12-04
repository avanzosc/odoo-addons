
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalStock(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalStock, self)._prepare_portal_layout_values()
        Catalog = request.env['product.catalog.web']
        values.update({
            'catalog_ids': Catalog.search([]),
            'catalog_count': Catalog.search_count([]),
            'page_name': 'catalog',
        })
        return values

    @http.route(['/my/catalog', '/my/catalog/<int:catalog_id>'],
                type='http', auth="user", website=True)
    def portal_my_catalogs(self, catalog_id=None, page=1, access_token=None,
                        report_type=None, message=False, download=False, **kw):
        # Prepare values
        values = self._prepare_portal_layout_values()
        Catalog = request.env['product.catalog.web']
        filtered_catalogs = self.filter_data([], 'product.catalog.web', **kw)
        filtered_catalog_ids = []
        domain = [('id', 'in', filtered_catalog_ids)]
        catalog_count = Catalog.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/catalog",
            total=catalog_count,
            page=page,
            step=self._items_per_page
        )
        pager = self.recalculatePager(pager, **kw)
        catalogs = Catalog.sudo().search(
            domain, limit=self._items_per_page,
            offset=pager['offset'])

        values.update({
            'pager': pager,
            'default_url': '/my/stock',
            'stock_picking_ids': catalogs
          })
        return request.render("website_catalog.portal_my_catalog", values)

    @http.route(['/my/catalog/<int:catalog_id>'],
                type='http', auth="user", website=True)
    def portal_my_catalog(self, catalog_id=None, access_token=None,
                        report_type=None, message=False, download=False, **kw):
        values = self._prepare_portal_layout_values()
        catalog = request.env['product.catalog.web'].get(catalog_id)
        values.update({
            'default_url': '/my/stock',
            'catalog': catalog
        })
        return request.render("website_catalog.portal_catalog", values)
