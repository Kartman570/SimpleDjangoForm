document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("userForm");
    const status = document.getElementById("status");
    const countrySelect = form.querySelector("select[name=country]");
    const codeInput = form.querySelector("input[name=code]");

    const countryCodes = {
        Georgia: "995",
        USA: "1",
        Germany: "49"
    };

    countrySelect.addEventListener("change", () => {
        const country = countrySelect.value;
        codeInput.value = countryCodes[country] || "";
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        document.querySelectorAll(".error").forEach(el => el.remove());
        document.querySelectorAll(".error-field").forEach(el => el.classList.remove("error-field"));
        status.textContent = "";

        const data = Object.fromEntries(new FormData(form));
        let hasError = false;

        const rules = {
            firstname: 10,
            lastname: 20,
            country: 20,
            code: 4,
            phone: 15
        };

        for (const [key, maxLen] of Object.entries(rules)) {
            if (data[key].length > maxLen) {
                const input = form.querySelector(`[name=${key}]`);
                input.classList.add("error-field");
                const error = document.createElement("span");
                error.classList.add("error");
                error.textContent = `Max ${maxLen} characters`;
                input.parentElement.appendChild(error);
                hasError = true;
            }
        }

        if (hasError) return;

        try {
            const resp = await fetch("/users/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            if (resp.ok) {
                form.reset();
                status.textContent = "Thank you for signing up! You will receive an email notification shortly.";
                status.style.color = "#3f8d46";
            } else {
                const err = await resp.json();
                for (const [field, messages] of Object.entries(err)) {
                    const input = form.querySelector(`[name=${field}]`);
                    if (input) {
                        input.classList.add("error-field");
                        const span = document.createElement("span");
                        span.classList.add("error");
                        span.textContent = messages.join(", ");
                        input.parentElement.appendChild(span);
                    }
                }
            }
        } catch (error) {
            status.textContent = "Server error.";
            status.style.color = "#b91c1c";
        }
    });
});
