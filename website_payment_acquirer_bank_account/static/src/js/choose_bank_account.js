odoo.define("website_payment_acquirer_bank_account.choose_bank_account", function (
  require
) {
  "use strict";

  const rpc = require("web.rpc");

  let isPaymentButtonDisabled = true; // Variable to track the disabled state of the payment button

  function getUrlParameter(name) {
    console.log(`Getting URL parameter: ${name}`);
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
  }

  function removeUrlParameter(name) {
    console.log(`Removing URL parameter: ${name}`);
    const url = new URL(window.location.href);
    url.searchParams.delete(name);
    window.history.replaceState({}, document.title, url);
  }

  function displayUrlMessage() {
    console.log("Displaying URL message");
    const message = getUrlParameter("message");
    const status = getUrlParameter("status");
    const messageContainer = document.querySelector("#bank-account-message");

    if (!messageContainer) {
      console.warn("Element with ID 'bank-account-message' not found.");
      return;
    }

    if (message) {
      console.log(`Message found: ${message}, Status: ${status}`);
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
    } else {
      console.log("No message to display");
    }
  }

  function onDOMReady() {
    console.log("Document is ready");
    displayUrlMessage();
    handleBankAccountSelect();
    updatePaymentButtonState();
    startMonitoringPaymentButton(); // Start monitoring the payment button state
  }

  function startMonitoringPaymentButton() {
    setInterval(() => {
      handleBankAccountSelect();
      const paymentButton = document.getElementById("o_payment_form_pay");
      if (paymentButton) {
        const shouldBeDisabled = isPaymentButtonDisabled; // Get the desired state from the variable
        paymentButton.disabled = shouldBeDisabled; // Set the button's disabled state
      }
    }, 200);
  }

  function chooseBankAccount(radio) {
    if (!radio || !radio.value) {
      console.log("No bank account selected.");
      alert("Please select a bank account.");
      return;
    }

    const BankID = radio.value;
    console.log(`Choosing bank account with ID: ${BankID}`);

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
        console.log("RPC response received:", data);
        const messageContainer = document.querySelector("#bank-account-message");
        if (data.status === "success") {
          messageContainer.innerHTML = `<div class="alert alert-success">${data.message || "Bank account selected successfully."
            }</div>`;
          messageContainer.style.backgroundColor = "#dff0d8";
          console.log("Bank account selected successfully");

          removeUrlParameter("status");
        } else if (data.status === "error") {
          messageContainer.innerHTML = `<div class="alert alert-danger">${data.message || "An error occurred while selecting the bank account."
            }</div>`;
          messageContainer.style.backgroundColor = "#f2dede";
          console.log("Error selecting bank account:", data.message);

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
    console.log("Handling bank account selection");

    const remesaRadioButtons = document.querySelectorAll(
      'input[type="radio"][data-acquirer-id="25"]'
    );
    const otherRadioButtons = document.querySelectorAll(
      'input[type="radio"][data-acquirer-id="9"]'
    );
    const ibanFormDiv = document.getElementById("bank-account-select-iban-form");
    const formRadioButtons = document.querySelectorAll(
      'form[action="/choose_bank_account"] input[type="radio"]'
    );

    updatePaymentButtonState();

    remesaRadioButtons.forEach(function (radio) {
      radio.addEventListener("focus", function () {
        if (radio.checked) {
          console.log(`Radio button ${radio.value} is selected.`);
          if (formRadioButtons.length > 0) {
            formRadioButtons[0].checked = true;
            chooseBankAccount(formRadioButtons[0]);
          }
          if (ibanFormDiv) {
            ibanFormDiv.style.display = "";
            console.log("IBAN form div displayed");
          }
        }
        updatePaymentButtonState();
      });
    });

    otherRadioButtons.forEach(function (radio) {
      radio.addEventListener("focus", function () {
        if (radio.checked) {
          console.log(`Radio button ${radio.value} is selected.`);
          if (ibanFormDiv) {
            ibanFormDiv.style.display = "none";
            console.log("IBAN form div hidden");
          }
        }
        updatePaymentButtonState();
      });
    });

    formRadioButtons.forEach(function (radio) {
      radio.addEventListener("change", function () {
        console.log(`Form radio button changed: ${radio.value}`);
        updatePaymentButtonState();
      });
    });



    remesaRadioButtons.forEach(function (radio) {
      // Find the closest parent div with the specified class
      const parentDiv = radio.closest('div.o_payment_acquirer_select');

      // Add event listener for change event directly on the radio button
      radio.addEventListener("focus", function () {
        if (radio.checked) {
          console.log(`Radio button ${radio.value} is selected.`);

          if (formRadioButtons.length > 0) {
            formRadioButtons[0].checked = true;
            chooseBankAccount(formRadioButtons[0]);
          }
          if (ibanFormDiv) {
            ibanFormDiv.style.display = ""; // Show the IBAN form
            console.log("IBAN form div displayed");
          }
        } else {
          // Handle deselection if needed
          console.log(`Radio button ${radio.value} is not selected.`);
        }
        updatePaymentButtonState();
      });
    });
  }

  function updatePaymentButtonState() {
    const formRadioButtons = document.querySelectorAll(
      'form[action="/choose_bank_account"] input[type="radio"]'
    );
    const ibanFormDiv = document.getElementById("bank-account-select-iban-form");

    const anySelected = Array.from(formRadioButtons).some((radio) => radio.checked);
    const ibanDisplayed = ibanFormDiv && ibanFormDiv.style.display !== "none";
    if (anySelected && ibanDisplayed) {
      console.log("At least one radio button is selected. Enabling payment button.");
      isPaymentButtonDisabled = false;
    } else {
      console.log("No radio buttons are selected. Disabling payment button.");
      isPaymentButtonDisabled = true;
    }
  }
  if (document.readyState !== 'loading') {
    onDOMReady();
  } else {
    document.addEventListener('DOMContentLoaded', function () {
      onDOMReady();
    });
  }

  window.chooseBankAccount = chooseBankAccount;

  return {
    chooseBankAccount: chooseBankAccount,
  };
});
