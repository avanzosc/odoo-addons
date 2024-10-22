odoo.define("mail_chatter_statistics.main", function (require) {
  "use strict";

  const rpc = require("web.rpc");
  const core = require("web.core");
  const QWeb = core.qweb;

  const Message = require("mail/static/src/components/message/message.js");

  let statisticsInitialized = false;

  const OriginalMounted = Message.prototype.mounted;

  Message.prototype.mounted = function () {
    // Import rpc inside the mounted method

    if (!statisticsInitialized) {
      console.log("El componente Message se ha montado por completo en el DOM");
      initChatterStatistics(); // Initialize statistics when the component mounts for the first time
      statisticsInitialized = true; // Prevent reinitialization
    }

    if (OriginalMounted) {
      OriginalMounted.call(this); // Call the original mounted method
    }

    console.log("this.mailingTrace:", this.mailingTrace);
  };

  Message.prototype.getMailingTrace = function (mailMessageId) {
    const rpc = require("web.rpc"); // Importar rpc aquí

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

  async function fetchMailingTrace(messageInstance, mailMessageId) {
    const mailingTrace = await messageInstance.getMailingTrace(mailMessageId);
    messageInstance._mailingTrace = mailingTrace; // Assign the resolved object
    console.log("Fetched and set mailingTrace:", mailingTrace);
  }

  // Define the getter with the resolved object
  Object.defineProperty(Message.prototype, "mailingTrace", {
    get: function () {
      // Check if the object is already set and return it if so
      if (this._mailingTrace) {
        return this._mailingTrace;
      }

      // Extract mail message ID
      const localIdParts = this.message.localId.split("_");
      const mailMessageId = localIdParts.length > 1 ? localIdParts[1] : null;

      // Trigger async function to fetch and set _mailingTrace only once
      if (!this._fetchMailingTraceStarted) {
        this._fetchMailingTraceStarted = true;
        fetchMailingTrace(this, mailMessageId);
      }

      console.log("mailingTrace is not yet fetched, returning undefined for now.");
      return undefined; // Return undefined until the object is set
    },
  });

  Object.defineProperty(Message.prototype, "onWillPatch", {
    async function() {
      // Wait until mailingTrace is fully loaded
      if (!this._mailingTrace) {
        console.log("Waiting for mailingTrace...");
        const localIdParts = this.message.localId.split("_");
        const mailMessageId = localIdParts.length > 1 ? localIdParts[1] : null;

        // Call the async function to fetch mailing trace
        await fetchMailingTrace(this, mailMessageId);
      }
    },
  });

  function initChatterStatistics() {
    console.log("Inicializando el módulo de estadísticas de Chatter");

    const {model, id} = getModelAndIdFromUrl();
    if (model && id) {
      console.log(
        "Llamando a la acción para obtener el Chatter Message ID y Mailing Trace IDs automáticamente"
      );
      callChatterAction(model, id);
    } else {
      console.warn("No se ha podido obtener el modelo o el ID para Chatter");
    }

    console.log("Message prototype:", Message.prototype);
  }

  function callChatterAction(modelName, recordId) {
    console.log(
      "Llamando a la acción personalizada para el modelo:",
      modelName,
      "y registro ID:",
      recordId
    );

    console.log(
      "Iniciando consulta RPC para obtener Chatter Message ID y Mailing Trace IDs..."
    );

    rpc
      .query({
        model: "mailing.trace",
        method: "get_chatter_id",
        args: [modelName, recordId],
      })
      .then(function (result) {
        console.log("Resultado de la consulta RPC:", result);
      })
      .catch(function (error) {
        console.error(
          "Error al obtener el Chatter Message ID o los Mailing Trace IDs:",
          error
        );
      });
  }
  function getModelAndIdFromUrl() {
    console.log("Accediendo al fragmento de la URL");

    const hash = window.location.hash.substring(1);
    console.log("Fragmento de URL:", hash);

    const params = new URLSearchParams(hash);
    const model = params.get("model");
    const id = params.get("id");

    console.log("Modelo:", model, "ID:", id);
    return {model, id};
  }
});
