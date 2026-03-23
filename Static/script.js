async function generate() {
    const mode = document.getElementById("mode").value;

    const res = await fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ mode: mode })
    });

    const data = await res.json();

    const list = document.getElementById("result");
    list.innerHTML = "";

    data.forEach(perk => {
        const li = document.createElement("li");
        li.textContent = perk;
        list.appendChild(li);
    });
}