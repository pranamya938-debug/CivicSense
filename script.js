
const complaintForm = document.getElementById("complaintForm");
const message = document.getElementById("message");

if (complaintForm && message) {
    complaintForm.addEventListener("submit", function (event) {
        event.preventDefault();

        message.textContent =
            "Your complaint has been submitted successfully!";

        message.style.color = "green";

        complaintForm.reset();
    });
}
