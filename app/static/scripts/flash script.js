// for alert box ------------------------------------------------------------------------------------------------------------------------
// initializer
const rootElement = document.querySelector("body:first-child");
const body = document.querySelector("body");

const alertBox = document.createElement("div");
alertBox.setAttribute("id", "alert-box");
body.insertBefore(alertBox, rootElement);


// Show alert box
function showAlert(message, status) {
    const alert = document.createElement("div");
    const alertIcon = document.createElement("div");
    const alertContent = document.createElement("div");
    const alertMessage = document.createElement("div");
    const alertDismiss = document.createElement("div");

    const delay = 100; // set delay

    // alert
    alert.className = "alert";
    setTimeout(function () {
        alert.classList.add("alert-active");
        alert.classList.add(`alert-${status}`);
    }, delay)

    // content
    alertContent.className = "alert-content";
    alertMessage.textContent = message;

    // icon
    alertIcon.className = "alert-icon";

    // dismiss
    alertDismiss.className = "alert-dismiss";

    // append everything together
    alertContent.appendChild(alertIcon);
    alertContent.appendChild(alertMessage);
    alert.appendChild(alertContent);
    alert.appendChild(alertDismiss);

    // add to DOM
    alertBox.prepend(alert);

    // auto closing
    setTimeout(function () {
        alert.classList.remove("alert-active");
        alert.classList.add("alert-closing");

        // remove element from dom
        setTimeout(function () {
            alert.remove();
        }, 500);
    }, 4000 + delay);

    // remove by clicking
    function dismissAlert(event) {
        if (event.target.parentElement.classList.contains("alert")) {
            console.log("true");
            const alert = event.target.parentElement;
            alert.classList.remove("alert-active");
            alert.classList.add("alert-closing");
            setTimeout(function () {
                alert.remove();
            }, 500);
        }
    }

    document.addEventListener("click", dismissAlert);
}