odoo.define("cleaning_database_operations.cleanup_progress", function (require) {
  "use strict";

  var WebClient = require("web.WebClient");
  var session = require("web.session");

  WebClient.include({
    start: function () {
      var result = this._super.apply(this, arguments);

      this._cleanupProgressChannel = JSON.stringify([
        session.db,
        "cleaning.database.progress",
        session.uid,
      ]);

      this._cleanupProgressNotificationId = false;

      this.call("bus_service", "addChannel", this._cleanupProgressChannel);

      this.call(
        "bus_service",
        "onNotification",
        this,
        this._onCleanupProgressNotification
      );

      return result;
    },

    _onCleanupProgressNotification: function (notifications) {
      var self = this;

      _.each(notifications, function (notification) {
        var channel = notification[0];
        var payload = notification[1];

        if (channel !== self._cleanupProgressChannel) {
          return;
        }

        if (!payload || payload.type !== "cleaning_database_progress") {
          return;
        }

        if (self._cleanupProgressNotificationId) {
          var previousNotificationId = self._cleanupProgressNotificationId;

          self._cleanupProgressNotificationId = false;

          // Odoo 14 returns the notification id before the
          // notification widget has necessarily finished rendering.
          // Do not close it immediately or $el may not exist yet.
          setTimeout(function () {
            self.call("notification", "close", previousNotificationId);
          }, 250);
        }

        var notificationId = self.displayNotification({
          title: payload.title || "Database Cleanup",
          message: payload.message || "",
          type: payload.notification_type || "info",
          sticky: !payload.finished,
        });

        if (!payload.finished) {
          self._cleanupProgressNotificationId = notificationId;
        }
      });
    },
  });
});
