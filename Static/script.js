const modeSelect = document.getElementById("mode");
const generateButton =
    document.getElementById("generate-button") ||
    document.querySelector('button[onclick*="generate"]') ||
    document.querySelector("button");
const result = document.getElementById("result");
const statusText = document.getElementById("status") || createStatusElement();

let currentBuild = [];

function createStatusElement() {
    const status = document.createElement("p");
    status.id = "status";
    status.className = "status";
    status.setAttribute("aria-live", "polite");
    if (result && result.parentElement) {
        result.parentElement.insertBefore(status, result);
    } else {
        document.body.appendChild(status);
    }
    return status;
}

function setStatus(message, isError = false) {
    statusText.textContent = message;
    statusText.dataset.state = isError ? "error" : "default";
}

function getCurrentMode() {
    return modeSelect ? modeSelect.value : "any";
}

async function requestBuild(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    const rawText = await response.text();
    let data;

    try {
        data = JSON.parse(rawText);
    } catch (error) {
        throw new Error("The app returned an invalid response. Restart the Flask server and refresh the page.");
    }

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}

function normalizeBuild(build) {
    return build.map((perk) => {
        if (typeof perk === "string") {
            return {
                name: perk,
                description: "This page is talking to an older server response. Restart the Flask app and refresh the page to load perk descriptions and reroll-one support.",
            };
        }

        return {
            name: perk.name,
            description: perk.description,
        };
    });
}

function renderBuild() {
    if (!result) {
        return;
    }

    result.innerHTML = "";

    if (!currentBuild.length) {
        return;
    }

    currentBuild.forEach((perk, index) => {
        const card = document.createElement("article");
        card.className = "perk-card";

        const title = document.createElement("h2");
        title.className = "perk-name";
        title.textContent = perk.name;

        const description = document.createElement("p");
        description.className = "perk-description";
        description.textContent = perk.description;

        const rerollButton = document.createElement("button");
        rerollButton.className = "reroll-button";
        rerollButton.type = "button";
        rerollButton.textContent = "Reroll This Perk";
        rerollButton.addEventListener("click", () => rerollOne(index));

        card.append(title, description, rerollButton);
        result.appendChild(card);
    });
}

async function generate() {
    if (generateButton) {
        generateButton.disabled = true;
    }
    setStatus("Generating build...");

    try {
        currentBuild = normalizeBuild(await requestBuild("/generate", { mode: getCurrentMode() }));
        renderBuild();
        setStatus("Build ready.");
    } catch (error) {
        setStatus(error.message, true);
    } finally {
        if (generateButton) {
            generateButton.disabled = false;
        }
    }
}

async function rerollOne(index) {
    setStatus(`Rerolling perk ${index + 1}...`);

    const buttons = document.querySelectorAll(".reroll-button");
    buttons.forEach((button) => {
        button.disabled = true;
    });

    try {
        currentBuild = normalizeBuild(await requestBuild("/reroll-one", {
            mode: getCurrentMode(),
            current_build: currentBuild.map((perk) => perk.name),
            index: index,
        }));
        renderBuild();
        setStatus(`Perk ${index + 1} rerolled.`);
    } catch (error) {
        setStatus(error.message, true);
        renderBuild();
    }
}

if (generateButton) {
    generateButton.addEventListener("click", generate);
}

window.generate = generate;
setStatus("Ready. Choose a mode and generate a build.");
