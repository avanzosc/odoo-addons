odoo.define('swipe_images_backend', function(require) {
    var base_f = require('web.basic_fields');
    var imageWidget = base_f.FieldBinaryImage;

    var DocumentViewer = require('mail.DocumentViewer');
    var field_utils = require('web.field_utils');

    imageWidget.include({
        _render: function() {
            var self = this;
            this._super.apply(this, arguments);
            if (this.mode === 'readonly') {
                var swiper = null;
                // if set options 'swipe_field'
                if (this.attrs.options.swipe_field){
                    if (this.recordData[this.attrs.options.swipe_field]) {
                        var related = this.recordData[this.attrs.options.swipe_field];
                        var product_image_ids = this.recordData[this.attrs.options.swipe_field].data;
                        var time = new Date().getTime().toString();
                        var width = this.nodeOptions.size ? this.nodeOptions.size[0] : this.attrs.width;
                        var height = this.nodeOptions.size ? this.nodeOptions.size[1] : this.attrs.height;
                        if (!width)
                            width = 90;
                        if (!height)
                            height = 90;
/*                        console.log($(this.$el[0]).scrollWidth)
                        console.log($(this.$el[0]).height())
                        console.log(this.$el)
                        console.log(this.el)
                        console.log(this.el.width)
                        console.log($(this.el).width())*/

                        for (var i = 0; i < product_image_ids.length; i++){
                            // base64 image data
                            console.log(this, "this");
                            var img = jQuery('<img/>', {
                                id: i.toString(),
                                'data-id': product_image_ids[i].data.id,
                                //src: 'data:image/;base64,' + product_image_ids[i].data.image,
                                src: '/web/image?model='+related.model+ "&field=image&id=" + JSON.stringify(product_image_ids[i].data.id) + "&unique=" + time+'&width='+width+'&height='+ height +"#"
                            });
                            if (width) {
                                img.attr('width', width);
                                img.css('max-width', width + 'px');
                            }
                            if (height) {
                                img.attr('height', height);
                                img.css('max-height', height + 'px');
                            }
                            img.appendTo(self.$('.img.img-fluid'));

                        }

                        if(self.$('.img.img-fluid').length && self.$('.img.img-fluid').parent())
                            swiper = self.$('.img.img-fluid').parent().brazzersCarousel();
                    }
                }
                // default work for product model
                else {
                    if (this.recordData.product_image_ids) {
                        var related = this.recordData.product_image_ids;
                        var product_image_ids = this.recordData.product_image_ids.data;
                        var time = new Date().getTime().toString();
                        var width = this.nodeOptions.size ? this.nodeOptions.size[0] : this.attrs.width;
                        var height = this.nodeOptions.size ? this.nodeOptions.size[1] : this.attrs.height;
                        if (!width)
                            width = 90;
                        if (!height)
                            height = 90;

                        for (var i = 0; i < product_image_ids.length; i++){
                            // base64 image data
                            var img = jQuery('<img/>', {
                                id: i.toString(),
                                'data-id': product_image_ids[i].data.id,
                                src: '/web/image?model='+related.model+ "&field=image&id=" + JSON.stringify(product_image_ids[i].data.id) + "&unique=" + time +'&width='+width+'&height='+ height +"#"
                            });
                            if (width) {
                                img.attr('width', width);
                                img.css('max-width', width + 'px');
                            }
                            if (height) {
                                img.attr('height', height);
                                img.css('max-height', height + 'px');
                            }
                            img.appendTo(self.$('.img.img-fluid'));

                        }

                        if(self.$('.img.img-fluid').length && self.$('.img.img-fluid').parent())
                            swiper = self.$('.img.img-fluid').parent().brazzersCarousel();
                    }
                }

            //swipe click handle
            if (swiper)
                swiper.parent().click(function(e) {
                    var current_div = $(this).find("div.active");
                    var all_img = $(this).closest(".brazzers-daddy").find("img");
                    var current_img = all_img.eq(current_div.index());

                    // default block preview 1 photo
                    var name_field = self.name;
                    if (name_field == "image_medium" ||
                        name_field == "image_small")
                        name_field = "image";
                    // unique forces a reload of the image when the record has been updated
                    var source_id = self.model + "/" + JSON.stringify(self.res_id) + "/" + name_field
                        + "?unique="+ field_utils.format.datetime(self.recordData.__last_update).replace(/[^0-9]/g, '')+"#";
                    var attachments = [{
                        "filename": self.recordData.display_name ,
                        "id": source_id,
                        "is_main": true,
                        "mimetype": "image/jpeg",
                        "name": self.recordData.display_name + " " + self.value,
                        "type": "image",
                    }];


                    // if from related field
                    if (self.attrs.options.swipe_field && self.recordData[self.attrs.options.swipe_field]){
                        var related = self.recordData[self.attrs.options.swipe_field];
                        var time = new Date().getTime().toString();
                        // if click non first image
                        if (current_img.data('id') >= 0 )
                        	var source_id =  '?model='+related.model+ "&field=image&id=" + JSON.stringify(current_img.data('id')) + "&unique=" + time+"#";

                        var product_image_ids = self.recordData[self.attrs.options.swipe_field].data;
                        for (var i = 0; i < product_image_ids.length; i++){
                        	attachments.push({
                            "filename": i,
                            "id": '?model='+related.model+ "&field=image&id=" + JSON.stringify(product_image_ids[i].data.id) + "&unique=" + time+"#",
                            "is_main": true,
                            "mimetype": "image/jpeg",
                            "name": self.attrs.options.swipe_field,
                            "type": "image",
                        	})
                    	}
                    }
                    // if from product
                    else {
                        if (self.recordData.product_image_ids){
                            var related = self.recordData.product_image_ids;
                            var time = new Date().getTime().toString();
                            // if click non first image
                            if (current_img.data('id') >= 0 )
                            	var source_id =  "?model=product.image&field=image&id=" + JSON.stringify(current_img.data('id')) + "&unique=" + time+"#";

                            var product_image_ids = self.recordData.product_image_ids.data;
                            for (var i = 0; i < product_image_ids.length; i++){
                            	attachments.push({
                                "filename": i,
                                "id": "?model=product.image&field=image&id=" + JSON.stringify(product_image_ids[i].data.id) + "&unique=" + time+"#",
                                "is_main": true,
                                "mimetype": "image/jpeg",
                                "name": "product_image_ids",
                                "type": "image",
                            	})
                    		}
                        }
                    }

                    var attachmentViewer = new DocumentViewer(self, attachments, source_id);
                    attachmentViewer.appendTo($('body'));
                });
            }

        }
    });

});