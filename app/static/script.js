async function upload() {
    const resultDiv = document.getElementById("uploadResult");
    resultDiv.className = "message";

    const fileInput = document.getElementById("file");
    if (!fileInput.files.length) {
        resultDiv.classList.add("error");
        resultDiv.innerText = "Please select a file.";
        return;
    }

    const product = document.getElementById("product").value;
    const type = document.getElementById("type").value;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch(
        `/api/v1/identifiers/upload?id_type=${type}&product=${product}`,
        { method: "POST", body: formData }
    );

    const data = await res.json();

    if (!res.ok) {
        resultDiv.classList.add("error");
        resultDiv.innerText = data.detail || "Upload failed";
        return;
    }

    resultDiv.classList.add("success");
    resultDiv.innerText =
        `Inserted: ${data.result.inserted}, Skipped: ${data.result.skipped}`;
}

async function getNext(product, type) {
    const resultDiv = document.getElementById("nextResult");
    resultDiv.className = "message";

    const res = await fetch(
        `/api/v1/identifiers/next?id_type=${type}&product=${product}`
    );

    const data = await res.json();

    if (!res.ok) {
        resultDiv.classList.add("error");
        resultDiv.innerText = data.detail || "No identifier available";
        return;
    }

    resultDiv.classList.add("success");
    resultDiv.innerText = `Value: ${data.value} | Remaining: ${data.remaining}`;

    if (data.warning) {
        resultDiv.classList.remove("success");
        resultDiv.classList.add("warning");
        resultDiv.innerText += `\n${data.warning}`;
    }
}

async function loadDashboard() {
    const tbody = document.querySelector("#dashboardTable tbody");
    tbody.innerHTML = "";

    const res = await fetch(`/api/v1/identifiers/dashboard`);
    const data = await res.json();

    for (const product in data) {
        const row = document.createElement("tr");

        const item = data[product];

        if (item.available === 0) {
            row.classList.add("out-of-stock");
        } else if (item.low_stock) {
            row.classList.add("low-stock");
        }

        row.innerHTML = `
            <td>${product}</td>
            <td>${item.type}</td>
            <td>${item.total}</td>
            <td>${item.available}</td>
            <td>${item.used}</td>
            <td>
                ${item.available === 0
                    ? "❌ Out of Stock"
                    : item.low_stock
                        ? "⚠️ Low Stock"
                        : "✅ OK"}
            </td>
        `;

        tbody.appendChild(row);
    }
}
