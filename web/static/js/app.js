const menuButtons = document.querySelectorAll(".menu-button");
const pages = document.querySelectorAll(".page");

// ============================================================
// MENU NAVIGATION
// ============================================================

menuButtons.forEach(button => {

    button.addEventListener("click", () => {

        const pageName = button.dataset.page;

        menuButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        pages.forEach(page => {
            page.classList.remove("active");
        });

        const selectedPage =
            document.getElementById(
                `page-${pageName}`
            );

        if (selectedPage) {
            selectedPage.classList.add("active");
        }

    });

});


// ============================================================
// CHAT
// ============================================================

const chatInput =
    document.getElementById("chat-input");

const sendButton =
    document.getElementById("send-button");

const messages =
    document.getElementById("messages");


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(text, sender) {

    const message =
        document.createElement("div");

    message.classList.add(
        "message",
        sender
    );

    message.textContent = text;

    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;
}


// ============================================================
// TEXT TO SPEECH
// ============================================================

function speakText(text) {

    if (!("speechSynthesis" in window)) {

        console.log(
            "Browserul nu suportă Speech Synthesis."
        );

        return;
    }

    speechSynthesis.cancel();

    const utterance =
        new SpeechSynthesisUtterance(text);

    utterance.lang = "ro-RO";
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    speechSynthesis.speak(
        utterance
    );
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const text =
        chatInput.value.trim();

    if (text === "") {
        return;
    }

    addMessage(
        text,
        "user"
    );

    chatInput.value = "";

    sendButton.disabled = true;

    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Eroare la comunicarea cu NOVA."
            );
        }

        addMessage(
            data.response,
            "nova"
        );

        speakText(
            data.response
        );

    } catch (error) {

        console.error(
            "Chat error:",
            error
        );

        addMessage(
            "Eroare la comunicarea cu LLM.",
            "nova"
        );

    } finally {

        sendButton.disabled = false;

        chatInput.focus();
    }
}


// ============================================================
// SEND BUTTON
// ============================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// ============================================================
// ENTER KEY
// ============================================================

chatInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);


// ============================================================
// HOME QUICK ACTIONS
// ============================================================

const homeCards =
    document.querySelectorAll(
        "[data-page-target]"
    );

homeCards.forEach(card => {

    card.addEventListener("click", () => {

        const targetPage =
            card.dataset.pageTarget;

        const targetButton =
            document.querySelector(
                `.menu-button[data-page="${targetPage}"]`
            );

        if (targetButton) {

            targetButton.click();

        }

    });

});


// ============================================================
// MEMORY GAME
// ============================================================

const gamesMenu = document.getElementById("games-menu");
const memoryGame = document.getElementById("memory-game");

const memoryBackButton =
    document.getElementById("memory-back");

const memoryNewGameButton =
    document.getElementById("memory-new-game");

const memoryBoard =
    document.getElementById("memory-board");

const memoryScore =
    document.getElementById("memory-score");

const memoryAttempts =
    document.getElementById("memory-attempts");

    const memoryGlobalScore =
    document.getElementById("memory-global-score");

const memoryGameLevel =
    document.getElementById("memory-game-level");

const memoryLevelMessage =
    document.getElementById("memory-level-message");

const memoryLevelActions =
    document.getElementById("memory-level-actions");

const memoryIncreaseLevel =
    document.getElementById("memory-increase-level");

const memoryDecreaseLevel =
    document.getElementById("memory-decrease-level");

const memoryGameOver =
    document.getElementById("memory-game-over");

const memoryGameButton =
    document.querySelector(
        '.game-card[data-game="memory"]'
    );


// ============================================================
// OPEN MEMORY GAME
// ============================================================

memoryGameButton.addEventListener(
    "click",
    startMemoryGame
);


async function startMemoryGame() {

    gamesMenu.style.display = "none";

    memoryGame.style.display = "block";

    memoryBoard.innerHTML = "";

    memoryScore.textContent = "0";

    memoryAttempts.textContent = "0";

    memoryGlobalScore.textContent = "50";
    memoryGameLevel.textContent = "1";

    memoryLevelMessage.style.display = "none";
    memoryLevelActions.style.display = "none";
    memoryGameOver.style.display = "none";


    try {

        const response = await fetch(
            "/api/games/memory/start",
            {
                method: "POST"
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server error: " + response.status
            );

        }


        const data = await response.json();
        updateMemoryDifficulty(data);

        console.log(
            "Memory game data:",
            data
        );


        createMemoryBoard(data);


    } catch (error) {

        console.error(
            "Memory game error:",
            error
        );


        memoryBoard.innerHTML = `
            <p>
                Nu am putut porni jocul.
            </p>
        `;

    }
}


// ============================================================
// CREATE MEMORY BOARD
// ============================================================

function createMemoryBoard(data) {

    memoryBoard.innerHTML = "";


    /*
     * Serverul ne trimite cărțile.
     *
     * Exemplu:
     *
     * {
     *     "cards": [
     *         "🐶",
     *         "🐱",
     *         "🐶",
     *         "🐱",
     *         ...
     *     ]
     * }
     */


    data.cards.forEach(
        (cardValue, index) => {

            const card =
                document.createElement("button");


            card.classList.add(
                "memory-card"
            );


            card.dataset.index = index;

            card.dataset.value = cardValue;


            card.textContent = "?";


            card.addEventListener(
                "click",
                () => {

                    revealMemoryCard(
                        card
                    );

                }
            );


            memoryBoard.appendChild(card);

        }
    );

}


// ============================================================
// MEMORY CARD SELECTION
// ============================================================

let memoryBusy = false;


async function revealMemoryCard(card) {

    if (memoryBusy) {
        return;
    }


    if (
        card.classList.contains("revealed") ||
        card.classList.contains("matched")
    ) {

        return;
    }


    const index =
        Number(card.dataset.index);


    try {

        const response = await fetch(
            "/api/games/memory/select",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    index: index
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Memory select failed: " +
                response.status
            );
        }


        const data =
            await response.json();

        console.log("Memory select response:", data);
        updateMemoryBoard(data);


        /*
         * Dacă avem două cărți descoperite
         * și nu sunt pereche, le ascundem
         * după o scurtă întârziere.
         */

        if (
            data.revealed.length === 2
        ) {

            memoryBusy = true;

            setTimeout(
                async () => {

                    await hideIncorrectCards();

                    memoryBusy = false;

                },
                1000
            );
        }

    }
    catch (error) {

        console.error(
            "Memory card error:",
            error
        );

    }

}


// ============================================================
// UPDATE MEMORY BOARD
// ============================================================

function updateMemoryBoard(data) {

    memoryScore.textContent =
        data.score;

    memoryAttempts.textContent =
        data.attempts;

    updateMemoryDifficulty(data);

    const cards =
        document.querySelectorAll(
            ".memory-card"
        );


    cards.forEach(
        (card, index) => {

            const isRevealed =
                data.revealed.includes(index);

            const isMatched =
                data.matched.includes(index);


            if (isRevealed || isMatched) {

                card.textContent =
                    card.dataset.value;

                card.classList.add(
                    "revealed"
                );

            }
            else {

                card.textContent =
                    "?";

                card.classList.remove(
                    "revealed"
                );

            }


            if (isMatched) {

                card.classList.add(
                    "matched"
                );

            }
            else {

                card.classList.remove(
                    "matched"
                );

            }

        }
    );
    if (data.game_over) {

        memoryGameOver.textContent =
            `🎉 Felicitări! Ai terminat jocul cu ${data.score} puncte.`;

        memoryGameOver.style.display =
            "block";

    }
    else {

        memoryGameOver.style.display =
            "none";

    }
}

function updateMemoryDifficulty(data) {

    if (
        data.global_score !== undefined
    ) {

        memoryGlobalScore.textContent =
            data.global_score;
    }


    if (
        data.game_level !== undefined
    ) {

        memoryGameLevel.textContent =
            data.game_level;
    }


    // Ascundem mesajul dacă nu există
    // nicio acțiune disponibilă

    memoryLevelActions.style.display =
        "none";


    memoryLevelMessage.style.display =
        "none";


    if (
        data.can_increase_level
    ) {

        memoryLevelMessage.textContent =
            "🎉 Poți crește nivelul de dificultate!";

        memoryLevelMessage.style.display =
            "block";

        memoryLevelActions.style.display =
            "flex";

        memoryIncreaseLevel.style.display =
            "inline-block";

        memoryDecreaseLevel.style.display =
            "none";
    }


    else if (
        data.can_decrease_level
    ) {

        memoryLevelMessage.textContent =
            "Nivelul actual poate fi prea dificil.";

        memoryLevelMessage.style.display =
            "block";

        memoryLevelActions.style.display =
            "flex";

        memoryIncreaseLevel.style.display =
            "none";

        memoryDecreaseLevel.style.display =
            "inline-block";
    }
}

// ============================================================
// BACK TO GAMES MENU
// ============================================================

memoryBackButton.addEventListener(
    "click",
    () => {

        memoryGame.style.display = "none";

        gamesMenu.style.display = "grid";

    }
);


// ============================================================
// NEW MEMORY GAME
// ============================================================

memoryNewGameButton.addEventListener(
    "click",
    () => {

        startMemoryGame();

    }
);


// ============================================================
// HIDE INCORRECT MEMORY CARDS
// ============================================================

async function hideIncorrectCards() {

    try {

        const response = await fetch(
            "/api/games/memory/hide",
            {
                method: "POST"
            }
        );


        if (!response.ok) {

            throw new Error(
                "Memory hide failed: " +
                response.status
            );

        }


        const data =
            await response.json();


        updateMemoryBoard(data);

    }
    catch (error) {

        console.error(
            "Memory hide error:",
            error
        );

    }
}



// ============================================================
// INCREASE MEMORY GAME LEVEL
// ============================================================

memoryIncreaseLevel.addEventListener(
    "click",
    async () => {

        try {

            const response =
                await fetch(
                    "/api/games/memory/increase-level",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Nu s-a putut crește nivelul."
                );

            }

            const data =
                await response.json();

            updateMemoryDifficulty(data);

        }
        catch (error) {

            console.error(
                "Increase level error:",
                error
            );

        }

    }
);


// ============================================================
// DECREASE MEMORY GAME LEVEL
// ============================================================

memoryDecreaseLevel.addEventListener(
    "click",
    async () => {

        try {

            const response =
                await fetch(
                    "/api/games/memory/decrease-level",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Nu s-a putut scădea nivelul."
                );

            }

            const data =
                await response.json();

            updateMemoryDifficulty(data);

        }
        catch (error) {

            console.error(
                "Decrease level error:",
                error
            );

        }

    }
);