openerp.pos_discount_extra = function(instance){
    var module   = instance.point_of_sale;
    var round_pr = instance.web.round_precision;
    var QWeb = instance.web.qweb;

    QWeb.add_template('/pos_discount_extra/static/src/xml/discount.xml');

    module.PosWidget.include({
        build_widgets: function(){
            var self = this;
            this._super();

            if ((!this.pos.config.discount2_product_id) &&
            		(!this.pos.config.discount3_product_id)){
                return;
            }
            var discount2 = $(QWeb.render('Discount2Button'));
            var discount3 = $(QWeb.render('Discount3Button'));
            if(this.pos.config.discount2_product_id){
	            discount2.click(function(){
	                var order    = self.pos.get('selectedOrder');
	                var product  = self.pos.db.get_product_by_id(self.pos.config.discount2_product_id[0]);
	                var disc2 = - self.pos.config.discount2_pc/ 100.0 * order.getTotalTaxIncluded();
	                if( disc2 < 0 ){
	                    order.addProduct(product, { price: disc2 });
	                }
	            });
	            discount2.appendTo(this.$('.control-buttons'));
            }
            if(this.pos.config.discount3_product_id){
	            discount3.click(function(){
	                var order    = self.pos.get('selectedOrder');
	                var product  = self.pos.db.get_product_by_id(self.pos.config.discount3_product_id[0]);
	                var disc3 = - self.pos.config.discount3_pc/ 100.0 * order.getTotalTaxIncluded();
	                if( disc3 < 0 ){
	                    order.addProduct(product, { price: disc3 });
	                }
	            });
	            discount3.appendTo(this.$('.control-buttons'));
            }
        }
    });

};

