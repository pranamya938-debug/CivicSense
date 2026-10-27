
const complaintForm = document.getElementById("complaintForm");
const message = document.getElementById("message");

if (complaintForm && message) {
    complaintForm.addEventListener("submit", function (event) {
        event.preventDefault();

        message.textContent =
            "✅ Your complaint has been submitted successfully!";
        message.style.color = "green";
        message.style.fontWeight = "bold";

        complaintForm.reset();
    });
} else {
    console.error("Complaint form or message element not found.");
}
