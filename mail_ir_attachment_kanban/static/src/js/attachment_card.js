/** @odoo-module **/

odoo.define("mail_ir_attachment_kanban.AttachmentCardHoverInfo", function (require) {
  "use strict";

  const {patch} = require("@web/core/utils/patch");
  const {AttachmentCard} = require("@mail/components/attachment_card/attachment_card");
  const {onMounted} = require("@odoo/owl");

  patch(AttachmentCard.prototype, "mail_ir_attachment_kanban.AttachmentCardHoverInfo", {
    setup() {
      this._super(...arguments);

      onMounted(() => {
        this._bindHoverEvent();
      });
    },

    _bindHoverEvent() {
      const attachmentId = this.props.record.attachment.id;
      if (!attachmentId) {
        return;
      }

      const attachmentCard = document.querySelector(
        `.o_AttachmentCard[attachment-id="${attachmentId}"]`
      );
      if (!attachmentCard) {
        return;
      }

      attachmentCard.addEventListener("mouseenter", () => {
        this._onHoverStart(attachmentId, attachmentCard);
      });

      attachmentCard.addEventListener("mouseleave", () => {
        this._onHoverEnd();
      });
    },

    async _onHoverStart(attachmentId, attachmentCard) {
      if (!attachmentId) {
        return;
      }
      await this._fetchAttachmentInfo(attachmentId, attachmentCard);
    },

    _onHoverEnd() {
      this._hideTooltip();
    },

    async _fetchAttachmentInfo(attachmentId, attachmentCard) {
      try {
        const attachmentData = await this.env.services.orm.call(
          "ir.attachment",
          "read",
          [[attachmentId], ["create_date", "create_uid", "write_date", "write_uid"]],
          {}
        );

        if (attachmentData && attachmentData.length > 0) {
          const attachment = attachmentData[0];
          const info = `
          <strong>Creado:</strong> ${attachment.create_date} por <em>${
            (attachment.create_uid && attachment.create_uid[1]) || "Desconocido"
          }</em><br>
          <strong>Modificado:</strong> ${attachment.write_date} por <em>${
            (attachment.write_uid && attachment.write_uid[1]) || "Desconocido"
          }</em>
      `;
          this._showTooltip(info, attachmentCard);
        }
      } catch (error) {
        console.error("Error fetching attachment info:", error);
      }
    },

    _showTooltip(info, attachmentCard) {
      let tooltip = document.getElementById("attachment-hover-tooltip");
      if (!tooltip) {
        tooltip = document.createElement("div");
        tooltip.id = "attachment-hover-tooltip";
        tooltip.style.position = "absolute";
        tooltip.style.background = "#fff";
        tooltip.style.border = "1px solid #ccc";
        tooltip.style.padding = "10px 15px";
        tooltip.style.zIndex = "1000";
        tooltip.style.pointerEvents = "none";
        tooltip.style.fontSize = "14px";
        tooltip.style.fontFamily = "'Arial', sans-serif";
        tooltip.style.color = "#333";
        tooltip.style.borderRadius = "5px";
        tooltip.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
        tooltip.style.maxWidth = "200px";
        tooltip.style.textAlign = "center";
        tooltip.style.lineHeight = "1.5";
        document.body.appendChild(tooltip);
      }

      const rect = attachmentCard.getBoundingClientRect();

      tooltip.innerHTML = info;
      tooltip.style.left = `${rect.left}px`;
      tooltip.style.top = `${rect.bottom + 5}px`;
      tooltip.style.display = "block";
    },

    _hideTooltip() {
      const tooltip = document.getElementById("attachment-hover-tooltip");
      if (tooltip) {
        tooltip.style.display = "none";
      }
    },
  });
});
