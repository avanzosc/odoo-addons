<?php
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com> 
#    Copyright (c) 2009-2010 Ana Juaristi Avanzosc, S.L. <ajuaristio@gmail.com>
#                       NaN Projectes de Programari Lliure, S.L. (http://www.nan-tic.com)
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
##############################################################################*/

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////   On windows servers line 65 use return utf8_encode($text);                   ////////////////////
/////////////////      PLEASE CONFIGURE THE RIGHT INCLUDES AND DEFINES FOR YOUR CONFIGURATION   ////////////////////

include("xmlrpcutils/xmlrpc.inc");
include("xmlrpcutils/xmlrpcs.inc");
include("../../includes/configure.php");
// Activate if you need integrating esale_m2m_categories or esale_extra_fields
include("esale_osc_m2mcat.php");
include("esale_osc_extra_fields.php");
include("esale_osc_variants.php");


define('TRANSACTIONAL',true); //Set true if you have intalled transactional feature.
define('RESPONSE_ENCODING', 'ISO-8859-1'); //It must be your DDBB encoding
define('DEBUG_FILE', 'temp/debug.xmlrpc.txt'); //Absolute path to debug and warning file
define('BAJA_IMAGENES',1); //Set true if you want downloading product with images.
define('STORES_ID',1); //Set default stores ID.
define('CREA_UPDATE',0); //Set true if you want downloading product with images.

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$con = mysql_pconnect(DB_SERVER, DB_SERVER_USERNAME, DB_SERVER_PASSWORD);
mysql_select_db(DB_DATABASE);


function debug($s) {
    $fp = fopen(DEBUG_FILE,"a");
    fwrite($fp, $s."\n");
    fclose($fp);
}

function debug_arr($para_arr,$tab='') {
    if (is_array($para_arr)) {
        foreach($para_arr as $key=>$values) {
            debug($tab.'Key :'.$key.' Value :'.$values);
            /*
            if (is_array($values)) {
                $tab.='\t';
                debug_arr($values,$tab);
            }*/
        }
    }
}

function clean_special_chars($text){
    for ($i=128; $i<=159; $i++){
        $text = ereg_replace(chr($i), "?", $text );
    }
    return utf8_encode($text);
}

function get_taxes() {
    $taxes = array();

    $result = mysql_query("select tax_class_id, tax_class_title from tax_class;");
    if ($result) while ($row = mysql_fetch_row($result)) {
        $taxes[] = new xmlrpcval(array(new xmlrpcval($row[0], "int"), new xmlrpcval($row[1], "string")), "array");
    }
    return new xmlrpcresp( new xmlrpcval($taxes, "array"));
}

function get_statuses() {
    $status = array();
    debug("select orders_status_id, orders_status_name, language_id from orders_status;");
    $result = mysql_query("select orders_status_id, orders_status_name, language_id from orders_status;");
    if ($result) while ($row = mysql_fetch_row($result)) {
        $status[] = new xmlrpcval(array(new xmlrpcval($row[0], "int"), new xmlrpcval(clean_special_chars($row[1]), "string"), new xmlrpcval($row[2], "int")), "array");
    }
    return new xmlrpcresp( new xmlrpcval($status, "array"));
}


function get_languages() {
    $languages = array();

    $result = mysql_query("select languages_id, name from languages;");
    if ($result) while ($row = mysql_fetch_row($result)) {
        $languages[] = new xmlrpcval(array(new xmlrpcval($row[0], "int"), new xmlrpcval(clean_special_chars($row[1]), "string")), "array");
    }
    return new xmlrpcresp(new xmlrpcval($languages, "array"));
}


function get_categories() {
    $categories = array();

    $result = mysql_query("select categories_id, min(language_id) from categories_description group by categories_id;");
    if ($result) while ($row = mysql_fetch_row($result)) {
        $resultb = mysql_query("select categories_id, categories_name from categories_description where categories_id=".$row[0]." and language_id=".$row[1].";");
        if ($resultb and $row = mysql_fetch_row($resultb)) {
            $categories[] = new xmlrpcval(array(new xmlrpcval($row[0], "int"), new xmlrpcval(clean_special_chars(parent_category($row[0],$row[1])), "string")), "array");
        }
    }
    return new xmlrpcresp( new xmlrpcval($categories, "array"));
}

function get_categories_parent($languages) {
    $categories = array();
    $lang_ids = "";

    foreach ($languages as $lang) $lang_ids .= $lang.", ";
    $lang_ids = substr($lang_ids, 0, strlen($lang_ids)-2);
    $result = mysql_query("select categories_id, parent_id from categories order by parent_id;");
    if ($result) while ($row = mysql_fetch_row($result)) {
        debug('Category: ' . $row[0].'-'. $row[1]);
        $cat = array(new xmlrpcval($row[0], "int"), new xmlrpcval($row[1], "int"));
        $resultlang = mysql_query("select categories_id, categories_name from categories_description where categories_id=".$row[0]." and language_id in ($lang_ids);");
        if ($resultlang) while ($rowl = mysql_fetch_row($resultlang)) {
            debug('Category language: ' .$rowl[1]);
            $cat[] = new xmlrpcval(clean_special_chars($rowl[1]), "string");
        }
        $categories[] = new xmlrpcval($cat, "array");
    }
    return new xmlrpcresp(new xmlrpcval($categories, "array"));
}

function get_products($languages, $osCodIni, $block, $last_date) {
    $products = array();
    $prod = array();
    $prod_desc = array();
    $row_product = array();
    $products_description_str = "";
    $products_url_str = "";
    $row_manuf = array();
    $manufacturers_name = "";
    $manuf_url = array();
    $manufacturers_url = "";

    $lang_ids = implode(", ", $languages);
    //debug('Languages ids = '.$lang_ids);

    $sQuery = "select products_id,
        products_quantity,
        products_model,
        products_image,
        products_price,
        products_date_added,
        products_last_modified,
        products_date_available,
        products_weight,
        products_status,
        products_tax_class_id,
        manufacturers_id
        from products";

    $nexo = ' where products_id > 2580 and ';

    if (TRANSACTIONAL){
        $sQuery .= $nexo . "( products_last_modified >= '" . $last_date . "' ";
		$nexo = ' or ';
        $sQuery .= $nexo . "products_date_added >= '" . $last_date . "' )" ;
		$nexo = ' and ';
	}

    if ($block==1){
        $sQuery .= $nexo . "products_id = " . $osCodIni;
		$nexo = ' and ';
	}else{
        $sQuery .= $nexo . "products_id > " . $osCodIni;
		$nexo = ' and ';
	}

	$sQuery .= " order by products_id LIMIT " . $block;
    debug('Query: ' .$sQuery);
    $result = mysql_query($sQuery);

    //debug('IF-WHILE-get_products');
    if ($result) while ($row_product = mysql_fetch_row($result)) {
        $resultcateg = mysql_query("select min(categories_id) from products_to_categories
            where products_id=".$row_product[0]." group by products_id;");
        if ($resultcateg) {
                $row = mysql_fetch_row($resultcateg);
            $prod_cat = $row[0];
            $prod_atrib = array();// If product has not attributes

        }
        debug('Producto: ' .$row_product[0]);
        //Get product's manufacturer name
        if ($row_product[11] > 0){
            $resultmanuf = mysql_query("select manufacturers_name from manufacturers where manufacturers_id = ".$row_product[11].";");
            if ($resultmanuf){
                $row_manuf = mysql_fetch_row($resultmanuf);
                if (strlen($row_manuf[0]) > 0)
                    $manufacturers_name = $row_manuf[0];
                else
                    $manufacturers_name = "";
            }
            //Get product's manufacturer url on each language
            $manuf_url = array();
            $resultmanuflang = mysql_query("select manufacturers_url, languages_id
                from manufacturers_info where manufacturers_id = ".$row_product[11]." and languages_id in (".$lang_ids.");");
            if ($resultmanuflang) while ($row_manuflang = mysql_fetch_row($resultmanuflang)) {
                if (strlen($row_manuflang[0]) == 0)
                    $manufacturers_url = "";
                else
                    $manufacturers_url = $row_manuflang[0];
                $manuf_url[] = new xmlrpcval(array(
                    "languages_id" => new xmlrpcval($row_manuflang[1],"int"),
                    "manufacturers_url" => new xmlrpcval($manufacturers_url,"string"),
                    ), "struct");
            }
        } else {
            $manufacturers_name = "";
            $manuf_url = array();
        }

        $prod = new xmlrpcval(array(
            "products_id" => new xmlrpcval($row_product[0],"int"),
            "products_quantity" => new xmlrpcval($row_product[1],"int"),
            "products_model" => new xmlrpcval(clean_special_chars($row_product[2]),"string"),
            "products_image" => new xmlrpcval(clean_special_chars($row_product[3]),"string"),
            "products_price" => new xmlrpcval(clean_special_chars($row_product[4]),"string"),
            "products_date_added" => new xmlrpcval(clean_special_chars($row_product[5]),"string"),
            "products_last_modified" => new xmlrpcval(clean_special_chars($row_product[6]),"string"),
            "products_date_available" => new xmlrpcval(clean_special_chars($row_product[7]),"string"),
            "products_weight" => new xmlrpcval(clean_special_chars($row_product[8]),"string"),
            "products_status" => new xmlrpcval($row_product[9],"int"),
            "products_tax_class_id" => new xmlrpcval($row_product[10],"int"),
            "manufacturers_name" => new xmlrpcval(clean_special_chars($manufacturers_name),"string"),
            "categ_id" => new xmlrpcval($prod_cat,"int")), "struct");
        //debug('Product_id: ' . $row_product[0] . '-IMG:' .$row_product[3]. '-CAT:' . $prod_cat);

        // Get product information in different languages
        $prod_desc = array();
        $resultlang = mysql_query("select products_id,
            language_id,
            products_name,
            products_description,
            products_url,
            products_viewed
            from products_description where products_id=".$row_product[0]." and language_id in (".$lang_ids.");");
        if ($resultlang) while ($row_desc = mysql_fetch_row($resultlang)) {
        /*    if (strlen($row_desc[3] == 0))
                $products_description_str = "";
            else
                $products_description_str = $row_desc[3];
            if (strlen($row_desc[4] == 0))
                $products_url_str = "";
            else
                $products_url_str = $row_desc[4];
        */        

            $description=clean_special_chars($row_desc[3]);
			if ($description!=$row_desc[3]){
                debug(date(DATE_ATOM) . ' -- Product_id: ' . $row_desc[0] . ' Language_id: ' . $row_desc[1] . ' -> Undefined characters: Description has been updated.');
            }

            $prod_desc[] = new xmlrpcval(array(
                //"products_id" => new xmlrpcval($row_desc[0],"int"),
                "language_id" => new xmlrpcval($row_desc[1],"int"),
                "products_name" => new xmlrpcval(clean_special_chars($row_desc[2]),"string"),
                "products_description" => new xmlrpcval($description,"string"),
                "products_url" => new xmlrpcval(clean_special_chars($row_desc[4]),"string"),
                "products_viewed" => new xmlrpcval(clean_special_chars($row_desc[5]),"string")), "struct");
            //debug('Product_id: ' . $row_desc[0] . 'language_id: ' . $row_desc[1] . 'products_name: ' . $row_desc[2]);
        }
                    $prod_atrib = array();// If product has not attributes

        // Get product discounts
        $prod_spec = new xmlrpcval(array(), "struct"); // If product has not any discount
        $resultspec = mysql_query("select specials_new_products_price,
            specials_date_added,
            specials_last_modified,
            expires_date,
            date_status_change,
            status
            from specials where products_id=". $row_product[0] .
                            " and specials_date_added =
                            (select max(specials_date_added) from specials where products_id=". $row_product[0] . ");");
        if ($resultspec) {
            $rowesp = mysql_fetch_row($resultspec);
            //debug('Product specials: ' . $rowesp[0] . " " . $rowesp[3]);
            $prod_spec = new xmlrpcval(array(
                "specials_new_products_price" => new xmlrpcval($rowesp[0],"string"),
                //"specials_date_added" => new xmlrpcval($rowesp[1],"string"),
                //"specials_last_modified" => new xmlrpcval($rowesp[2],"string"),
                "expires_date" => new xmlrpcval($rowesp[3],"string"),
                //"date_status_change" => new xmlrpcval($rowesp[4],"string"),
                "status" => new xmlrpcval($rowesp[5],"int")), "struct");
        }
        // Get product attributes
        
        debug('Begin Atributes');
            $prod_atrib = array();// If product has not attributes

            debug('Inicio atributos: ' . $row_product[0]);
            debug("Query: SELECT distinct p.products_id, op.products_options_id, op.products_options_name, op.language_id,     opv.products_options_values_id, opv.products_options_values_name, opv.language_id, pa.options_values_price 
                                     FROM products p, products_attributes pa, products_options op, products_options_values opv
                                     WHERE p.products_id = pa.products_id
                                     AND pa.options_id = op.products_options_id 
                                     AND op.language_id = opv.language_id
                                     AND op.language_id = 3 and opv.language_id = 3
                                     AND pa.options_values_id = opv.products_options_values_id 
                                     and p.products_id =". $row_product[0] . ";");

            $prod_atrib = array();// If product has not attributes
        
            $result_atrib = mysql_query("SELECT distinct p.products_id, op.products_options_id, op.products_options_name, op.language_id,     opv.products_options_values_id, opv.products_options_values_name, opv.language_id, pa.options_values_price 
                                     FROM products p, products_attributes pa, products_options op, products_options_values opv
                                     WHERE p.products_id = pa.products_id
                                     AND pa.options_id = op.products_options_id 
                                     AND op.language_id = opv.language_id
                                     AND op.language_id = 3 and opv.language_id = 3
                                     AND pa.options_values_id = opv.products_options_values_id 
                                     and p.products_id =". $row_product[0] . ";");
        if ($result_atrib) while ($rowatr = mysql_fetch_row($result_atrib)) {
   
            debug('Product atributes: '  . $rowatr[0] . ' ' . $rowatr[2]. ' ' . $rowatr[5] );
            $prod_atrib[] = new xmlrpcval(array(
                "products_id" => new xmlrpcval(clean_special_chars($rowatr[0]),"int"),
                "products_options_id" => new xmlrpcval(clean_special_chars($rowatr[1]),"int"),
                "products_options_name" => new xmlrpcval(clean_special_chars($rowatr[2]),"string"),
                "opt_language_id" => new xmlrpcval(clean_special_chars($rowatr[3]),"int"),
                "products_options_values_id" => new xmlrpcval(clean_special_chars($rowatr[4]),"int"),
                "opv.products_options_values_name" => new xmlrpcval(clean_special_chars($rowatr[5]),"string"),
                "opv_language_id" => new xmlrpcval(clean_special_chars($rowatr[6]),"int"),
                "options_values_price" => new xmlrpcval(clean_special_chars($rowatr[7]),"string"),
                                          ), "struct");
            
        }

        
        $products[] = new xmlrpcval(array(
            'product' => $prod,
            'product_description' => new xmlrpcval($prod_desc, "array"),
            'product_special' => $prod_spec,
            'manufacturers_url' => new xmlrpcval($manuf_url, "array"),
            'variants' => new xmlrpcval($prod_atrib, "array"),
            ), "struct");
    }
    debug('END-IF-WHILE-get_products');
    
    return new xmlrpcresp(new xmlrpcval($products, "array"));
}

function get_payment_methods() {
    $payment_methods = array();

    $result_modules = mysql_query("SELECT configuration_value FROM configuration WHERE (configuration_key = 'MODULE_PAYMENT_INSTALLED');");
    if ($result_modules && $row_modules=mysql_fetch_row($result_modules)) {
        $modules = explode(';', $row_modules[0]);
    }
    reset($modules);
    while (list($key, $value) = each($modules)) {
        include("../../includes/modules/payment/".$value);
        include("../../includes/languages/espanol/modules/payment/".$value);
        $class = substr($value, 0, strrpos($value, '.'));
        $obj = new $class();
        $payment_methods[] = new xmlrpcval(array(new xmlrpcval($key, "int"), new xmlrpcval(clean_special_chars($obj->title), "string")), "array");
    }
    return new xmlrpcresp( new xmlrpcval($payment_methods, "array"));
}

function get_shipping_methods() {
    $delivery_carriers = array();

    $result_modules = mysql_query("SELECT configuration_value FROM configuration WHERE (configuration_key = 'MODULE_SHIPPING_INSTALLED');");
    if ($result_modules && $row_modules=mysql_fetch_row($result_modules)) {
        $modules = explode(';', $row_modules[0]);
    }
    reset($modules);
    while (list($key, $value) = each($modules)) {
        include("../../includes/modules/shipping/".$value);
        include("../../includes/languages/espanol/modules/shipping/".$value);
        $class = substr($value, 0, strrpos($value, '.'));
        $obj = new $class();
        $delivery_carriers[] = new xmlrpcval(array(new xmlrpcval($key, "int"), new xmlrpcval(clean_special_chars($obj->title), "string")), "array");
    }
    return new xmlrpcresp( new xmlrpcval($delivery_carriers, "array"));
}

function search_payment_method($payment_name) {
    $languages = array();

    $result_modules = mysql_query("SELECT configuration_value FROM configuration WHERE (configuration_key = 'MODULE_PAYMENT_INSTALLED');");
    if ($result_modules && $row_modules = mysql_fetch_row($result_modules)) {
        $modules = explode(';', $row_modules[0]);
    }

    $result=mysql_query("select directory from languages;");
    if ($result) while ($row=mysql_fetch_row($result)) {
        $languages[] = $row[0];
    }

    reset($modules);
    while (list($key, $value) = each($modules)) {
        foreach ($languages as $lang) {
            $title = "";
            // We must extract the payment method name from the translation file of the payment module
            // We search lines containing the TEXT_TITLE constant like: define('MODULE_PAYMENT_COD_TEXT_TITLE', 'Cash on Delivery');
            $gestor = @fopen("../../includes/languages/$lang/modules/payment/$value", "r");
            if ($gestor) {
                while (!feof($gestor) and $title=="") {
                    // Read translation file line by line
                    $pieces = explode("'", fgets($gestor));
                    if (strpos($pieces[1], "TEXT_TITLE")) {
                        $title = $pieces[3];
                    }
                }
                fclose ($gestor);
            }
            if ($title == $payment_name) {
                return $key;
            }
        }
    }
    return 0;
}


function parent_category($id, $name) {
    $result = mysql_query("select parent_id from categories where categories_id=".$id.";");
    if ($result && $row = mysql_fetch_row($result)) {
        if ($row[0] == 0) {
            return $name;
        } else {
            $resultb = mysql_query("select min(language_id) from categories_description where categories_id=".$row[0].";");
            if ($resultb && $rowb=mysql_fetch_row($resultb)) {
                $resultb = mysql_query("select categories_name from categories_description where categories_id=".$row[0]." and language_id=".$rowb[0].";\n");
                if ($resultb && $rowb=mysql_fetch_row($resultb)) {
                    $name = parent_category($row[0], $rowb[0] . " \\ ". $name);
                    return $name;
                }
            }
        }
    }
    return $name;
}

function isTransactional() {
    return new xmlrpcresp(new xmlrpcval(TRANSACTIONAL,"boolean"));
}

function setSyncronizedFlag($product_id) {
	mysql_query("update products set products_syncronized = 1, products_last_syncronized = now() where products_id=" . $product_id . ";");
	return new xmlrpcresp(new xmlrpcval(true,"boolean"));
}

function set_product_stock($tiny_product) {
    mysql_query("update products set products_quantity=".$tiny_product['quantity']." where products_id=".$tiny_product['product_id'].";");
    mysql_query("update products set products_status=".(($tiny_product['quantity']>0)?1:0)." where products_id=".$tiny_product['product_id'].";");
    return new xmlrpcresp(new xmlrpcval(0,"int"));
}


function set_product_manufacturer($tiny_product) {
    $oscom_id = 0;

    if(array_key_exists('manufacturers_name',$tiny_product)) {
        $result = mysql_query("select l.languages_id from languages as l ,configuration as c where
        c.configuration_key='DEFAULT_LANGUAGE' and c.configuration_value=l.code;");

        if ($result && $row = mysql_fetch_row($result)) {
            $lang_id = $row[0];
        }
        $result = mysql_query("select manufacturers_id from manufacturers where (manufacturers_name='".$tiny_product['manufacturers_name']."');");
        if ($result && $row = mysql_fetch_row($result)) {
            $id_exist = 1;
            $oscom_id = $row[0];
        }
        if ($id_exist == 0) {
            mysql_query("insert into manufacturers (manufacturers_name, date_added) values ('".$tiny_product['manufacturers_name']."', now());");
            $oscom_id = mysql_insert_id();
            mysql_query("insert into manufacturers_info (manufacturers_id, languages_id,manufacturers_url) values (".$oscom_id.",".$lang_id.",'".$tiny_product['manufacturers_url']."');");
            foreach ($tiny_product['manufacturer_langs'] as $lang=>$values){
                mysql_query("insert into manufacturers_info (manufacturers_id, languages_id,manufacturers_url) values (".$oscom_id.",".$lang.",'".$values['manufacturers_url']."');");
            }
        } else {
            mysql_query("update manufacturers_info set manufacturers_url='".$tiny_product['manufacturers_url']."' where manufacturers_id=".$oscom_id." and languages_id=".$lang_id.";");
            foreach ($tiny_product['manufacturer_langs'] as $lang=>$values){
                mysql_query("delete from manufacturers_info where manufacturers_id=".$oscom_id." and languages_id=".$lang.";");
                mysql_query("insert into manufacturers_info (manufacturers_id, languages_id,manufacturers_url) values (".$oscom_id.",".$lang.",'".$values['manufacturers_url']."');");
            }
        }
    }
    return $oscom_id;
}


function remove_product($tiny_product) {

    if (array_key_exists('oscom_product_ids',$tiny_product)) {
        $i = 0;
        foreach($tiny_product['oscom_product_ids'] as $key=>$values) {
            if($i == 0) {
                $a .= $values;
            } else {
                $a .= ",".$values;
            }
            $i = $i + 1;
        }
        foreach(array('_description','_to_categories','') as $key) {
           // mysql_query("delete from products".$key." where products_id in (".$a.");");
        }
    }
    return new xmlrpcresp(new xmlrpcval(1, "int"));
}

function del_spe_price($tiny_val) {
    mysql_query("delete from specials where products_id = ".$tiny_val.";");
    return new xmlrpcresp(new xmlrpcval(1, "int"));
}

function set_product_spe($tiny_product) {
    $lang_id = 1;
    $id_exist = 0;
if (CREA_UPDATE==1){
    ////////Check for existance of product_id ///////////
    debug("localizando producto Oferta: select products_id from products where products_model='".$tiny_product['model']."'");
    $result = mysql_query("select products_id from products where (products_id=".$tiny_product['product_id'].");");
    if ($result && $row=mysql_fetch_row($result)) {
        $id_exist = 1;
    }

    $result = mysql_query("select l.languages_id from languages as l configuration as c where c.configuration_key='DEFAULT_LANGUAGE' and c.configuration_value = l.code;");

    if ($result && $row = mysql_fetch_row($result)) {
        $lang_id = $row[0];
    }
    //if ($tiny_product['quantity']>0) {
    //    $tiny_product['status']=1;
    //} else {
    //    $tiny_product['status']=0;
    //}
    $manufacturers_id = set_product_manufacturer($tiny_product);
    if ($id_exist == 0) {
        mysql_query("insert into products (products_quantity, products_model, products_price, products_weight, products_tax_class_id, products_status, manufacturers_id, products_date_added) values (".$tiny_product['quantity'].", '". $tiny_product['model']."', ".$tiny_product['price'].", ".$tiny_product['weight'].", ".$tiny_product['tax_class_id'].", ".$tiny_product['status'].", ".$manufacturers_id.", now());");

        $oscom_id = mysql_insert_id();
        if ( $tiny_product['date_available'] != 'NULL') {
            mysql_query("update products set products_date_available='".$tiny_product['date_available']."' where products_id=".$oscom_id.";");
        }
        mysql_query("insert into specials (products_id, specials_new_products_price, specials_date_added, date_status_change, status) values (".$oscom_id.",".$tiny_product['spe_price'].",now(),now(),".$tiny_product['spe_price_status'].");");
        if ( $tiny_product['exp_date'] != 'NULL') {
            mysql_query("update specials set expires_date='".$tiny_product['exp_date']."' where products_id=".$oscom_id.";");
        }
        mysql_query("insert into products_description (products_id, language_id, products_name, products_description, products_url) values (".$oscom_id.", ".$lang_id.", '".$tiny_product['name']."', '".$tiny_product['description']."', '".$tiny_product['url']."');");
        mysql_query("insert into products_to_categories (categories_id, products_id) values(".$tiny_product['category_id'].",".$oscom_id.");");
        foreach ($tiny_product['langs'] as $lang=>$values) {
            mysql_query("insert into products_description(products_id, language_id, products_name, products_description, products_url)
            values (".$oscom_id.", ".$lang.", '".$values['name']."', '".$values['description']."', '".$values['url']."');");
        }
    } else {
        debug("localizando producto Modelo existe: select products_id from products where products_id=".$tiny_product['product_id']);
        $result = mysql_query("select products_id from products where (products_id=".$tiny_product['product_id'].");");
        if ($result && $row=mysql_fetch_row($result)) {
            $id_exist = 1;
        }
        if ($id_exist){
        $oscom_id = $tiny_product['product_id'];
        foreach (array('quantity', 'price', 'weight', 'tax_class_id', 'status', 'date_available') as $key) {
            if ($key == 'date_available' and $tiny_product[$key] != 'NULL') {
                mysql_query("update products set products_".$key."='".$tiny_product[$key]."' where products_id=".$oscom_id.";");
            } else {
                mysql_query("update products set products_".$key."=".$tiny_product[$key]." where products_id=".$oscom_id.";");
            }
        }
        mysql_query("delete from specials where products_id=".$oscom_id.";");
        mysql_query("insert into specials (products_id, specials_new_products_price, specials_date_added, date_status_change, status) values (".$oscom_id.",".$tiny_product['spe_price'].",now(),now(),".$tiny_product['spe_price_status'].");");
        if ( $tiny_product['exp_date'] != 'NULL') {
            mysql_query("update specials set expires_date='".$tiny_product['exp_date']."' where products_id=".$oscom_id.";");
        }

        mysql_query("update products set products_model='".$tiny_product['model']."', manufacturers_id=".$manufacturers_id." where products_id=".$oscom_id.";");

        mysql_query("update products_to_categories set categories_id=".$tiny_product['category_id']." where products_id=".$oscom_id.";");
        foreach ($tiny_product['langs'] as $lang=>$values) {
            mysql_query("update products_description set ". 
                         " products_id  = " .  $oscom_id . 
                         ", language_id = ". $lang .
                         ", products_name = '".$values['name']."'" .
                         ", products_description =  '".$values['description']."'" .
                         ", products_url = '".$values['url']."'".
                         " where products_id=".$oscom_id." and language_id=".$lang.";");           
        }
    }
    }

    $cpt = 0;
    if ($tiny_product['haspic']==1) {
        if (file_exists('../../images/'.$cpt.'-'.$tiny_product['fname'])) {
            unlink('../../images/'.$cpt.'-'.$tiny_product['fname']); // DELETE THE EXISTING IMAGES
        }
        if ($hd = fopen('../../images/'.$cpt.'-'.$tiny_product['fname'], "w")) {
            fwrite($hd, base64_decode($tiny_product['picture']));
            fclose($hd);
            mysql_query("update products set products_image='".$cpt."-".$tiny_product['fname']."' where products_id=".$oscom_id.";");
        }
    } else if ($tiny_product['haspic']==2) {
        if (file_exists('../../images/'.$cpt.'-'.$tiny_product['fname'])) {
            unlink('../../images/'.$cpt.'-'.$tiny_product['fname']); // DELETE THE EXISTING IMAGES
        }
        mysql_query("update products set products_image='".$tiny_product['fname']."' where products_id=".$oscom_id.";");
    } else {
        mysql_query("update products set products_image=NULL where products_id=".$oscom_id.";");
    }
    return new xmlrpcresp(new xmlrpcval($oscom_id, "int"));
}
}
function set_product_classical($tiny_product) {
    $lang_id = 1;
    $id_exist = 0;
if (CREA_UPDATE==1){
    ////////Check for existance of product ///////////
    $result = mysql_query("select products_id from products where (products_id=".$tiny_product['product_id'].");");
    if ($result && $row=mysql_fetch_row($result)) {
        $id_exist = 1;
    }
    $result = mysql_query("select l.languages_id from languages as l configuration as c where c.configuration_key='DEFAULT_LANGUAGE' and c.configuration_value=l.code;");

    if ($result && $row = mysql_fetch_row($result)) {
        $lang_id = $row[0];
    }
    //if ($tiny_product['quantity']>0) {
    //    $tiny_product['status']=1;
    //} else {
    //    $tiny_product['status']=0;
    //}
    $manufacturers_id = set_product_manufacturer($tiny_product);
    if ($id_exist == 0) {
        mysql_query("insert into products (products_quantity, products_model, products_price, products_weight, products_tax_class_id, products_status, manufacturers_id, products_date_added) values (".$tiny_product['quantity'].", '". $tiny_product['model']."', ".$tiny_product['price'].", ".$tiny_product['weight'].", ".$tiny_product['tax_class_id'].", ".$tiny_product['status'].", ".$manufacturers_id.", now());");

        $oscom_id = mysql_insert_id();
        if ( $tiny_product['date_available'] != 'NULL') {
            mysql_query("update products set products_date_available='".$tiny_product['date_available']."' where products_id=".$oscom_id.";");
        }
        mysql_query("insert into products_description (products_id, language_id, products_name, products_description, products_url) values (".$oscom_id.", ".$lang_id.", '".$tiny_product['name']."', '".$tiny_product['description']."', '".$tiny_product['url']."');");
        mysql_query("insert into products_to_categories (categories_id, products_id) values(".$tiny_product['category_id'].",".$oscom_id.");");
        foreach ($tiny_product['langs'] as $lang=>$values) {
            mysql_query("insert into products_description(products_id, language_id, products_name, products_description, products_url)
            values (".$oscom_id.", ".$lang.", '".$values['name']."', '".$values['description']."', '".$values['url']."');");
        }
    } else {
        debug("localizando producto Modelo existe: select products_id from products where products_id=".$tiny_product['product_id']);
        $result = mysql_query("select products_id from products where (products_id=".$tiny_product['product_id'].");");
        if ($result && $row=mysql_fetch_row($result)) {
            $id_exist = 1;
        }
        if ($id_exist){
        
        $oscom_id = $tiny_product['product_id'];
        foreach (array('quantity', 'price', 'weight', 'tax_class_id', 'status', 'date_available') as $key) {
            if ($key == 'date_available' and $tiny_product[$key] != 'NULL') {
                mysql_query("update products set products_".$key."='".$tiny_product[$key]."' where products_id=".$oscom_id.";");
            } else {
                mysql_query("update products set products_".$key."=".$tiny_product[$key]." where products_id=".$oscom_id.";");
            }
        }

        mysql_query("update products set products_model='".$tiny_product['model']."', manufacturers_id=".$manufacturers_id." where products_id=".$oscom_id.";");

        mysql_query("update products_to_categories set categories_id=".$tiny_product['category_id']." where products_id=".$oscom_id.";");
        foreach ($tiny_product['langs'] as $lang=>$values) {
            mysql_query("update products_description set ". 
                         " products_id  = " .  $oscom_id . 
                         ", language_id = ". $lang .
                         ", products_name = '".$values['name']."'" .
                         ", products_description =  '".$values['description']."'" .
                         ", products_url = '".$values['url']."'".
                         " where products_id=".$oscom_id." and language_id=".$lang.";");           
        }
    }
    }
    $cpt = 0;
    if ($tiny_product['haspic']==1) {
        if (file_exists('../../images/'.$cpt.'-'.$tiny_product['fname'])) {
            unlink('../../images/'.$cpt.'-'.$tiny_product['fname']); // DELETE THE EXISTING IMAGES
        }
        if ($hd=fopen('../../images/'.$cpt.'-'.$tiny_product['fname'], "w")){
            fwrite($hd, base64_decode($tiny_product['picture']));
            fclose($hd);
            mysql_query("update products set products_image='".$cpt."-".$tiny_product['fname']."' where products_id=".$oscom_id.";");
        }
    } else if ($tiny_product['haspic']==2) {
        if (file_exists('../../images/'.$cpt.'-'.$tiny_product['fname'])) {
            unlink('../../images/'.$cpt.'-'.$tiny_product['fname']); // DELETE THE EXISTING IMAGES
        }
        mysql_query("update products set products_image='".$tiny_product['fname']."' where products_id=".$oscom_id.";");
    } else {
        mysql_query("update products set products_image=NULL where products_id=".$oscom_id.";");
    }
    return new xmlrpcresp(new xmlrpcval($oscom_id, "int"));
}
}

function get_order_address($address_condition, $oscom_id, $name, $street, $street2, $zip, $city, $state, $zone, $country, $email="", $phone="", $fax="") {
    $addresses = array();
    $num_rows = 0; 
    $query = "SELECT address_book_id,CONCAT(entry_firstname,' ',entry_lastname) as name, entry_street_address, entry_suburb, entry_postcode, entry_city, entry_state, entry_country_id, entry_zone_id FROM address_book";
    //debug("Init address controll:". $name . "-zip: ". $zip . "-city" . $city . "-state" . $state . "-country" . $country);

    if (is_array($address_condition)) {
        $where = " where ";
        $flag = true;
        foreach($address_condition as $key=>$values) {
            if ($flag) {
                if (!is_numeric($values)) {
                    $where.= "(" . $key."='".str_replace("'", "''", $values)."'" . " or isnull(" . $key . "))" ;
                } else {
                    $where.=$key."=".$values;
                }
                $flag=false;
            } else {
                if (!is_numeric($values)) {
                    $where.=" and "."(" . $key."='".str_replace("'", "''", $values)."'" . " or isnull(" . $key . "))" ;
                } else {
                    $where.=" and ".$key."=".$values;
                }
            }
        }
        debug("Localizando existe direccion: ". $query.$where);
        $result = mysql_query($query.$where);
        $num_rows = mysql_num_rows($result);
        debug("Existe direccion: ". $num_rows);
   }
    if ($num_rows>0) {
        debug("Localizada direccion cliente: ". $ret_address);
        return get_partner_address($address_condition,$email, $phone, $fax);
    }
    else {
        debug("Dirección cliente no localizada: ". $ret_address);

        $addresses = array();
        $country_data = get_country_detail($country);
        if ($state != '') {
            $state_name = $state;
        } else {
            $state_name = $zone;
        }
        $state_data = get_state_detail($country,$state_name);
        $ret_address = array(
            "esale_oscom_id" => new xmlrpcval($oscom_id,"int"),
            "name" => new xmlrpcval(clean_special_chars($name),"string"),
            "street" => new xmlrpcval(clean_special_chars($street),"string"),
            "street2" => new xmlrpcval(clean_special_chars($street2),"string"),
            "zip" => new xmlrpcval(clean_special_chars($zip),"string"),
            "city" => new xmlrpcval(clean_special_chars($city),"string"),
            "state" => $state_data,
            "country" => $country_data,
            "email" => new xmlrpcval(clean_special_chars($email),"string"),
            "phone" => new xmlrpcval(clean_special_chars($phone),"string"),
            "fax" => new xmlrpcval(clean_special_chars($fax),"string")
        );
        debug("No se ha localizado direccion cliente ");
        debug("Finalizada asignacion de direccion del pedido: ". $name . "-zip: ". $zip . "-city" . $city . "-state" . $state . "-country" . $country);

        $addresses[] = new xmlrpcval($ret_address,"struct");
    }
    return new xmlrpcval($addresses,"array");
}



function get_partner_address($address_condition, $email="", $phone="", $fax="") {
    $addresses = array();
    $query = "SELECT address_book_id,CONCAT(entry_firstname,' ',entry_lastname) as name, entry_street_address, entry_suburb, entry_postcode, entry_city, entry_state, entry_country_id, entry_zone_id FROM address_book";

    if (is_array($address_condition)) {
        $where = " where ";
        $flag = true;
        foreach($address_condition as $key=>$values) {
            if ($flag) {
                if (!is_numeric($values)) {
                    $where.= "(" . $key."='".str_replace("'", "''", $values)."'" . " or isnull(" . $key . "))" ;
                } else {
                    $where.=$key."=".$values;
                }
                $flag=false;
            } else {
                if (!is_numeric($values)) {
                    $where.=" and "."(" . $key."='".str_replace("'", "''", $values)."'" . " or isnull(" . $key . "))" ;
                } else {
                    $where.=" and ".$key."=".$values;
                }
            }
        }
        $result = mysql_query($query.$where);
        debug("Obteniendo direcciones en procedimiento habitual: ". $query.$where);
    }
    if ($result) while ($row_address=mysql_fetch_array($result, MYSQL_ASSOC)) {
        $country_data = get_country_detail($row_address['entry_country_id']);
        if ($row_address['entry_state'] != '') {
            $state_name = $row_address['entry_state'];
        } else {
            $state_name = $row_address['entry_zone_id'];
        }
        $state_data = get_state_detail($row_address['entry_country_id'],$state_name);
        $ret_address = array(
            "esale_oscom_id" => new xmlrpcval($row_address['address_book_id'],"int"),
            "name" => new xmlrpcval(clean_special_chars($row_address['name']),"string"),
            "street" => new xmlrpcval(clean_special_chars($row_address['entry_street_address']),"string"),
            "street2" => new xmlrpcval(clean_special_chars($row_address['entry_suburb']),"string"),
            "zip" => new xmlrpcval(clean_special_chars($row_address['entry_postcode']),"string"),
            "city" => new xmlrpcval(clean_special_chars($row_address['entry_city']),"string"),
            "state" => $state_data,
            "country" => $country_data,
            "email" => new xmlrpcval(clean_special_chars($email),"string"),
            "phone" => new xmlrpcval(clean_special_chars($phone),"string"),
            "fax" => new xmlrpcval(clean_special_chars($fax),"string")
        );
        debug("Direcciones retorno: ". $row_address['address_book_id']);

        $addresses[] = new xmlrpcval($ret_address,"struct");
    }
    return new xmlrpcval($addresses,"array");
}


function get_customer($cust_id) {
    $ret_partners = array();
    $condition = '';


    $query = "SELECT customers_id, CONCAT(customers_firstname,' ',customers_lastname) as name, customers_email_address, customers_default_address_id, customers_telephone, customers_fax from customers";

    if ($cust_id != 0) {
        $condition = " where customers_id=".$cust_id;
    }
    $result = mysql_query($query.$condition.';');
    debug("extrayendo cliente:" . $result);
    if ($result) while ($row_cust=mysql_fetch_array($result, MYSQL_ASSOC)) {
        $addresses = get_partner_address(array('customers_id'=>$row_cust['customers_id']));
        $partner = array();
        $partner['esale_oscom_id'] = new xmlrpcval($row_cust['customers_id'],"int");
		$partner['name'] = new xmlrpcval(clean_special_chars($row_cust['name']),"string");

//!!!!!!!!!!! BE CAREFULL, ENTRY_NIF is VAT NUMBER IN SPAIN, if you obtain
///// response error when executing sales order download, remove the field or addecuate the name
        $query_company = "select a.entry_nif, a.entry_company , a.entry_country_id, countries_iso_code_2, countries_name 
                              from address_book a, customers c, countries co
                              where a.entry_country_id = co.countries_id and c.customers_id = " . $row_cust['customers_id'] . " and a.address_book_id = c.customers_default_address_id;";
		debug($query_company);
        $result_company = mysql_query($query_company);
        if ($result_company) while ($row_nif=mysql_fetch_array($result_company, MYSQL_ASSOC)) {
                $cif_nif = str_replace(' ', '',str_replace('-', '',strtoupper($row_nif['entry_nif'])));
                debug( "TRATANDO NIF: " .  $row_nif['entry_nif'] . " -- Longitud: " . strlen($row_nif['entry_nif']) );        
                debug( "TRATANDO NIF: " .  $cif_nif . " -- Longitud: " . strlen($cif_nif) );        

			$paises9 = array('ES', 'DE','EL','PT');
			$paises10 = array('BE', 'RO','SK','PL');
			$paises11 = array('IT', 'RO','SK', 'FR');

			$pais = $row_nif['countries_iso_code_2'];
			debug ("PAIS:  ". $pais . '-' . $row_nif['countries_name']);
			if (in_array($pais, $paises9) and(strlen($cif_nif)==  9)) $p9=true;
			if (in_array($pais, $paises10)and(strlen($cif_nif)== 10)) $p10=true;
			if (in_array($pais, $paises11)and(strlen($cif_nif)== 11)) $p11=true;
			debug ("P9:  ". $p9);
			debug ("P10:  ". $p10);
			debug ("P11:  ". $p11);


            if ($p9 or $p10 or  $p11) {
                $partner['vat'] = new xmlrpcval($row_nif['countries_iso_code_2'] . clean_special_chars($cif_nif), "string");
                debug(  " -- NIF CORRECTO: " . $row_nif['countries_iso_code_2'] . $cif_nif);        
                debug(  " -- Nombre: " . $row_cust['name']);
                debug(  " -- Compania: " . $row_nif['entry_company'].  " -- IDCliente: " . $row_cust['customers_id'] . "\n");
            }else {
			    debug(  " -- ERROR EN NIF: " . "ES" . $cif_nif);
                $cif_nif = "01234567L";
                $partner['vat'] = new xmlrpcval("ES" . clean_special_chars($cif_nif), "string");               
                debug(  " -- Nombre: " . $row_cust['name']);
                debug(  " -- Compania " . $row_nif['entry_company'].  " -- IDCliente " . $row_cust['customers_id'] . "\n");
            }

            if ($row_nif['entry_company']!= '' ) {
                $partner['name'] = new xmlrpcval(clean_special_chars($row_nif['entry_company']),"string");
                debug(  "existe compania " . $row_nif['entry_company'] . "\n");
            }else{
                $partner['name'] = new xmlrpcval(clean_special_chars($row_cust['name']),"string");
                debug(  "NO existe compania " . $partner['company'] . "\n");
            }
        }
        $partner['addresses'] = $addresses;
        $ret_partners[] = new xmlrpcval($partner,"struct");
    }
   
    return new xmlrpcresp(new xmlrpcval($ret_partners,"array"));
}


function get_country_detail($country_name) {
    $query = "select countries_id, countries_name, countries_iso_code_2, countries_iso_code_3 from countries";
    $ret_country = '0';

    if (!is_numeric($country_name)) {
        if($country_name != '') {
            $result = mysql_query($query." where countries_name='".$country_name."';");
        }
    } else {
        $result = mysql_query($query." where countries_id=".$country_name.";");
    }
    if ($result && $row=mysql_fetch_row($result)) {
        $ret_country = new xmlrpcval( array (
            "esale_oscom_id" => new xmlrpcval($row[0],"int"),
            "name" => new xmlrpcval(clean_special_chars($row[1]),"string"),
            "code" => new xmlrpcval(clean_special_chars($row[2]),"string"),
            "code3" => new xmlrpcval(clean_special_chars($row[3]),"string")
        ),"struct");
        return $ret_country;
    }
    return new xmlrpcval($ret_country,'string');
}


function get_state_detail($country_id,$state_name) {
    $ret_state = '0';
    $query = "select zone_id, zone_code, zone_name from zones";
    $condition = '';

    if (!is_numeric($state_name)) {
        if ($state_name != '') {
            $condition = " where zone_name='".$state_name."' and zone_country_id=".$country_id;
        }
    } else {
        $condition = " where zone_id=".$state_name." and zone_country_id=".$country_id;
    }
    $result = mysql_query($query.$condition.";");
    if ($result && $row=mysql_fetch_row($result)) {
        $ret_state = new xmlrpcval( array (
            "esale_oscom_id" => new xmlrpcval($row[0],"int"),
            "name" => new xmlrpcval(clean_special_chars($row[2]),"string"),
            "code" => new xmlrpcval(clean_special_chars($row[1]),"string")
            ),"struct");
        return $ret_state;
    }
    $ret_state = new xmlrpcval( array (
        "esale_oscom_id" => new xmlrpcval(0,"int"),
        "name" => new xmlrpcval(clean_special_chars($state_name),"string"),
        "code" => new xmlrpcval('',"string")
    ),"struct");
    return $ret_state;
}


function get_saleorders($last_so, $statuses_ids) {
    $saleorders = array();
    $status_ids = implode(", ", $statuses_ids);


   debug("SELECT `orders_id` , `customers_name` , `customers_street_address` , `customers_city` , `customers_postcode` , `customers_state` , `customers_country` , `customers_telephone` , `customers_email_address` , `delivery_name` , `delivery_street_address` , `delivery_city` , `delivery_postcode` , `delivery_state` , `delivery_country` , `billing_name` , `billing_street_address` , `billing_city` , `billing_postcode` , `billing_state` , `billing_country` , `date_purchased` , `orders_status`, `customers_id`, `payment_method`, `customers_id`,`customers_company`,`delivery_company`,`billing_company` 
                FROM `orders` where (orders_id > ".$last_so." and orders_status in (" . $status_ids . ")) order by orders_id limit 1;");

    $result = mysql_query("SELECT `orders_id` , `customers_name` , `customers_street_address` ,  `customers_city` , `customers_postcode` , `customers_state` , `customers_country` , `customers_telephone` , `customers_email_address` , `delivery_name` , `delivery_street_address` , `delivery_city` , `delivery_postcode` , `delivery_state` , `delivery_country` , `billing_name` , `billing_street_address` , `billing_city` , `billing_postcode` , `billing_state` , `billing_country` , `date_purchased` , `orders_status`, `customers_id`, `payment_method`, `customers_id`,`customers_company`,`delivery_company`,`billing_company` ,`customers_suburb`,`delivery_suburb`,`billing_suburb` 
                        FROM `orders` where (orders_id > ".$last_so." and orders_status in (" . $status_ids . ")) order by orders_id limit 1;");

    $num_rows = mysql_num_rows($result);
    debug("Pedidos a descargar: " . $num_rows. "\n");
    debug("Ultimo Pedido que se descargo: " . $last_so . "\n");

    if ($result){
        while ($row = mysql_fetch_row($result)) {
            debug('Tratando Pedido: ' . $row[0]  . "\n");
            $shopping_price = 0;
            $result_shopping = mysql_query("SELECT value, title from orders_total where class='ot_shipping' and orders_id=".$row[0].";");
            if ($result_shopping && $row_shopping=mysql_fetch_row($result_shopping)) {
                $shopping_price = $row_shopping[0];
                $shipping_title = $row_shopping[1];
            }

            $result_customer = mysql_query("SELECT customers_email_address, customers_telephone, customers_fax FROM customers WHERE customers_id=".$row[25].";");
            if ($result_customer && $row_customer=mysql_fetch_row($result_customer)) {
                $email = $row_customer[0];
                $phone = $row_customer[1];
                $fax = $row_customer[2];
            }
            $default_condition = array("customers_id"=>$row[25],
                        "entry_company"=>$row[26],
                        "CONCAT(entry_firstname,' ',entry_lastname)"=>$row[1],
                        "entry_street_address"=>$row[2],
                        "entry_city"=>$row[3],
                        "entry_postcode"=>$row[4]
                        );
            $oscom_id = 9990;
            $name= $row[1];
            $street = $row[2];
            $street2 = $row[29];
            $city = $row[3];
            $zip = $row[4];
            $state = $row[5];
            $country = $row[6];
            $email = $row[7];
            $phone = $row[8];

            debug("Extrayendo direccion Defecto:". $default_condition . $oscom_id);
            debug("Pasando la direccion:". $name. $street. $street2. $city);
            $default_address =get_order_address($default_condition, $oscom_id, $name, $street, $street2, $zip, $city, $state, $zone, $country, $email, $phone, $fax);

            //$default_address = get_partner_address($default_condition, $email, $phone, $fax);

            $delivery_condition = array("customers_id"=>$row[25],
                        "entry_company"=>$row[26],
                        "CONCAT(entry_firstname,' ',entry_lastname)"=>$row[9],
                        "entry_street_address"=>$row[10],
                        "entry_city"=>$row[11],
                        "entry_postcode"=>$row[12]
                        );
            $oscom_id = 9991;
            $name= $row[9];
            $street = $row[10];
            $street2 = $row[30];
            $city = $row[11];
            $zip = $row[12];
            $state = $row[13];
            $country = $row[14];

            debug("Extrayendo direccion de envío:". $delivery_condition. $oscom_id);
            debug("Pasando la direccion:". $name. $street. $street2. $city);
            $delivery_address  =get_order_address($delivery_condition, $oscom_id, $name, $street, $street2, $zip, $city, $state, $zone, $country, $email, $phone, $fax);
            //$delivery_address = get_partner_address($delivery_condition, $email, $phone, $fax);

            $billing_condition = array("customers_id"=>$row[25],
                        "entry_company"=>$row[26],
                        "CONCAT(entry_firstname,' ',entry_lastname)"=>$row[15],
                        "entry_street_address"=>$row[16],
                        "entry_city"=>$row[17],
                        "entry_postcode"=>$row[18]
                        );
            $oscom_id = 9992;
            $name= $row[15];
            $street = $row[16];
            $street2 = $row[31];
            $city = $row[17];
            $zip = $row[18];
            $state = $row[19];
            $country = $row[20];

            debug("Extrayendo direccion de facturacion:". $billing_condition.$oscom_id);
            debug("Pasando la direccion:". $name. $street. $street2. $city);
            $billing_address  =get_order_address($billing_condition, $oscom_id, $name, $street, $street2, $zip, $city, $state, $zone, $country, $email, $phone, $fax);
            //$billing_address = get_partner_address($billing_condition, $email, $phone, $fax);

            $result_status = mysql_query("select orders_status_name from orders_status where orders_status_id = " . $row[22].";");
            if ($result_status && $row_status=mysql_fetch_row($result_status)) {
                        $status = $row_status[0];
            }
            $orderlines = array();
			$resultb = mysql_query("select products_id, products_quantity, products_price, products_tax, products_name, orders_products_id from orders_products where orders_id=".$row[0]." UNION select -1, 1, value, '18.0000', title, 0 from orders_total where class not in('ot_subtotal', 'ot_total', 'ot_tax') and orders_id=".$row[0].";");

			debug("query lineas:". "select products_id, products_quantity, products_price, products_tax, products_name, orders_products_id from orders_products where orders_id=".$row[0]." UNION select -1, 1, value, '18.0000', title, 0 from orders_total where class not in('ot_subtotal', 'ot_total', 'ot_tax') and orders_id=".$row[0].";");
            if ($resultb){
                while ($rowb = mysql_fetch_row($resultb)) {
				    debug("Extrayendo líneas:" . $rowb[0]."-". $rowb[1]."-".$rowb[2]. "-" . $rowb[3]); 

				    if ($rowb[3]>18) $rowb[3]=18;
                    $values_array = array("product_id" => new xmlrpcval($rowb[0], "int"),
                        "orders_products_id" => new xmlrpcval($rowb[5], "int"),
                        "product_qty" => new xmlrpcval($rowb[1], "int"),
                        "price" => new xmlrpcval($rowb[2], "double"),
                        "tax_rate" => new xmlrpcval($rowb[3],"double"),
                        "products_model" => new xmlrpcval(html_entity_decode(clean_special_chars($rowb[6])),"string"),
                        "name" => new xmlrpcval(html_entity_decode(clean_special_chars($rowb[4])),"string"));
                    $result_orders_product_attributes = mysql_query("select products_options, products_options_values, options_values_price, price_prefix from orders_products_attributes where orders_id=".$row[0]." and orders_products_id=".$rowb[5].";");
                    if($result_orders_product_attributes && $row_orders_product_attributes= mysql_fetch_row($result_orders_product_attributes)) {
                        //debug("En atributos línea:" . $row_orders_product_attributes[0]); 
                    if ($row_orders_product_attributes[3] !== '+' and $row_orders_product_attributes[3] !== '-'){$row_orders_product_attributes[3]='+';}

                        //debug("En atributos línea prefijo :" . $row_orders_product_attributes[3]); 
                        $num_atrib =  explode("-", clean_special_chars($row_orders_product_attributes[1])); 
                        $auxi_model = clean_special_chars($rowb[6]) . '-' . $num_atrib[0];

                        $orders_product_attributes = new xmlrpcval( array(
                            "products_options" => new xmlrpcval(clean_special_chars($row_orders_product_attributes[0]),"string"),
                            "products_options_values" => new xmlrpcval(clean_special_chars($row_orders_product_attributes[1]),"string"),
                            "options_values_price" => new xmlrpcval($row_orders_product_attributes[2],"double"),
                            "composed_code" => new xmlrpcval($auxi_model,"string"),
                            "price_prefix" => new xmlrpcval(clean_special_chars($row_orders_product_attributes[3]),"string")), "struct");
                        $values_array["attributes"] = $orders_product_attributes;
                    }
                    $orderlines[] = new xmlrpcval($values_array, "struct");
                }
            }
            $note = "";
            $result_comments = mysql_query("select comments FROM orders_status_history where (orders_id = ".$row[0]." and orders_status_id = 1);");
            if ($result_comments && $row_comments=mysql_fetch_row($result_comments)) {
                $note=$row_comments[0];
            }
//                $result_price_with_tax = mysql_query("SELECT configuration_value FROM configuration where (configuration_key = 'DISPLAY_PRICE_WITH_TAX');");
//                if ($result_price_with_tax && $row_price_with_tax=mysql_fetch_row($result_price_with_tax)) {
//                    if ($row_price_with_tax[0] == 'false') {
                    $price_type="tax_excluded";
//                    } else {
//                        $price_type="tax_included";
//                    }
//                }

            // Take the total information from oscommerce to bring to the OpenERP for the possiblity to use the oscommerce decimal calculattion in the OpenERP
            $order_subtotal = 0.0;
            $resultot_subtotal = mysql_query("select value from orders_total where class =  'ot_subtotal' and orders_id=".$row[0].";");
            if ($resultot_subtotal && $rowot_subtotal=mysql_fetch_row($resultot_subtotal)) {
                $order_subtotal=$rowot_subtotal[0];
            }
            $order_tax = 0.0;
            $resultot_tax = mysql_query("select value from orders_total where class =  'ot_tax' and orders_id=".$row[0].";");
            if ($resultot_tax && $rowot_tax=mysql_fetch_row($resultot_tax)) {
                $order_tax=$rowot_tax[0];
            }
            $order_total = 0.0;
            $resultot_total = mysql_query("select value from orders_total where class =  'ot_total' and orders_id=".$row[0].";");
            if ($resultot_total && $rowot_total=mysql_fetch_row($resultot_total)) {
                $order_total=$rowot_total[0];
            }

            $saleorders[] = new xmlrpcval( array("id" => new xmlrpcval( $row[0], "int"),
                "price_type" => new xmlrpcval( clean_special_chars($price_type), "string" ),
                "note" => new xmlrpcval(clean_special_chars($note), "string" ),
                "lines" => new xmlrpcval( $orderlines, "array"),
                "pay_met" => new xmlrpcval( search_payment_method($row[24]), "int"),
                "pay_met_title" => new xmlrpcval( clean_special_chars($row[24]), "string"),
                "shipping_price" => new xmlrpcval( $shopping_price, "double"),
                "shipping_title" => new xmlrpcval(html_entity_decode(clean_special_chars($shipping_title)), "string"),
                "orders_status" => new xmlrpcval( clean_special_chars($status), "string"),
                "partner" => get_customer($row[25]),
                "date" => new xmlrpcval( $row[21], "string"),
                "address" => $default_address,
                "delivery" => $delivery_address,
                "billing" => $billing_address,
                "order_subtotal" => new xmlrpcval($order_subtotal, "double"),
                "order_tax" => new xmlrpcval($order_tax, "double"),
                "order_total" => new xmlrpcval($order_total, "double"),
            ), "struct");
        }
    }
    return new xmlrpcresp(new xmlrpcval($saleorders, "array"));
}


function get_min_open_orders($last_so) {
    $result = mysql_query("SELECT min(`orders_id`) as min FROM `orders` where (orders_id <= ".$last_so.") and (orders_status = 2);");
    if ($result) {
        $min = mysql_fetch_row($result);
        return new xmlrpcresp( new xmlrpcval($min[0], "int"));
    } else
            return new xmlrpcresp( new xmlrpcval(-1, "int"));
}



function get_max_products_id() {
    $result = mysql_query("SELECT max(`products_id`) as max FROM `products`;");
    if ($result) {
        $max = mysql_fetch_row($result);
        return new xmlrpcresp( new xmlrpcval($max[0], "int"));
    } else
            return new xmlrpcresp( new xmlrpcval(-1, "int"));
}

function get_min_products_id() {
    $result = mysql_query("SELECT min(`products_id`) as min FROM `products`;");
    if ($result) {
        $min = mysql_fetch_row($result);
        return new xmlrpcresp( new xmlrpcval($min[0], "int"));
    } else
        return new xmlrpcresp( new xmlrpcval(-1, "int"));
}


function close_open_orders($order_id, $order_status_id) {
    mysql_query("update orders set orders_status= " . $order_status_id . " where orders_id=".$order_id.";");
    return new xmlrpcresp(new xmlrpcval(0, "int"));
}


function process_order($order_id, $order_status_id) {
          debug("ONPROCESS: update orders set orders_status = " . $order_status_id . " where orders_id = ".$order_id.";");

    mysql_query("update orders set orders_status= " . $order_status_id . "  where orders_id=".$order_id.";");
    return new xmlrpcresp(new xmlrpcval(0, "int"));
}


function update_order_status($order_id, $order_status_id, $status_comment, $update_comment, $send_web_email) {
     
      $oID = $order_id;
    
      mysql_query("update orders set orders_status = '" . $order_status_id . "', last_modified = now() where orders_id = '" . (int)$oID . "'");
      $customer_notified = $send_web_email;

    if ($update_comment){
          debug("ACTUALIZAR COMENTARIOS insert into orders_status_history (orders_id, orders_status_id, date_added, customer_notified, comments) values ('" . (int)$oID . "', '" . $order_status_id . "', now(), '1', '" . $status_comment  . "')");
          mysql_query("insert into orders_status_history (orders_id, orders_status_id, date_added, customer_notified, comments) values ('" . (int)$oID . "', '" . $order_status_id . "', now(), '". $customer_notified . "', '" . $status_comment  . "')");
    }else {
          debug("NO ACTUALIZAR COMENTARIOS insert into orders_status_history (orders_id, orders_status_id, date_added, customer_notified, comments) values ('" . (int)$oID . "', '" . $order_status_id . "', now(), '1', '')");
         mysql_query("insert into orders_status_history (orders_id, orders_status_id, date_added, customer_notified, comments) values ('" . (int)$oID . "', '" . $order_status_id . "', now(), '". $customer_notified . "', '')");
    }

    if ($send_web_email) {
          $check_status_query = mysql_query("select customers_name, customers_email_address, orders_status, date_purchased 
                                             from orders where orders_id = '" . (int)$oID . "'");

    if ($check_status_query && $check_status=mysql_fetch_row($check_status_query)) {
        debug("ONCHANGEORDER1: en envio e-mail;");
        $email = $status_comment ;

        debug("ONCHANGEORDER2: " . $email);
    //    $headers = "From: \r\n";
    //  mail($check_status['customers_email_address'],'Subject', $email, $headers );
 

        debug("ONCHANGEORDER: en envio e-mail;");
      }
    } else {
        debug("ONCHANGEORDER: en NO envio e-mail;");
    }
    debug("ONCHANGEORDER: FINAL PROCEDIMIENTO;");

    return new xmlrpcresp(new xmlrpcval(0, "int"));
}

$server = new xmlrpc_server( array(    "get_taxes" => array(        "function" => "get_taxes",
                                                                "signature" => array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                       "get_statuses" => array(        "function" => "get_statuses",
                                                                "signature" => array(    array($xmlrpcArray)
                                                                                    )
                                                                ),

                                    "get_languages" => array(    "function" =>    "get_languages",
                                                                "signature" => array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_categories" => array(    "function" =>    "get_categories",
                                                                "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_categories_parent" => array(    "function" =>    "get_categories_parent",
                                                                "signature" =>    array(    array($xmlrpcArray, $xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_products" => array(    "function" =>    "get_products",
                                                                "signature" =>    array(    array($xmlrpcArray, $xmlrpcArray, $xmlrpcInt, $xmlrpcInt, $xmlrpcString)
                                                                                    )
                                                                ),                                                                                                                        
                                    "get_payment_methods" => array(    "function" =>    "get_payment_methods",
                                                                    "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_shipping_methods" => array(    "function" =>    "get_shipping_methods",
                                                                    "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_saleorders" => array(    "function" =>    "get_saleorders",
                                                                "signature" =>    array(    array($xmlrpcArray, $xmlrpcInt ,$xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_min_products_id" => array( "function" =>   "get_min_products_id",
                                                                "signature" =>  array(  array($xmlrpcInt)
                                                                                    )
                                                                ),                                                                                                                                      
                                    "get_max_products_id" => array( "function" =>   "get_max_products_id",
                                                                "signature" =>  array(  array($xmlrpcInt)
                                                                                    )
                                                                ),                                                                   
                                    "get_min_open_orders" => array(    "function" =>    "get_min_open_orders",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "set_product_spe" => array(        "function" =>    "set_product_spe",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcStruct)
                                                                                    )
                                                                ),
                                    "set_product_classical" => array(        "function" =>    "set_product_classical",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcStruct)
                                                                                    )
                                                                ),
                                    "remove_product" => array(        "function" =>    "remove_product",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcStruct)
                                                                                    )
                                                                ),
                                    "del_spe_price" => array(        "function" =>    "del_spe_price",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "update_order_status" => array(        "function" =>    "update_order_status",
                                                                "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt, $xmlrpcInt, $xmlrpcString, $xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),

                                    "isTransactional" => array(	"function" =>	"isTransactional",
                                                                "signature" =>	array(	array($xmlrpcBoolean)
                                                                                    )
                                                                ),
                                    "setSyncronizedFlag" => array(	"function" =>	"setSyncronizedFlag",
                                                                 "signature" =>	array(	array($xmlrpcBoolean, $xmlrpcInt)
                                                                                   )
                                                                ),
                                    "set_product_stock" => array(	"function" =>	"set_product_stock",
                                                                        "signature" =>	array(	array($xmlrpcInt, $xmlrpcStruct)
                                                                                   )
                                                                ),
                                    "process_order" => array(        "function" =>    "process_order",
                                                                    "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "close_open_orders" => array(    "function" =>    "close_open_orders",
                                                                    "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "get_customer" => array(    "function" =>    "get_customer",
                                                                    "signature" =>    array(    array($xmlrpcArray, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "get_m2m_cat" => array(    "function" =>    "get_m2m_cat",
                                                                    "signature" =>    array(    array($xmlrpcArray, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "set_m2m_cat" => array(    "function" =>    "set_m2m_cat",
                                                                    "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt, $xmlrpcArray)
                                                                                    )
                                                                ),
									"get_extra_fields" => array(    "function" =>    "get_extra_fields",
                                                                     "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_products_extra_fields_values" => array(    "function" =>    "get_products_extra_fields_values",
                                                                     "signature" =>    array(    array($xmlrpcArray, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    "set_products_extra_fields_values" => array(    "function" =>    "set_products_extra_fields_values",
                                                                     "signature" =>    array(    array($xmlrpcInt, $xmlrpcInt, $xmlrpcStruct)
                                                                                    )
                                                                ),
                                    "get_options" => array(    "function" =>    "get_options",
                                                                     "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_options_values" => array(    "function" =>    "get_options_values",
                                                                     "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_attributes" => array(    "function" =>    "get_attributes",
                                                                     "signature" =>    array(    array($xmlrpcArray)
                                                                                    )
                                                                ),
                                    "get_products_attributes" => array(    "function" =>    "get_products_attributes",
                                                                     "signature" =>    array(    array($xmlrpcArray,$xmlrpcInt)
                                                                                    )
                                                                ),
                                    "get_saleorderline_attributes" => array(    "function" =>    "get_saleorderline_attributes",
                                                                     "signature" =>    array(    array($xmlrpcString, $xmlrpcInt, $xmlrpcInt)
                                                                                    )
                                                                ),
                                    ), false);
$server->functions_parameters_type = 'phpvals';
$server->response_charset_encoding = RESPONSE_ENCODING;
$server->service();
?>
