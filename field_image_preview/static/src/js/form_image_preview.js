
odoo.define('field_image_preview.image_widget_extend', function (require) {
"use strict";

    var base_f = require('web.basic_fields')
	var imageWidget = base_f.FieldBinaryImage
    var DocumentViewer = require('mail.DocumentViewer');
    var field_utils = require('web.field_utils');

imageWidget.include({

    _render: function () {
        this._super.apply(this, arguments);
        var self = this;
        this.$("img").click(function(e) {
            console.log(self);
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
            var attachmentViewer = new DocumentViewer(self, attachments, source_id);
            attachmentViewer.appendTo($('body'));
        });
    },
});
});

