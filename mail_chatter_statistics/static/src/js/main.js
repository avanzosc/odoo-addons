odoo.define("mail_chatter_statistics.main", function (require) {
  "use strict";

  const rpc = require("web.rpc");

  const Message = require("mail/static/src/components/message/message.js");

  let statisticsInitialized = false;

  const OriginalMounted = Message.prototype.mounted;

  Message.prototype.mounted = async function () {
    if (!statisticsInitialized) {
      statisticsInitialized = true;

      const parentGroups = document.querySelectorAll(
        `div[role="group"][data-message-local-id^="mail.message_"]`
      );
      if (parentGroups.length) {
        for (const parentGroup of parentGroups) {
          const dataMessageLocalId = parentGroup.getAttribute("data-message-local-id");
          const mailMessageId = dataMessageLocalId?.split("_")[1];

          if (mailMessageId) {
            try {
              const mailingTrace = await this.getMailingTrace(mailMessageId);
              updateMailingTraceInDOM(mailingTrace, parentGroup);
            } catch (error) {
              console.error("Error fetching mailing trace:", error);
            }
          } else {
            console.warn(
              "No valid mailMessageId found in data-message-local-id:",
              dataMessageLocalId
            );
          }
        }
      }
    }

    if (OriginalMounted) {
      OriginalMounted.call(this);
    }
  };

  Message.prototype.getMailingTrace = function (mailMessageId) {
    return rpc
      .query({
        model: "mail.message",
        method: "get_mailing_trace",
        args: [mailMessageId],
      })
      .then(function (result) {
        return result;
      })
      .catch(function (error) {
        console.error("Error al obtener el mailing trace:", error);
        return {};
      });
  };

  function updateMailingTraceInDOM(mailingTrace, parentGroup) {
    const row = parentGroup.querySelector(".your-mailing-trace-ids-selector .row");

    if (row) {
      row.children[0].innerHTML =
        mailingTrace && mailingTrace.sent_at
          ? createHoverText(mailingTrace.sent_at)
          : "";
      row.children[1].innerHTML =
        mailingTrace && mailingTrace.clicked_at
          ? createHoverText(mailingTrace.clicked_at)
          : "";
      row.children[2].innerHTML =
        mailingTrace && mailingTrace.opened_at
          ? createHoverText(mailingTrace.opened_at)
          : "";
      row.children[3].innerHTML =
        mailingTrace && mailingTrace.bounced_at
          ? createHoverText(mailingTrace.bounced_at)
          : "";
      row.children[4].innerHTML =
        mailingTrace && mailingTrace.replied_at
          ? createHoverText(mailingTrace.replied_at)
          : "";
    }
  }

  function createHoverText(dateTime) {
    const date = new Date(dateTime);
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const fullDate = date.toLocaleDateString(); // Get the full date

    return `
      <span class="time" title="${fullDate}">${hours}:${minutes}</span>
    `;
  }
});
