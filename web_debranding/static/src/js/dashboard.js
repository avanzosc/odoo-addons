/*  Copyright 2015-2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    Copyright 2017 ArtyomLosev <https://github.com/ArtyomLosev>
    Copyright 2017 Ildar Nasyrov <https://it-projects.info/team/iledarn>
    License MIT (https://opensource.org/licenses/MIT). */
odoo.define("web_debranding.dashboard", function (require) {
    "use strict";

    var dashboard = require("web_settings_dashboard");
    dashboard.Dashboard.include({
        start: function () {
            this.all_dashboards = _.without(this.all_dashboards, "share");

            // Remove Share section completly
            this.$(".o_web_settings_dashboard_share").parent().remove();

            var self = this;
            return this._super().then(function () {
                // Remove bottom of Apps settion (links to odoo apps store)
                self.$(".o_browse_apps").parent().nextAll().remove();
            });
        },
    });
});
