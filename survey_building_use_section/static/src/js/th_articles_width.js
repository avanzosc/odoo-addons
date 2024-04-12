odoo.define('survey_building_use_section.th_articles_width', function (require) {
    "use strict";

    var core = require('web.core');
    var SurveyForm = require('survey.form');

    var ThArticlesWidth = SurveyForm.include({

        events: _.extend({}, SurveyForm.prototype.events, {
            'click tr': '_onClickTableRow'
        }),

        _onClickTableRow: function (ev) {
            this._super.apply(this, arguments); // Call parent method
            if (this.modelName === 'survey.survey') {
                var target = ev.target;
                if (target.tagName === 'TR') {
                    var thElements = document.getElementsByTagName('th');
                    for (var i = 0; i < thElements.length; i++) {
                        if (thElements[i].getAttribute('data-name') === "question_article_ids") {
                            var currentStyle = thElements[i].getAttribute('style');
                            if (currentStyle) {
                                thElements[i].style.width = (parseInt(thElements[i].style.width) + 500) + 'px';
                            } else {
                                thElements[i].style.width = '500px';
                            }
                        } else if (thElements[i].getAttribute('data-name') === "value") {
                            var currentStyle = thElements[i].getAttribute('style');
                            if (currentStyle) {
                                thElements[i].style.width = (parseInt(thElements[i].style.width) - 400) + 'px';
                            } else {
                                thElements[i].style.width = '100px';
                            }
                        }
                    }
                }
            }
        },
    });

    return ThArticlesWidth;

});
