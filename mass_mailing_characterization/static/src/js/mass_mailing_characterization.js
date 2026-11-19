// Copyright 2019 Roberto Lizana - Trey, Jorge Camacho - Trey
// License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
odoo.define('web_editor.backend', function (require) {
    'use strict'

    var AbstractField = require('web.AbstractField')
    var basic_fields = require('web.basic_fields')
    var config = require('web.config')
    var core = require('web.core')
    var session = require('web.session')
    var field_registry = require('web.field_registry')
    var SummernoteManager = require('web_editor.rte.summernote')
    var transcoder = require('web_editor.transcoder')

    var FieldTextHtml = field_registry.get('html_frame').extend({
        getDatarecord: function () {
            let data = Object.assign({}, this.recordData)
            let removeProperty = ((key) => {
                if (data.hasOwnProperty(key)) {
                    delete data[key]
                }
            })
            removeProperty('area_ids')
            removeProperty('featured_post_ids')
            removeProperty('post_ids')
            removeProperty('post_line_ids')
            removeProperty('post_state')
            return data
        }
    })

    field_registry
        .add('html_frame', FieldTextHtml)
    return {
        FieldTextHtml: FieldTextHtml}
});
