odoo.define("access_apps.dashboard", function(require) {
    "use strict";

    var dashboard = require("web_settings_dashboard");

    var def = $.Deferred();

    dashboard.Dashboard.include({
        start: function() {
            return this._super().then(function() {
                def.resolve();
            });
        },

        load_apps: function(data) {
            if (data.has_access_to_apps) {
                return this._super(data);
            }
            this.$(".o_web_settings_dashboard_apps").remove();
            return $.when();
        },
    });
    return {ready: def};
});
