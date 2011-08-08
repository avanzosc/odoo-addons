# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#                       NaN Projectes de Programari Lliure, S.L. (http://www.nan-tic.com)
#                       Ana Juaristi, Avanzosc, S.L. <ajuaristio@gmail.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import netsvc
from osv import fields,osv,orm
import ir
import time
import xmlrpclib
from mx import DateTime
from tools.translate import _
import unicodedata

def unaccent(text):
    if isinstance( text, str ):
        text = unicode( text, 'utf-8' )
    elif isinstance(text, unicode):
        pass
    else:
        return str(text)
    return unicodedata.normalize('NFKD', text ).encode('ASCII', 'ignore')

class esale_oscom_web(osv.osv):
    _name = 'esale.oscom.web'
esale_oscom_web()


class esale_oscom_tax(osv.osv):
    _name = "esale.oscom.tax"
    _description = "esale_oscom Tax"
    _columns = {
        'name': fields.char('Tax name', size=32, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce Id'),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'tax_id': fields.many2one('account.tax', 'OpenERP tax'),
    }
esale_oscom_tax()


class esale_oscom_status(osv.osv):
    _name = "esale.oscom.status"
    _description = "esale_oscom Status"
    _columns = {
        'name': fields.char('Status name', size=32, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce Id'),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'language_id': fields.integer('Language Id'),
        'download': fields.boolean('Download Orders on Status'),
    }
esale_oscom_status()


class esale_oscom_category(osv.osv):
    _name = "esale.oscom.category"
    _description = "esale_oscom Category"
    _columns = {
        'name': fields.char('Name', size=64, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce Id', required=True),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'category_id': fields.many2one('product.category', 'OpenERP category'),
    }
esale_oscom_category()


class esale_oscom_paytype(osv.osv):
    _name = "esale.oscom.paytype"
    _description = "esale_oscom PayType"
    _columns = {
        'name': fields.char('Name', size=64, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce Id', required=True),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'payment_id': fields.many2one('payment.type', 'OpenERP payment'),
        'paytyp': fields.selection([('type1','SO in State Draft'),('type2','SO Confirmed'),('type3','Invoice Draft'),('type4','Invoice Confirmed'),('type5','Invoice Payed')], 'Payment type'),
        'journal_id': fields.many2one('account.journal', 'OpenERP payment journal'),
        'product_id': fields.many2one( 'product.product', 'OpenERP product associated' ),
    }
esale_oscom_paytype()


class esale_oscom_language(osv.osv):
    _name = "esale.oscom.lang"
    _description = "esale_oscom Language"
    _columns = {
        'name': fields.char('Name', size=32, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce Id', required=True),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'language_id': fields.many2one('res.lang', 'OpenERP language'),
    }
esale_oscom_language()


class esale_oscom_product(osv.osv):
    _name = "esale.oscom.product"
    _description = "esale_oscom Product"
    _columns = {
        'name': fields.char('Name', size=64, required=True, readonly=True),
        'esale_oscom_id': fields.integer('OScommerce product Id'),
        'web_id': fields.many2one('esale.oscom.web', 'Website'),
        'product_id': fields.many2one('product.product', 'OpenERP product'),
    }

    def onchange_product_id(self, cr, uid, ids, product_id, web_id):
        value = {}
        if (product_id):
            product = self.pool.get('product.product').browse(cr, uid, product_id)
            value['name'] = product.name
        return {'value': value}

    def unlink(self, cr, uid, ids, context=None):
        websites = {}
        for esale_product in self.browse(cr, uid, ids):
            web_product_ids = websites.get(esale_product.web_id and esale_product.web_id.id)
            if web_product_ids and len(web_product_ids):
                web_product_ids.append(esale_product.esale_oscom_id)
            else:
                websites[esale_product.web_id and esale_product.web_id.id] = [esale_product.esale_oscom_id]
        websites_objs = self.pool.get('esale.oscom.web').browse(cr, uid, [x for x in websites.keys() if type(x) is int])
        for website in websites_objs:
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            server.remove_product({'oscom_product_ids':websites.get(website.id)})
        return super(esale_oscom_product,self).unlink(cr, uid, ids, context)
esale_oscom_product()

class esale_oscom_carrier( osv.osv ):
    _name = "esale.oscom.carrier"
    _description = "esale_oscom Delivery Carrier"
    _columns = {
        'name': fields.char( 'Name', size=64, required=True ),
        'esale_oscom_id': fields.integer( 'OScommerce Id', required=True ),
        'web_id': fields.many2one( 'esale.oscom.web', 'Website' ),
        'carrier_id': fields.many2one( 'delivery.carrier', 'OpenERP Delivery Carrier' ),
        'product_id': fields.many2one( 'product.product', 'OpenERP product', help="OpenERP product associated to this type of delivery." ),
    }

esale_oscom_carrier()

class esale_oscom_web(osv.osv):
    _name = "esale.oscom.web"
    _description = "OScommerce Website"
    _columns = {
        'name': fields.char('Name',size=64, required=True),
        'url': fields.char('URL', size=128, required=True),
        'shop_id': fields.many2one('sale.shop', 'Sale shop', required=True),
#        'partner_anonymous_id': fields.many2one('res.partner', 'Anonymous', required=True),
        'active': fields.boolean('Active'),
        'product_ids': fields.one2many('esale.oscom.product', 'web_id', 'Web products'),
        'language_ids': fields.one2many('esale.oscom.lang', 'web_id', 'Languages'),
        'tax_ids': fields.one2many('esale.oscom.tax', 'web_id', 'Taxes'),
        'category_ids': fields.one2many('esale.oscom.category', 'web_id', 'Categories'),
        'pay_typ_ids': fields.one2many('esale.oscom.paytype', 'web_id', 'Payment types'),
        'status_ids': fields.one2many('esale.oscom.status', 'web_id', 'Osc Status'),
        'delivery_carrier_ids': fields.one2many( 'esale.oscom.carrier', 'web_id', 'Delivery Carrier' ),
        'esale_account_id': fields.many2one('account.account', 'Dest. account', required=True, help="Payment account for web invoices."),
        'price_type': fields.selection([('0', 'Untaxed price'), ('1', 'Taxed price')], 'Price type', required=True),
        'date_download_from':fields.date('Date Download From', help="Specify date since you want to download modified or new products"),
        'intermediate': fields.many2one('esale.oscom.status', 'Intermediate Status', help="Select intermediate status for Osc downloaded Orders"), 
        'download_number': fields.integer('Download number', help="Osc product number to download by block. You should find the optimum block to download for your shop"),
    }
    _defaults = {
        'active': lambda *a: 1,
        'price_type': lambda *a:'0',  
        'download_number': lambda *a:30,
    }

    def add_all_products(self, cr, uid, ids, *args):
        esale_product_obj = self.pool.get('esale.oscom.product')
        for id in ids:
            cr.execute("select p.id from product_product as p left join esale_oscom_product as o on p.id=o.product_id and o.web_id=%d where o.id is NULL;" % id)
            for [product] in cr.fetchall():
                value = {
                    'product_id' : product,
                    'web_id' : id
                }
                value.update(esale_product_obj.onchange_product_id(cr, uid, [], product, id)['value'])
                esale_product_obj.create(cr, uid, value)
        return True


    def tax_import(self, cr, uid, ids, *args):
        esale_tax_obj = self.pool.get('esale.oscom.tax')
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            taxes = server.get_taxes()
            for tax in taxes:
                update_taxes_ids = esale_tax_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',tax[0])])
                if len(update_taxes_ids):
                    esale_tax_obj.write(cr, uid, update_taxes_ids, {'name': tax[1]})
                else:
                    value = {
                        'web_id' : website.id,
                        'esale_oscom_id' : tax[0],
                        'name' : tax[1]
                    }
                    esale_tax_obj.create(cr, uid, value)
        return True

    def status_import(self, cr, uid, ids, *args):
        esale_status_obj = self.pool.get('esale.oscom.status')
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            statuses = server.get_statuses()
            for status in statuses:
                update_statuses_ids = esale_status_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',status[0])])
                if len(update_statuses_ids):
                    esale_status_obj.write(cr, uid, update_statuses_ids, {'name': status[1]})
                else:
                    value = {
                        'web_id' : website.id,
                        'esale_oscom_id' : status[0],
                        'name' : status[1],
                        'language_id': status[2],
                        'download': 0
                    }
                    esale_status_obj.create(cr, uid, value)
        return True


    def lang_import(self, cr, uid, ids, *args):
        esale_lang_obj = self.pool.get('esale.oscom.lang')
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            languages = server.get_languages()
            for language in languages:
                update_language_ids = esale_lang_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',language[0])])
                if len(update_language_ids):
                    esale_lang_obj.write(cr, uid, update_language_ids, {'name': language[1]})
                else:
                    value = {
                        'web_id' : website.id,
                        'esale_oscom_id' : language[0],
                        'name' : language[1]
                    }
                    esale_lang_obj.create(cr, uid, value)
        return True


    def get_payment_methods(self, cr, uid, ids, *args):
        esale_paytype_obj = self.pool.get('esale.oscom.paytype')
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            payment_methods = server.get_payment_methods()
            for payment_method in payment_methods:
                value={
                    'web_id' : website.id,
                    'esale_oscom_id' : payment_method[0],
                    'name' : payment_method[1]
                }
                existing = esale_paytype_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id', '=', payment_method[0])])
                if len(existing) > 0:
                    esale_paytype_obj.write(cr, uid, existing, value)
                else:
                    esale_paytype_obj.create(cr, uid, value)
        return True

    def get_shipping_methods( self, cr, uid, ids, *args ):
        esale_carrier_obj = self.pool.get( 'esale.oscom.carrier' )
        for website in self.browse( cr, uid, ids ):
            server = xmlrpclib.ServerProxy( "%s/openerp-synchro.php" % website.url )
            delivery_carriers = server.get_shipping_methods()
            for delivery_carrier in delivery_carriers:
                value = {
                    'web_id' : website.id,
                    'esale_oscom_id' : delivery_carrier[ 0 ],
                    'name' : delivery_carrier[ 1 ]
                }
                existing = esale_carrier_obj.search( cr, uid, [ ( 'web_id', '=', website.id ), ( 'esale_oscom_id', '=', delivery_carrier[ 0 ] ) ] )
                if len( existing ) > 0:
                    esale_carrier_obj.write( cr, uid, existing, value )
                else:
                    esale_carrier_obj.create( cr, uid, value )
        return True

    def category_import(self, cr, uid, ids, *args):
        """Imports product categories from OSCommerce"""
        esale_category_obj = self.pool.get('esale.oscom.category')
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            categories = server.get_categories()
            for category in categories:
                value = {
                    'web_id' : website.id,
                    'esale_oscom_id' : category[0],
                    'name' : category[1]
                }
                existing = esale_category_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id', '=', category[0])])
                if len(existing) > 0:
                    esale_category_obj.write(cr, uid, existing, value)
                else:
                    esale_category_obj.create(cr, uid, value)
        return True

    def category_import_create(self, cr, uid, ids, *args):
        """Imports product categories from OSCommerce and creates/updates OpenERP product categories"""
        category_obj = self.pool.get('product.category')
        esale_category_obj = self.pool.get('esale.oscom.category')

        created, updated = 0,0
        for website in self.browse(cr, uid, ids):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)

            # Search OScommerce languages mapped to OpenERP
            osc_langs = [lang.esale_oscom_id for lang in website.language_ids if lang.language_id and lang.language_id.translatable]
            oerp_langs = [lang.language_id for lang in website.language_ids if lang.language_id and lang.language_id.translatable]
            if not osc_langs:
                raise osv.except_osv(_('Warning'), _("First you must map OScommerce languages to OpenERP languages in the Web Shop!"))
            print "idiomas a descargar", osc_langs
            categories = server.get_categories_parent(osc_langs)
            for category in categories:
                # Search in intermediate esale.oscom.category object that maps OScommerce and OpenERP categories
                print "TRATANDO CATEGORIA", category
                cat_oscom_id = esale_category_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',category[0])])
                if cat_oscom_id:
                    cat_oscom = esale_category_obj.browse(cr, uid, cat_oscom_id)[0]
                if category[1]: # Has a parent category
                    cat_oscom_p_id = esale_category_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',category[1])])
                    if not cat_oscom_p_id:
                        raise osv.except_osv(_('Import Error'), _('Category %s (%s) has parent %s in osCommerce, but no mapping was found for it in OpenERP') % (category[0], category[2], category[1]) )
                    cat_oscom_p = esale_category_obj.browse(cr, uid, cat_oscom_p_id)[0]

                # Creates or updates product.category and esale.oscom.category objects
                if len(category) >= 3:
                    cat_nombre = category[2]
                else:
                    cat_nombre = 'SIN NOMBRE'
                value = {
                    'name' : cat_nombre,
                    'parent_id': category[1] and cat_oscom_p.category_id.id or False
                }
                if not cat_oscom_id or not cat_oscom.category_id: # OpenERP category does not exist
                    cat_id = category_obj.create(cr, uid, value)
                    created += 1
                    value_cat_oscom = {
                        'web_id' : website.id,
                        'esale_oscom_id' : category[0],
                        'name' : cat_nombre,
                        'category_id' : cat_id,
                    }
                    if not cat_oscom_id:
                        cat_oscom_id = esale_category_obj.create(cr, uid, value_cat_oscom)
                    else:
                        esale_category_obj.write(cr, uid, cat_oscom_id, value_cat_oscom)
                else:  # OpenERP category exists
                    cat_id = cat_oscom.category_id.id
                    category_obj.write(cr, uid, cat_id, value)
                    updated += 1

                # Updates translations
                for trans, lang in zip(category[2:], oerp_langs):
                    ##print trans, lang.code
                    category_obj.write(cr, uid, cat_id, {'name': trans}, {'lang': lang.code})

            cr.commit()
            raise osv.except_osv(_('Category import done'), _('Created: %d categories\nUpdated: %d categories\n\nRefresh screen to see updates') % (created, updated))
        return True


    def product_fields(self, info_prod):
        """If you want compute additional product fields you can redefine this method in your own module"""
        vals = {
            #'field_name': info_prod['field_name']
        }
        return vals


    def product_trans_fields(self, trans):
        """If you want compute additional product translated fields you can redefine this method in your own module"""
        vals = {
            #'field_name': trans['field_name']
        }
        return vals

    def variant_import_create(self, cr, uid, website, prod_id, product, esale_product):

        return True

    def product_extra_info_m2m(self, cr, uid, website, prod_id, prod_data):
        """Module to import m2m categories for oscommerce products"""

        return True

    def product_extra_info_extra_fields(self, cr, uid, website, prod_id, prod_data):
        """Module to import extra_fields for oscommerce products"""

        return True


    def product_extra_info_pricelist(self, cr, uid, website, prod_id, prod_data):
        """Module to import product partner pricelists for oscommerce products"""
        return True

    def product_extra_info(self, cr, uid, website, prod_id, prod_data):
        """If you want create additonal information in OpenERP objects related to product you can redefine this method in your own module"""
        return True



    def selected_product_import_create(self, cr, uid, websites, osc_prod_id):
        product_obj = self.pool.get('product.product')
        esale_product_obj = self.pool.get('esale.oscom.product')
        manufacturer_obj = self.pool.get('product.manufacturer')
        stock_inventory_obj = self.pool.get('stock.inventory')
        stock_inventory_line_obj = self.pool.get('stock.inventory.line')            

        print "================================Creando producto unico =========================================="
        print "website", websites
        print "osc_prod_id", osc_prod_id
  
        created, updated = 0,0


        for website in self.browse(cr, uid, websites):
            server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
            website_url = website.url.split("/")
            # Search esale languages mapped to OpenERP
            osc_langs = [lang.esale_oscom_id for lang in website.language_ids if lang.language_id and lang.language_id.translatable]
            if not osc_langs:
                raise osv.except_osv(_('Warning'), _("First you must map OScommerce languages to OpenERP languages in the Web Shop!"))

            # Creates dictionary mapping esale language id -> OpenERP language
            oerp_langs = {}
            for lang in website.language_ids:
                if lang.language_id and lang.language_id.translatable:
                    oerp_langs[lang.esale_oscom_id] = lang.language_id

            # Creates dictionary mapping esale category id -> OpenERP category
            oerp_categs = {}
            for categ in website.category_ids:
                if categ.category_id:
                    oerp_categs[categ.esale_oscom_id] = categ.category_id

            # Creates dictionary mapping esale tax id -> OpenERP tax
            oerp_taxs = {}
            for tax in website.tax_ids:
                if tax.tax_id and tax.tax_id.active:
                    oerp_taxs[tax.esale_oscom_id] = tax.tax_id


            value_stock_inv = {
                'name' : "Descarga Inicial",
            }
            stock_init_id =  stock_inventory_obj.create(cr, uid, value_stock_inv)

            para = 0
            oscom_id = 0
            bloque = website.download_number
            continuar = True
            transaccional = server.isTransactional()
            from_date = website.date_download_from

            if (len(osc_prod_id) > 0):
                from_date = '19900101'
                oscom_id = osc_prod_id[0]
                bloque = len(osc_prod_id)
                para = 1
                #print "from_date", from_date
            
            while (continuar):
                print "osc_langs", osc_langs
                print "oscom_id: ", oscom_id
                print "bloque", bloque
                print "from_date", from_date
                products_osc = server.get_products(osc_langs, oscom_id, bloque, from_date)

                if (len(products_osc) < bloque):
                    continuar = False
                if (para >0):
                    continuar = False
                #print "from_date", from_date

                for product in products_osc:
                    print "================================product from osc=========================================="
                    #print product
                    info_prod = product['product']
                    spec_prod = product['product_special']
                    name_prod = product['product_description'] and product['product_description'][0]['products_name'] or '-'
                    url_manuf = product['manufacturers_url']
                    print info_prod['products_id'], " Code " , info_prod['products_model']
                    oscom_id = info_prod['products_id']
                    # Search mapped category. If not found the product is not added/modified
                    if info_prod['categ_id'] in oerp_categs:
                        categ = oerp_categs[info_prod['categ_id']]
                    else:
                        continue

                    # Search mapped tax
                    tax = []
                    if info_prod['products_tax_class_id'] in oerp_taxs:
                        tax = [(6, 0, [oerp_taxs[info_prod['products_tax_class_id']].id])]

                    # Search manufacturer. If not exists, create it. Create related url for each language
                    manuf_id = ''
                    if (len(info_prod['manufacturers_name']) > 0):
                        print "buscando fabricante" , info_prod['manufacturers_name']
                        manuf_ids = manufacturer_obj.search(cr, uid, [('name','=',info_prod['manufacturers_name'])])
                        if not manuf_ids:
                            print "creando fabricante"
                            manuf_id = manufacturer_obj.create(cr, uid, {'name': info_prod['manufacturers_name']})
                            print "creado fabricante", manuf_id
                        else:
                            manuf_id = manuf_ids[0]
                        for url_manuf_el in url_manuf:
                            if url_manuf_el['languages_id'] in oerp_langs:
                                print url_manuf_el['languages_id'], oerp_langs[url_manuf_el['languages_id']].code
                                manufacturer_obj.write(cr, uid, [manuf_id], {'manufacturer_url': url_manuf_el['manufacturers_url']}, {'lang': oerp_langs[url_manuf_el['languages_id']].code})

                    value = {
                        'name': name_prod,
                        'default_code': info_prod['products_model'],
                        'categ_id': categ.id,
                        'taxes_id': tax,
                        'list_price': info_prod['products_price'],
                        'weight': info_prod['products_weight'],
                        'product_picture': info_prod['products_image'],
                        'in_out_stock': str(info_prod['products_status']),
                        'date_available': info_prod['products_date_available']!='0000-00-00 00:00:00' and info_prod['products_date_available'] or False,
                        'spe_price_status': 'status' in spec_prod and str(spec_prod['status']) or False,
                        'spe_price': 'specials_new_products_price' in spec_prod and spec_prod['specials_new_products_price'] or False,
                        'exp_date': 'expires_date' in spec_prod and spec_prod['expires_date']!='0000-00-00 00:00:00' and spec_prod['expires_date'] or False,
                        'oscom_url': website_url[0] + "//" + website_url[2] + "/" +"product_info.php?cPath=" + str(info_prod['categ_id']) + "&products_id=" + str(info_prod['products_id']),
                        'manufacturer_id': manuf_id or False,
                        #'ean13': info_prod['products_model'],
                        #'type': 'Stockable product',
                        #'supply_method': 'buy',
                        #'procure_method': 'make_to_stock',
                        #'cost_method': 'standard',
                        #'weight_net': info_prod['products_weight'],
                        #'standard_price': info_prod['products_price'],
                    }
                    value.update(self.product_fields(info_prod)) # Adds additional fields
                    print "=======value======"
                    print value

                    # Search in intermediate esale.oscom.product object that maps OScommerce and OpenERP products
                    esale_product_ids = esale_product_obj.search(cr, uid, [('web_id','=',website.id), ('esale_oscom_id','=',info_prod['products_id'])])
                    if esale_product_ids:
                        esale_product = esale_product_obj.browse(cr, uid, esale_product_ids[0])
                        print "De nuevo encontrado: ", esale_product.esale_oscom_id

                    # Creates or updates product.product and esale.oscom.product objects
                    if not esale_product_ids or not esale_product.product_id: # OpenERP product does not exist
                        print "DOES NOT EXIST: ", info_prod['products_id']
                        prod_id = product_obj.create(cr, uid, value)
                        print "creando producto Open: ", prod_id
                        created += 1
                        value_esale_product = {
                                'name': name_prod,
                                'esale_oscom_id': info_prod['products_id'],
                                'web_id': website.id,
                                'product_id': prod_id,
                        }                        
                        if not esale_product_ids:
                            esale_product_id = esale_product_obj.create(cr, uid, value_esale_product)
                            #print "creando producto osc: ", esale_product_id
                            esale_product = esale_product_obj.browse(cr, uid, esale_product_id)
                        else:
                            esale_product_obj.write(cr, uid, [esale_product_ids[0]], value_esale_product)
                            print "Modificando producto osc: ", esale_product_id
                    else: # OpenERP product exists
                        prod_id = esale_product.product_id.id
                        product_obj.write(cr, uid, [prod_id], value)
                        print "Actualizando producto Open: ", prod_id
                        print "Actualizado producto Open, esale_oscom: ", esale_product.esale_oscom_id
                        esale_product_obj.write(cr, uid, [esale_product.id], {'esale_oscom_id': esale_product.esale_oscom_id,})
                       
                        updated += 1


                    print "==========Extra Info - Init =========" 
                    print "==========Extra Info - Init =========" 
                    # Creates additonal information in OpenERP objects related to product
                    self.product_extra_info_pricelist(cr, uid, website, prod_id, product) 
                    print "==========Extra Info - pl =========" 

                    self.product_extra_info_m2m(cr, uid, website, prod_id, product) 

                    print "==========Extra Info - m2m =========" 

                    self.product_extra_info_extra_fields(cr, uid, website, prod_id, product) 

                    print "==========Extra Info - ext ========="      

                    # Updates translations
                    for trans in product['product_description']:
                        value_trans = {
                            'name': trans['products_name'] or '-',
                            'description': trans['products_description'],
                            'description_sale': trans['products_description'],
                            'product_url': trans['products_url'],
                        }
                        value_trans.update(self.product_trans_fields(trans)) # Adds additional fields
                        #print "==========trans - Init========="
                        #print value_trans
                        product_obj.write(cr, uid, [prod_id], value_trans, {'lang': oerp_langs[trans['language_id']].code})

                    #self.product_extra_info(cr, uid, website, prod_id, product) 
                    print "==========trans - Fin========="
                    # Creates additonal information in OpenERP objects related to product
                    #Duplicates product for each osc attribute, associating with same OSC object
                    print "==========Entrando en Variantes ========="
                    self.variant_import_create(cr, uid, website, prod_id, product, esale_product) 
                    print "==========Saliendo de Variantes ========="


                    #Creates inventory_line
                    value_inventory_line = {
                        'inventory_id': stock_init_id,
                        'location_id': 11,
                        'product_id' : prod_id,
                        'product_uom' : 1,
                        'product_qty' : info_prod['products_quantity']
                    }
                    #print "==========Inicio Inventario ========="
                    stock_inventory_line_id = stock_inventory_line_obj.create(cr, uid, value_inventory_line)
                    if transaccional:
                        server.setSyncronizedFlag(info_prod['products_id'])
                cr.commit()
                if (created>0 or updated>0):
                    oscom_id = info_prod['products_id']
                #else:
                    #raise osv.except_osv(_('Product import done'),_('New or updated products are not found'))
            #raise osv.except_osv(_('Product import done'), _('Created: %d products\nUpdated: %d products\n\nRefresh screen to see updates') % (created, updated))
        return True



    def product_import_create(self, cr, uid, ids, *args):
        self.selected_product_import_create(cr, uid, ids, [])
        return True


    def customer_extra_info(self, cr, uid, website, customer_id, osc_customer_id):
        """If you want create additonal information in OpenERP objects related to customer you can redefine this method in your own module"""
        return True

    def sale_order_code(self, order_id_obj):
        return order_id_obj.name + "-" + str(order_id_obj.esale_oscom_id) + "-" + order_id_obj.partner_id.name
 


    def saleorder_import(self, cr, uid, website_id, context):
        """Imports sale orders from OSCommerce"""

        def _country_info(self, cr, uid, data, context):
            country_obj = self.pool.get('res.country')
            data['code'] = data['code'].upper()
            search_country = country_obj.search(cr, uid, [('code','=',data['code'])])
            if len(search_country):
                return search_country[0]
            del data['code3']
            # data['esale_oscom_id'] = data['country_id']
            del data['esale_oscom_id']
            return country_obj.create(cr, uid, data)

        def _state_info(self, cr, uid, data, country_id, context):
            state_obj = self.pool.get('res.country.state')
            data['country_id'] = country_id
            search_state = state_obj.search(cr, uid, ['|',('code','ilike',data['code']),('name','ilike','%'+data['code']+'%'), ('country_id','=',data['country_id'])])
            if len(search_state):
                return search_state[0]
            # data['esale_oscom_id'] = data['state_id']
            del data['esale_oscom_id']
            return state_obj.create(cr, uid, data)

        def _add_address(self, cr, uid, data, partner_id, context):
            address_obj = self.pool.get('res.partner.address')
            if isinstance( data.get( 'country' ), dict):
                country_id = _country_info(self, cr, uid, data['country'].copy(), context)
                data['country_id'] = country_id
                if type(data['state']) == type({}):
                    state_id = _state_info(self, cr, uid, data['state'].copy(), country_id, context)
                    data['state_id'] = state_id
            del data['country']
            del data['state']
            search_address = address_obj.search(cr, uid, [('partner_id','=',partner_id),('esale_oscom_id','=',data['esale_oscom_id'])])
            if len(search_address):
                address_obj.write(cr, uid, search_address,data)
                return search_address[0]
            else:
                data['partner_id'] = partner_id
            return address_obj.create(cr, uid, data)

 

        partner_obj = self.pool.get('res.partner')
        saleorder_obj = self.pool.get('sale.order')
        saleorder_line_obj = self.pool.get('sale.order.line')
        product_obj = self.pool.get('product.product')
        esale_product_obj = self.pool.get('esale.oscom.product')
        esale_paytype_obj = self.pool.get('esale.oscom.paytype')
        esale_carrier_obj = self.pool.get('esale.oscom.carrier')
        tax_obj = self.pool.get('account.tax')
        inv_obj = self.pool.get('account.invoice')
        journal_obj = self.pool.get('account.journal')
        esale_status_obj = self.pool.get('esale.oscom.status')
        statuses_ids_aux = esale_status_obj.search(cr, uid, [('download','=','TRUE')])
        statuses_ids =[]
        if statuses_ids_aux:
            for idst in statuses_ids_aux:
                osc_id = esale_status_obj.read(cr, uid, idst, ['esale_oscom_id'])
                statuses_ids.append(osc_id['esale_oscom_id'])
        print "statuses_ids", statuses_ids

        website = self.pool.get('esale.oscom.web').browse(cr, uid, website_id)
        osc_int = esale_status_obj.read(cr, uid, website.intermediate.id, ['esale_oscom_id'])
        intermediate = osc_int['esale_oscom_id']
        print "intermediate before import", intermediate

        server = xmlrpclib.ServerProxy("%s/openerp-synchro.php" % website.url)
        cr.execute("select max(esale_oscom_id) from sale_order where esale_oscom_web=%s;" % str(website.id))
        max_web_id = cr.fetchone()[0]

        min_openorder=-1
        if max_web_id:
            saleorders = server.get_saleorders(max_web_id, statuses_ids)
            min_openorder = server.get_min_open_orders(max_web_id)
        else:
            saleorders = server.get_saleorders(0, statuses_ids)
        no_of_so = 0
        for saleorder in saleorders:
            print "==========*********NEW**************==========="
            print "== Oscommerce Sale Order Number :", saleorder['id']
            print "PEDIDO VENTA: " , saleorder
            saleorder_partner = saleorder.get('partner', '')
            oscom_partner = None
            if not len(saleorder_partner):
                if saleorder.get( 'id' ):
                    raise osv.except_osv( _( 'Warning' ), _( "There aren't a Partner in this Sale Order (id: %s)" ) % saleorder[ 'id' ] )
                else:
                    raise osv.except_osv( _( 'Warning' ), _( "There aren't a Partner in this Sale Order" ) )
            else:
                oscom_partner = saleorder['partner'][0]
                #print "== Sale order partner:", saleorder['partner'][0]
            partner_ids = partner_obj.search(cr, uid, [('esale_oscom_id','=',oscom_partner['esale_oscom_id'])])
            if len(partner_ids):
                partner_id = partner_ids[0]
                #print "partner por ID: ", partner_ids
                partner_obj.write(cr, uid, partner_ids, {'name':oscom_partner['name']})
            else:
                print " CIF Nuevo log: ", oscom_partner['vat']
                if oscom_partner['vat'] != 'ES01234567L':
                    partner_ids = partner_obj.search(cr, uid, [('vat','=',oscom_partner['vat'])])
                    if len(partner_ids):
                        partner_id = partner_ids[0]
                        print "ENCONTRADO partner por CIF: ", partner_ids
                        partner_obj.write(cr, uid, partner_ids, {'name':oscom_partner['name'], 'esale_oscom_id': oscom_partner['esale_oscom_id']})
                    #Añadido última edicion Dani - Ana
                    else:
                        print "CREANDO NUEVO PARTNER: ", partner_ids
                        del oscom_partner['addresses']
                        partner_id = partner_obj.create(cr, uid, oscom_partner)
                        partner_obj.write(cr, uid, partner_ids, {'ref':oscom_partner['esale_oscom_id']})
                else:
                    print "CREANDO NUEVO PARTNER: ", partner_ids
                    del oscom_partner['addresses']
                    partner_id = partner_obj.create(cr, uid, oscom_partner)
                    partner_obj.write(cr, uid, partner_ids, {'ref':oscom_partner['esale_oscom_id']})

                self.customer_extra_info(cr, uid, website, partner_id, oscom_partner['esale_oscom_id']) # Creates additonal information in OpenERP objects related to customer
            
            # Default address is right on Website so we create the order.
            if len(saleorder.get('address', '')):
                # print "===Sale order address:",saleorder['address'][0]
                default_address = saleorder['address'][0]
                del saleorder['address']
                default_address['type'] = 'default'
                default_address_id = _add_address(self, cr, uid, default_address.copy(), partner_id, context)
                shipping_address = []
                if len(saleorder['delivery']) > 0 :
                    #print ""
                    #print "===Sale order Delivery:",saleorder['delivery'][0]
                    shipping_address = saleorder['delivery'][0]
                    del saleorder['delivery']
                    shipping_address['type'] = 'delivery'
                    shipping_address_id = _add_address(self, cr, uid, shipping_address.copy(), partner_id, context)
                billing_address = []
                if len(saleorder['billing']) > 0 :
                    #print ""
                    #print "===Sale order Billing:",saleorder['billing'][0]
                    billing_address = saleorder['billing'][0]
                    del saleorder['billing']
                    billing_address['type'] = 'invoice'
                    billing_address_id = _add_address(self, cr, uid, billing_address.copy(),partner_id, context)

                value={ 'esale_oscom_web': website.id,
                        'esale_oscom_id' : saleorder['id'],
                        'shop_id'        : website.shop_id.id,
                        'partner_id'     : partner_id,
                        'note'           : saleorder['note'],
                        'pay_met_title'  : saleorder['pay_met_title'],
                        'shipping_title' : saleorder['shipping_title'],
                        'orders_status'  : saleorder['orders_status'],
                        'date_order'     : saleorder['date'],
                        #'price_type'    : saleorder['price_type']
                    }

                value.update(saleorder_obj.onchange_shop_id(cr, uid, [], value['shop_id'])['value'])
                value.update(saleorder_obj.onchange_partner_id(cr, uid, [], value['partner_id'])['value'])
        #        address_obj = self.pool.get('res.partner.address')
        #        for address in [('address','order'), ('billing', 'invoice'), ('delivery', 'shipping')]:
        #            criteria = [('partner_id', '=', website.partner_anonymous_id.id)]
        #            insert = {'partner_id': website.partner_anonymous_id.id}
        #            for criterium in [('city', 'city'), ('name', 'name'), ('zip','zip'), ('address', 'street') ]:
        #                criteria.append((criterium[1], 'like', saleorder[address[0]][criterium[0]]))
        #                insert[criterium[1]] = saleorder[address[0]][criterium[0]]
        #            address_ids = address_obj.search(cr, uid, criteria)
        #            if len(address_ids):
        #                id = address_ids[0]
        #            else:
        #                country_ids = self.pool.get('res.country').search(cr, uid, [('name', 'ilike', saleorder[address[0]]['country'])])
        #                if len(country_ids):
        #                    country_id = country_ids[0]
        #                else:
        #                    country_id = self.pool.get('res.country').create(cr, uid, { 'name' : saleorder[address[0]]['country'],
        #                                                                              'code' : saleorder[address[0]]['country'][0:2].lower()})
        #                insert['country_id'] = country_id
        #                if address[0] == 'address':
        #                    insert['email'] = saleorder['address']['email']
        #                id = address_obj.create(cr, uid, insert)
        #
        #            value.update({'partner_%s_id' % address[1]: id})
                value['partner_order_id'] = default_address_id
                if len(shipping_address) > 0 :
                    value['partner_shipping_id'] = shipping_address_id
                else:
                    value['partner_shipping_id'] =  default_address_id

                if len(billing_address) > 0 :
                    value['partner_invoice_id'] = billing_address_id
                else:
                    value['partner_invoice_id'] =  default_address_id
                order_id = saleorder_obj.create(cr, uid, value)
                order_id_obj = saleorder_obj.browse(cr, uid, order_id)
                fpos = order_id_obj.partner_id.property_account_position and order_id_obj.partner_id.property_account_position.id or False
                if fpos: 
                    print "posicion fiscal cliente", fpos

                concat_cod = self.sale_order_code(order_id_obj)
                saleorder_obj.write(cr, uid, [order_id], {'name':concat_cod})
                saleorder[ 'carrier_id' ] = False
 
                for orderline in saleorder['lines']:
                    if orderline['product_id'] != -1 :
                        print "tratando linea", orderline

                        print "Finding variant: ", saleorder['id'], " product:" , orderline['product_id']
                        variant_name = server.get_saleorderline_attributes(saleorder['id'], orderline['orders_products_id'])
                        print "variant_name", variant_name

                        ids = esale_product_obj.search(cr, uid, [('esale_oscom_id', '=', orderline['product_id']), ('web_id', '=', website.id)])
                        if len(ids):
                            oscom_product_id = ids[0]
                            oscom_product = esale_product_obj.browse(cr, uid, oscom_product_id)
                            product_id = oscom_product.product_id.id                        
                            print "****************producto openERP encontrado:**************", product_id
                            prod_tmp_id = oscom_product.product_id.product_tmpl_id.id
                            print "****************Template:**************", prod_tmp_id

                            product_variant_ids = product_obj.search(cr, uid, [('product_tmpl_id', '=', prod_tmp_id), ('variants', '=', variant_name)])
                            if len(product_variant_ids):
                                print "****************Variante encontrada:**************", product_variant_ids
                                product_id = product_variant_ids[0]                       
                                print "****************VARIANTE DE producto oscommerce encontrada:**************", product_id
                        else:
                            print "****************creando nuevo producto***************", orderline['product_id']
                            print  website.id
                            create_id = self.selected_product_import_create(cr, uid, [website.id], [ orderline['product_id'] ])
                            if create_id:
                                print "****************Buscando nuevo producto***************", orderline['product_id'], "variante : ", variant_name
                                ids = esale_product_obj.search(cr, uid, [('esale_oscom_id', '=', orderline['product_id']), ('web_id', '=', website.id)])
                                if len(ids):
                                    oscom_product_id = ids[0]
                                    oscom_product = esale_product_obj.browse(cr, uid, oscom_product_id)
                                    product_id = oscom_product.product_id.id                        
                                    print "****************producto openERP encontrado TC:**************", product_id
                                    prod_tmp_id = oscom_product.product_id.product_tmpl_id.id
                                    print "****************Template:************** TC", prod_tmp_id

                                    product_variant_ids = product_obj.search(cr, uid, [('product_tmpl_id', '=', prod_tmp_id), ('variants', '=', variant_name)])
                                    if len(product_variant_ids):
                                        print "****************Variante encontrada TC:**************", product_variant_ids
                                        product_id = product_variant_ids[0]                       
                                        print "****************VARIANTE DE producto oscommerce encontrada: TC**************", product_id
                                    print "producto oscommerce encontrado tras creacion:", product_id
                    else :
                        print "****************Tratando producto de transporte o pago **************", orderline['product_id']
                        line_found = False
                        oscom_name = unaccent( orderline[ 'name' ] ).lower()
                        for carrier_id in esale_carrier_obj.browse( cr, uid, [ x for x in esale_carrier_obj.search( cr, uid, [ ( 'web_id', '=', website.id ) ], context=context ) ] ):
                            
                            openerp_name = unaccent( carrier_id.name.split("(")[0]).lower()
                            openerp_name_strip = openerp_name.replace( ' ', '' )
                            if oscom_name.find( openerp_name ) != -1 or oscom_name.find( openerp_name_strip ) != -1:
                                saleorder[ 'carrier_id' ] = carrier_id.carrier_id.id
                                product_id = carrier_id.product_id.id
                                print "****************Encontrado Transportista:**************", orderline['product_id']
                                line_found = True
                                break
                        if not line_found:
                            for paytype_id in esale_paytype_obj.browse( cr, uid, [ x for x in esale_paytype_obj.search( cr, uid, [ ( 'web_id', '=', website.id ) ], context=context ) ] ):
                                paytype_name = unaccent( paytype_id.name ).lower()
                                paytype_name_strip = paytype_name.replace( ' ', '' )
                                if oscom_name.find( paytype_name ) != -1 or oscom_name.find( paytype_name_strip ) != -1:
                                    product_id = paytype_id.product_id.id
                                    print "****************Encontrado Pago:**************", orderline['product_id']

                                    line_found = True
                                    break
                        if not line_found:
                            product_id = product_obj.search(cr, uid, [('name','=','Shipping Cost')])[0] 

                    linevalue = {
                        'product_id'     : product_id,
                        'product_uom_qty': orderline['product_qty'],
                        'order_id'       : order_id,
                        # Make a mark in the line to advice that it use the external prices, and in this case the total external prices
                        'use_external_prices': 'external_total_prices',
                    }
                    producto = self.pool.get('product.product').browse(cr, uid, product_id)
                    fiscal_pos = fpos and self.pool.get('account.fiscal.position').browse(cr, uid, fpos) or False
                    set_taxes = []
                    onchange_product_sol = saleorder_line_obj.product_id_change(cr, uid, [], value['pricelist_id'], linevalue['product_id'], linevalue['product_uom_qty'],False, 0, False, '', value['partner_id'])['value']
                    if fiscal_pos:
                        print fiscal_pos.id
                        set_taxes = self.pool.get('account.fiscal.position').map_tax(cr, uid, fiscal_pos, producto.taxes_id)
                        print "set_taxes", set_taxes
                        onchange_product_sol['tax_id'] = set_taxes
                    else:
		                if orderline['tax_rate'] > 0.0000:
		                    tax_rate_search_ids = tax_obj.search(cr, uid, [('amount','=',orderline['tax_rate']/100), ('type_tax_use', '=','sale')])
                            #tax_rate_search_ids = tax_obj.search(cr, uid, [('tax_group','=','vat'),('amount','=',orderline['tax_rate']/100), ('type_tax_use', '=','sale')])
		                else:
		                    tax_rate_search_ids = tax_obj.search(cr, uid, [('amount','=',0), ('type_tax_use', '=','sale')])
                           # tax_rate_search_ids = tax_obj.search(cr, uid, [('tax_group','=','vat'),('amount','=',0), ('type_tax_use', '=','sale')])
		                if tax_rate_search_ids:
		                    onchange_product_sol['tax_id'] = tax_rate_search_ids
                    price = orderline['price']
                    name = orderline['name']                      
                    attributes = (orderline.has_key('attributes') and orderline['attributes']) or False
                    if saleorder['price_type'] == 'tax_excluded' and attributes:
                        # print "EVALUANDO PRECIOS ATRIBUTOS: ", str(price)
                        # print "prefix: ", attributes['price_prefix']
                        # print "EVALUANDO PRECIOS ATRIBUTOS2: ", str(attributes['options_values_price'])
                        price = eval(str(price) + attributes['price_prefix'] + str(attributes['options_values_price']))
                        name = name + ' ' + attributes['products_options'] + ' + ' + attributes['products_options_values']
                    elif saleorder['price_type'] == 'tax_included':
                        price = price * (1+orderline['tax_rate']/100)
                        if attributes:
                            options_value_price = attributes['options_values_price']
                            cal_options_value_price = options_value_price * (1+orderline['tax_rate']/100)
                            price = eval(str(price) + attributes['price_prefix'] + str(cal_options_value_price))
                            name = name + ' ' + attributes['products_options'] + ' + ' + attributes['products_options_values']
                    onchange_product_sol['price_unit'] = round(price,2)
                    onchange_product_sol['discount']=0.0
                    linevalue.update(onchange_product_sol)
                    linevalue.update(saleorder_line_obj.default_get(cr, uid, ['sequence', 'invoiced', 'state', 'product_packaging']))
                    linevalue['name'] = name
                    if linevalue.get('weight',False):
                        del linevalue['weight']
                    linevalue["product_uos"] = linevalue['product_uos'] and linevalue['product_uos'][0]
                    tax_id = linevalue['tax_id'] and linevalue['tax_id'][0]
                    del linevalue['tax_id']
                    ptax_id = []
                    if tax_id:
                        ptax_id = [ tax_id ]

                    id_orderline = saleorder_line_obj.create(cr, uid, linevalue)
                    if fiscal_pos:
                        saleorder_line_obj.write(cr, uid, [id_orderline], {'tax_id':[(6, 0, set_taxes)]})
                    else:
                        saleorder_line_obj.write(cr, uid, [id_orderline], {'tax_id':[(6, 0, ptax_id)]})
                no_of_so +=1

                # Take the total invoiced in the sale order from oscommerce to the openerp and the delivery carrier
                saleorder_obj.write(cr, uid, [ order_id ], {
                    #'external_sale_base_amount': saleorder[ 'order_subtotal' ],
                    #'external_tax_amount': saleorder[ 'order_tax' ],
                    #'external_sale_total_amount': saleorder[ 'order_total' ],
                    #'use_external_prices': 'external_total_prices',
                    'carrier_id': saleorder[ 'carrier_id' ],
                })

                ######################################################################################
                oscom_pay_met = saleorder['pay_met']
                typ_ids = esale_paytype_obj.search(cr, uid, [('esale_oscom_id', '=', oscom_pay_met), ('web_id', '=', website.id)])
                saleorder = saleorder_obj.browse(cr, uid, order_id)
                if typ_ids:
                    typ_data = esale_paytype_obj.browse(cr, uid, typ_ids)[0]
                    paytype = typ_data.paytyp
                    cr.execute('select * from ir_module_module where name=%s and state=%s', ('sale_payment','installed'))
                    if cr.fetchone():
                        saleorder_obj.write(cr, uid, [order_id], {'payment_type': typ_data.payment_id.id})
                else:
                    paytype = 'type1'
                wf_service = netsvc.LocalService("workflow")
                if paytype == 'type1':
                    #SO in state draft so nothing
                    pass
                elif paytype == 'type2':
                    #SO in state confirmed
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'order_confirm', cr)
                elif paytype == 'type3':
                    #INVOICE draft
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'order_confirm', cr)
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'manual_invoice', cr)
                elif paytype == 'type4':
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'order_confirm', cr)
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'manual_invoice', cr)
                    inv_ids = inv_obj.search(cr, uid, [('origin','=',saleorder.name)])
                    inv_obj.button_compute(cr, uid, inv_ids)
                    wf_service.trg_validate(uid, 'account.invoice',inv_ids[0], 'invoice_open', cr)
                elif paytype == 'type5':
                    #INVOICE payed
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'order_confirm', cr)
                    wf_service.trg_validate(uid, 'sale.order', order_id, 'manual_invoice', cr)
                    pay_account_id = (website.esale_account_id)['id']
                    pay_journal_id = typ_data.journal_id.id
                    inv_ids = inv_obj.search(cr, uid, [('origin','=',saleorder.name)])
                    inv_obj.button_compute(cr, uid, inv_ids)
                    wf_service.trg_validate(uid, 'account.invoice',inv_ids[0], 'invoice_open', cr)
                    ids = self.pool.get('account.period').find(cr, uid, context=context)
                    period_id = False
                    if len(ids):
                        period_id = ids[0]

                    invoice = inv_obj.browse(cr, uid,inv_ids[0],{})
                    company_currency = self.pool.get('res.users').browse(cr, uid, uid).company_id.currency_id.id
                    if invoice.currency_id.id != company_currency:
                        amount = round(self.pool.get('res.currency').compute(cr, uid, invoice.currency_id.id, company_currency, invoice.amount_total), 2)
                    else:
                        amount = invoice.amount_total

                    inv_obj.pay_and_reconcile(cr, uid, inv_ids, amount, pay_account_id, period_id, pay_journal_id, False, False, False, context={})
                else:
                    #The payment method hasn't been mapped
                    pass
            cr.commit()
        for saleorder in saleorders:
            #print "website.intermediate: " , intermediate
            server.update_order_status(saleorder['id'], intermediate, '',0,0)

        ###################### look for open orders in site that are 'done' in TinyERP ###################
        ######################                and close them                           ###################
        return no_of_so
esale_oscom_web()


class esale_oscom_saleorder_line(osv.osv):
    def _amount_line_net(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for line in self.browse(cr, uid, ids):
            if line.product_uos.id:
                res[line.id] = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            else:
                res[line.id] = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        return res

    _inherit='sale.order.line'
    _columns = {
        'price_unit': fields.float('Unit price', required=True, digits=(16, 2)),
        'price_net': fields.function(_amount_line_net, method=True, string='Net price', digits=(16, 2)),
    }
esale_oscom_saleorder_line()


class esale_oscom_saleorder(osv.osv):
    _inherit='sale.order'
    _name='sale.order'
    _table='sale_order'
    _columns = {
        'esale_oscom_web': fields.many2one('esale.oscom.web', 'Website'),
        'esale_oscom_id': fields.integer('esale_oscom Id'),
        'pay_met_title': fields.char('Payment Method', size=255),
        'shipping_title': fields.char('Shipping', size=255),
        'shipping_agency': fields.many2one('res.partner', 'Carrier Partner',help=" Include Carrier to delivery order with" ),
        'tracking_number': fields.char('Num tracking', size=32, help="Include order trucking number given by carrier"),
        'number_of_packages': fields.char('Num pack', size=32, help="Include number of packages to send"),
        'volume': fields.char('Volum', size=32, help="Include volume of packages to send"),
        'additional_info': fields.text('Aditional Info', help="Include any additional info you need internaly include on order"),
        'orders_status': fields.char('Osc Status Inic', size=32,help="Indicates the initial status of order on Osc Web"),
        'orders_status_id': fields.many2one('esale.oscom.status','Osc Status Actual',help="Indicates the actual status of order on Osc Web"),
        'status_comment': fields.text('Status Comment', help="Write a comment to include on Osc order. It will be uploaded to Osc Web on changing actual osc status"), 
        'update_comment': fields.boolean('Update Comment', help="Click if you want to Update comments on order"),  
        'send_web_email': fields.boolean('Send web E-mail', help="Click if you want Sending comments to customer from web. Requires modifying .php procedure"), 
    }
    _defaults = {
        'esale_oscom_id': lambda *a: False,
        'update_comment': lambda *a: False,
        'send_web_email': lambda *a: False,
    }

    def onchange_esale_oscom_web( self, cr, uid, ids, esale_oscom_web, context=None ):
        value = {}
        if esale_oscom_web:
            web = self.pool.get('esale.oscom.web').browse(cr, uid, esale_oscom_web)
            value['shop_id'] = web.shop_id.id
            # value['partner_id'] = web.partner_anonymous_id.id
            value.update(self.pool.get('sale.order').onchange_shop_id(cr, uid, ids, value['shop_id'])['value'])
            # value.update(self.pool.get('sale.order').onchange_partner_id(cr, uid, ids, value['partner_id'])['value'])

        return { 'value': value }

    def order_create( self, cr, uid, ids, context=None ):
        if not context:
            context = {}
        partner_obj = self.pool.get('res.partner')
        saleorder_obj = self.pool.get('sale.order')
        for order in self.browse(cr, uid, ids, context):
            addr = partner_obj.address_get(cr, uid, [order.partner_id.id], ['delivery','invoice','contact'])
            pricelist_id = order.partner_id.property_product_pricelist[0]
            order_lines = []
            for line in order.order_lines:
                order_lines.append( (0,0,{
                    'name': line.name,
                    'product_qty': line.product_qty,
                    'date_planned': line.date_planned,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'type': line.product_id.procure_method
                 }) )
            order_id = saleorder_obj.create(cr, uid, {
                'name': order.name,
                'shop_id': order.web_id.shop_id.id,
                'origin': 'WEB:'+str(order.id),
                'date_order': order.date_order,
                'user_id': uid,
                'partner_id': order.partner_id.id,
                'partner_invoice_id': addr['invoice'],
                'partner_order_id': addr['contact'],
                'partner_shipping_id': addr['delivery'],
                'pricelist_id': pricelist_id,
                'order_line': order_lines
            })
            self.write(cr, uid, [order.id], {'state':'done', 'order_id': order_id})
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'sale.order', order_id, 'order_confirm', cr)
        return True

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=['confirmed','done']):
        ret_super = super(esale_oscom_saleorder,self).action_invoice_create(cr, uid, ids, grouped, states)
        # If you have create the invoice after you remove it, if you try to create it again you obtain a Flase ret_super, because the lines don't permit you to create the invoce, because they are market as invoiced, soy you have to change it checkbox from DB.
        if not ret_super:
            return False
        sale_order = self.browse(cr, uid, ids[0])
        self.pool.get('account.invoice').write(cr, uid, [ret_super], {'esale_oscom_web': sale_order.esale_oscom_web.id})
        return ret_super

    def write( self, cr, uid, ids, vals, context=None ):
        result = super( esale_oscom_saleorder, self ).write( cr, uid, ids, vals, context )
        if 'orders_status_id' in vals.keys():
            orders_status_id = vals['orders_status_id']
            for id in ids:
                sale_order = self.browse( cr, uid, id, context )
                if 'esale_oscom_web' in vals.keys():
                    website = self.pool.get( 'esale.oscom.web' ).browse( cr, uid, vals['esale_oscom_web'] )
                else:
                    website = sale_order.esale_oscom_web
                if website and orders_status_id:
                    if 'esale_oscom_id' in vals.keys():
                        esale_oscom_id = vals['esale_oscom_id']
                    else:
                        esale_oscom_id = sale_order.esale_oscom_id
                    if 'status_comment' in vals.keys():
                        status_comment = vals['status_comment']
                    else:
                        status_comment = sale_order.status_comment
                    if 'update_comment' in vals.keys():
                        update_comment = vals['update_comment']
                    else:
                        update_comment = sale_order.update_comment
                    if 'send_web_email' in vals.keys():
                        send_web_email = vals['send_web_email']
                    else:
                        send_web_email = sale_order.send_web_email
                    if 'tracking_number' in vals.keys():
                        tracking_number = vals['tracking_number']
                    else:
                        tracking_number = sale_order.tracking_number

                    server = xmlrpclib.ServerProxy( "%s/openerp-synchro.php" % website.url )
                    osc_int = self.pool.get('esale.oscom.status').read(cr, uid, orders_status_id, ['esale_oscom_id'])
                    ostatus_id = osc_int['esale_oscom_id'] 
                    status_comment_tn = status_comment or ''
                    if tracking_number:
                        status_comment_tn = "Tracking: " + tracking_number + "\n " + status_comment
                    if not update_comment:
                        update_comment = 0
                    if not send_web_email:
                        send_web_email = 0
                    server.update_order_status(esale_oscom_id, ostatus_id, status_comment_tn, update_comment, send_web_email)
        return result

esale_oscom_saleorder()


class esale_oscom_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'esale_oscom_web': fields.many2one('esale.oscom.web', 'Website'),
    }
esale_oscom_invoice()


class esale_oscom_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'esale_oscom_id': fields.integer('OScommerce Id'),
    }
esale_oscom_partner()


class esale_oscom_partner_address(osv.osv):
    _inherit = 'res.partner.address'
    _columns = {
        'esale_oscom_id': fields.integer('OScommerce Id'),
    }
esale_oscom_partner_address()

class stock_picking( osv.osv ):
    _inherit = "stock.picking"

    # Because the delivery carrier amount are download from oscommerce, but we have the delivery module as a dependency for the mapping, and the delivery module will create a another invoice line with the delivery grid, the only "clean" way to solve the duplicated line problem is taken the delivery before the creation of the invoices and put again at the end.
    def action_invoice_create( self, cursor, user, ids, journal_id=False, group=False, type='out_invoice', context=None ):
        pick_delivery = {}
        for picking in self.browse( cursor, user, ids, context=context ):
            pick_delivery[ picking.id ] = picking.carrier_id.id
        self.write( cursor, user, ids, {
            'carrier_id': '',
        }, context )

        result = super( stock_picking, self ).action_invoice_create( cursor, user, ids, journal_id, group, type, context )

        pick_ids = result.keys()
        for pick_id in pick_ids:
            self.write( cursor, user, [ pick_id ], {
                'carrier_id': pick_delivery[ pick_id ],
            }, context )
    	return result

stock_picking()
