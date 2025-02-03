odoo.define("website_payment_acquirer_bank_account.choose_bank_account", function (
  require
) {
  "use strict";

  const rpc = require("web.rpc");

  let isPaymentButtonDisabled = true;

  function getUrlParameter(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
  }

  function removeUrlParameter(name) {
    const url = new URL(window.location.href);
    url.searchParams.delete(name);
    window.history.replaceState({}, document.title, url);
  }

  function displayUrlMessage() {
    const message = getUrlParameter("message");
    const status = getUrlParameter("status");
    const existing_bank_id = getUrlParameter("existing_bank_id");
    const messageContainer = document.querySelector("#bank-account-message");

    if (!messageContainer) {
      console.warn("Element with ID 'bank-account-message' not found.");
      return;
    }

    messageContainer.style.display = "block";

    if (message) {
      messageContainer.innerHTML = `<div class="alert">${message}</div>`;
      let responseMessage = "";

      if (status === "200") {
        messageContainer.style.backgroundColor = "#d4edda";
        messageContainer.style.color = "#155724";
        const radioButton = document.querySelector(
          'input[type="radio"][data-acquirer-id="25"]'
        );
        if (radioButton) {
          radioButton.click(); // Trigger a click event on Remesa Bancaria
        }
      } else if (status === "400") {
        messageContainer.style.backgroundColor = "#f8d7da";
        messageContainer.style.color = "#721c24";
        if (existing_bank_id) {
          const errorMessage =
            "ERROR: Esa cuenta ya existe para otro usuario del sistema. " +
            "Por favor indique otra cuenta. " +
            `O <a href="#" id="log-in-existant-account">logueese</a> con el otro usuario de la cuenta indicada (al pinchar en logueese le enviará un recordatorio de contraseña al usuario para el que se ha encontrado la cuenta bancaria).`;
          messageContainer.innerHTML = `<div class="alert alert-danger">${errorMessage}</div>`;

          const logInLink = document.getElementById("log-in-existant-account");
          logInLink.addEventListener("click", function (event) {
            event.preventDefault();
            const requestData = {existing_bank_id: existing_bank_id};
            rpc
              .query({
                route: "/send_email_to_log_for_existing_account",
                params: requestData,
              })
              .then(function (data) {
                if (data.success) {
                  responseMessage = `<div class="alert alert-success">${data.success}</div>`;
                } else {
                  responseMessage = `<div class="alert alert-danger">${data.error}</div>`;
                }
                messageContainer.innerHTML += responseMessage;
              })
              .catch(function (error) {
                responseMessage = `<div class="alert alert-danger">Error during RPC call: ${error}</div>`;
                messageContainer.innerHTML += responseMessage;
              });
          });
        }
      } else {
        messageContainer.style.backgroundColor = "#fff3cd";
        messageContainer.style.color = "#856404";
      }

      removeUrlParameter("message");
      removeUrlParameter("status");
    } else {
      console.log("No message to display");
    }
  }

  function onDOMReady() {
    handleBankAccountSelect();
    displayUrlMessage();
    updatePaymentButtonState();
    startMonitoringPaymentButton();
  }

  function startMonitoringPaymentButton() {
    const paymentButton = document.getElementById("o_payment_form_pay");
    let lastDisabledState = null;

    if (paymentButton) {
      const observer = new MutationObserver(() => {
        const shouldBeDisabled = isPaymentButtonDisabled;

        if (
          paymentButton.disabled !== shouldBeDisabled &&
          shouldBeDisabled !== lastDisabledState
        ) {
          observer.disconnect();
          paymentButton.disabled = shouldBeDisabled;
          lastDisabledState = shouldBeDisabled;
          observer.observe(paymentButton, {
            attributes: true,
            attributeFilter: ["disabled"],
          });
        }
      });

      observer.observe(paymentButton, {
        attributes: true,
        attributeFilter: ["disabled"],
      });
    } else {
      console.log("No se encontró el botón de pago en la página.");
    }
  }

  function chooseBankAccount(radio) {
    if (!radio || !radio.value) {
      console.error("No bank account selected.");
      alert("Please select a bank account.");
      return;
    }

    const BankID = radio.value;

    const requestData = {
      bank_id: BankID,
    };

    const messageContainer = document.querySelector("#bank-account-message");
    if (messageContainer) {
      messageContainer.innerHTML = "";
      messageContainer.style.backgroundColor = "";
    }

    rpc
      .query({
        route: "/choose_bank_account",
        params: requestData,
      })
      .then(function (data) {
        const messageContainer = document.querySelector("#bank-account-message");
        if (data.status === "success") {
          messageContainer.innerHTML = `<div class="alert alert-success">${
            data.message || "Bank account selected successfully."
          }</div>`;
          messageContainer.style.backgroundColor = "#dff0d8";

          removeUrlParameter("status");
        } else if (data.status === "error") {
          messageContainer.innerHTML = `<div class="alert alert-danger">${
            data.message || "An error occurred while selecting the bank account."
          }</div>`;
          messageContainer.style.backgroundColor = "#f2dede";

          removeUrlParameter("status");
        }
      })
      .catch(function (error) {
        console.error("Error during RPC call:", error);
        const messageContainer = document.querySelector("#bank-account-message");
        if (messageContainer) {
          messageContainer.innerHTML = `<div class="alert alert-danger">An error occurred while processing your request.</div>`;
          messageContainer.style.backgroundColor = "#f2dede";

          removeUrlParameter("status");
        }
      });
  }

  function handleBankAccountSelect() {
    const ibanFormDiv = document.getElementById("bank-account-select-iban-form");
    const paymentAcquirerSelectDivs = document.querySelectorAll(
      ".o_payment_acquirer_select"
    );
    const messageContainer = document.querySelector("#bank-account-message");

    function getFormRadioButtons() {
      return document.querySelectorAll(
        'form[action="/choose_bank_account"] input[type="radio"]'
      );
    }

    const bankAccountRadio = getFormRadioButtons()[0];
    if (bankAccountRadio) bankAccountRadio.checked = true;

    function updateIBANFormVisibility(radio) {
      if (radio.dataset.acquirerId === "25") {
        ibanFormDiv.style.display = "";
        messageContainer.style.display = "";
      } else if (radio.dataset.acquirerId === "9") {
        ibanFormDiv.style.display = "none";
        messageContainer.style.display = "none";
      }
    }

    function updateState(radio) {
      if (bankAccountRadio) bankAccountRadio.checked = true;

      radio.checked = true;

      const formRadioButtons = getFormRadioButtons();
      if (radio.dataset.acquirerId === "25" && formRadioButtons.length > 0) {
        formRadioButtons[0].checked = true;
        formRadioButtons[0].dispatchEvent(new Event("change"));
        chooseBankAccount(formRadioButtons[0]);
      }

      updateIBANFormVisibility(radio);
      updatePaymentButtonState();
    }

    paymentAcquirerSelectDivs.forEach((div) => {
      div.addEventListener("click", () => {
        const target =
          div.querySelector(`input[type="radio"][data-acquirer-id="25"]`) ||
          div.querySelector(`input[type="radio"][data-acquirer-id="9"]`);
        if (target) updateState(target);
      });

      div.addEventListener("focusin", () => {
        const target =
          div.querySelector(`input[type="radio"][data-acquirer-id="25"]`) ||
          div.querySelector(`input[type="radio"][data-acquirer-id="9"]`);
        if (target) updateState(target);
      });
    });

    getFormRadioButtons().forEach((radio) => {
      radio.addEventListener("change", updatePaymentButtonState);
    });
  }

  document.addEventListener("DOMContentLoaded", handleBankAccountSelect);

  function updatePaymentButtonState() {
    const formRadioButtons = document.querySelectorAll(
      'form[action="/choose_bank_account"] input[type="radio"]'
    );
    const ibanFormDiv = document.getElementById("bank-account-select-iban-form");

    const paymentButton = document.getElementById("o_payment_form_pay");

    const anySelected = Array.from(formRadioButtons).some((radio) => radio.checked);
    const ibanDisplayed = ibanFormDiv && ibanFormDiv.style.display !== "none";
    if (anySelected && ibanDisplayed) {
      isPaymentButtonDisabled = false;
      if (paymentButton) paymentButton.disabled = false;
    } else {
      isPaymentButtonDisabled = true;
      if (paymentButton) paymentButton.disabled = true;
    }
  }
  if (document.readyState !== "loading") {
    onDOMReady();
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      onDOMReady();
    });
  }

  window.chooseBankAccount = chooseBankAccount;

  return {
    chooseBankAccount: chooseBankAccount,
  };
});
