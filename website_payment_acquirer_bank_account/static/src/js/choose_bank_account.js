odoo.define("website_payment_acquirer_bank_account.choose_bank_account", function (
  require
) {
  "use strict";

  const rpc = require("web.rpc");

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
    const messageContainer = document.querySelector("#bank-account-message");

    if (!messageContainer) {
      console.warn("Element with ID 'bank-account-message' not found.");
      return;
    }

    if (message) {
      messageContainer.innerHTML = `<div class="alert">${message}</div>`;
      if (status === "200") {
        messageContainer.style.backgroundColor = "#d4edda";
        messageContainer.style.color = "#155724";
      } else if (status === "400") {
        messageContainer.style.backgroundColor = "#f8d7da";
        messageContainer.style.color = "#721c24";
      } else {
        messageContainer.style.backgroundColor = "#fff3cd";
        messageContainer.style.color = "#856404";
      }

      removeUrlParameter("message");
      removeUrlParameter("status");
    }
  }

  function onDOMReady() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        displayUrlMessage();
      });
    } else {
      displayUrlMessage();
    }
  }

  onDOMReady();

  function chooseBankAccount(radio) {
    if (!radio || !radio.value) {
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
        console.error("Error:", error);
        const messageContainer = document.querySelector("#bank-account-message");
        if (messageContainer) {
          messageContainer.innerHTML = `<div class="alert alert-danger">An error occurred while processing your request.</div>`;
          messageContainer.style.backgroundColor = "#f2dede";

          removeUrlParameter("status");
        }
      });
  }

  window.chooseBankAccount = chooseBankAccount;

  return {
    chooseBankAccount: chooseBankAccount,
  };
});
