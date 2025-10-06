document.getElementById("userForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    document.querySelectorAll(".error").forEach(el => el.remove());
    document.querySelectorAll(".error-field").forEach(el => el.classList.remove("error-field"));
    document.getElementById("status").textContent = "";

    const form = e.target;
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
            document.getElementById("status").textContent = "User successfully added.";
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
        document.getElementById("status").textContent = "Server error.";
    }
});
