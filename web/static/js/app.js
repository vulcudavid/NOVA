const menuButtons = document.querySelectorAll(".menu-button");
const pages = document.querySelectorAll(".page");

// ============================================================
// MENU NAVIGATION
// ============================================================

menuButtons.forEach(button => {

    button.addEventListener("click", () => {

        const pageName = button.dataset.page;

        if (
            pageName !== "chat" &&
            conversationActive
        ) {
            stopEmotionDetection();
        }
        
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
// CAMERA + EMOTION DETECTION
// ============================================================

const cameraContainer =
    document.getElementById("camera-container");

const cameraVideo =
    document.getElementById("camera-video");

const cameraCanvas =
    document.getElementById("camera-canvas");

const emotionLabel =
    document.getElementById("emotion-label");

const emotionConfidence =
    document.getElementById("emotion-confidence");

let cameraStream = null;
let emotionInterval = null;
let conversationActive = false;


async function startEmotionDetection() {

    if (conversationActive) {
        return;
    }

    try {

        cameraStream =
            await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });

        cameraVideo.srcObject =
            cameraStream;

        cameraContainer.style.display =
            "block";

        conversationActive = true;

        console.log(
            "Camera browser pornită."
        );

        startEmotionAnalysis();

    } catch (error) {

        console.error(
            "Nu am putut accesa camera:",
            error
        );

        alert(
            "NOVA nu poate accesa camera. " +
            "Verifică permisiunea camerei în browser."
        );
    }
}

function stopEmotionDetection() {

    conversationActive = false;

    if (emotionInterval !== null) {

        clearInterval(
            emotionInterval
        );

        emotionInterval = null;
    }

    if (cameraStream) {

        cameraStream
            .getTracks()
            .forEach(track => track.stop());

        cameraStream = null;
    }

    cameraVideo.srcObject = null;

    cameraContainer.style.display =
        "none";

    console.log(
        "Camera și analiza emoției au fost oprite."
    );
}

function captureCameraFrame() {

    if (!conversationActive) {
        return;
    }

    if (
        cameraVideo.videoWidth === 0 ||
        cameraVideo.videoHeight === 0
    ) {
        return;
    }

    cameraCanvas.width =
        cameraVideo.videoWidth;

    cameraCanvas.height =
        cameraVideo.videoHeight;

    const context =
        cameraCanvas.getContext("2d");

    context.drawImage(
        cameraVideo,
        0,
        0,
        cameraCanvas.width,
        cameraCanvas.height
    );

    cameraCanvas.toBlob(
        blob => {

            if (!blob) {
                return;
            }

            sendFrameForEmotionAnalysis(
                blob
            );

        },
        "image/jpeg",
        0.7
    );
}

async function sendFrameForEmotionAnalysis(blob) {

    if (!conversationActive) {
        return;
    }

    const formData =
        new FormData();

    formData.append(
        "frame",
        blob,
        "frame.jpg"
    );

    try {

        const response =
            await fetch(
                "/api/emotion",
                {
                    method: "POST",
                    body: formData
                }
            );

        if (!response.ok) {
            throw new Error(
                "Emotion API error: " +
                response.status
            );
        }

        const data =
            await response.json();

        if (data.emotion) {

            emotionLabel.textContent =
                data.emotion;

            emotionConfidence.textContent =
                `${(data.confidence * 100).toFixed(1)}%`;
        }

    } catch (error) {

        console.error(
            "Emotion analysis error:",
            error
        );
    }
}

function startEmotionAnalysis() {

    if (emotionInterval !== null) {
        return;
    }

    emotionInterval =
        setInterval(
            captureCameraFrame,
            500
        );
}

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
    if (!conversationActive) {
        await startEmotionDetection();
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


// ============================================================
// REACTION GAME
// ============================================================

const reactionGame = document.getElementById("reaction-game");

const reactionBackButton =
    document.getElementById("reaction-back");

const reactionMenu =
    document.getElementById("reaction-menu");

const reactionContainer =
    document.getElementById("reaction-container");

const reactionResults =
    document.getElementById("reaction-results");

const reactionStartButton =
    document.getElementById("reaction-start-button");

const reactionBox =
    document.getElementById("reaction-box");

const reactionText =
    document.getElementById("reaction-text");

const reactionNewGameButton =
    document.getElementById("reaction-new-game");

const reactionTimeValue =
    document.getElementById("reaction-time-value");

const reactionScoreValue =
    document.getElementById("reaction-score-value");

const reactionGameButton =
    document.querySelector(
        '.game-card[data-game="reaction"]'
    );

let reactionGameRunning = false;
let reactionUpdateInterval = null;


// ============================================================
// OPEN REACTION GAME
// ============================================================

if (reactionGameButton) {

    reactionGameButton.addEventListener(
        "click",
        startReactionGame
    );

}
else {

    console.error(
        "Reaction game button not found!"
    );

}


async function startReactionGame() {

    gamesMenu.style.display = "none";

    reactionGame.style.display = "block";

    reactionMenu.style.display = "flex";

    reactionContainer.style.display = "none";

    reactionResults.style.display = "none";

    reactionGameRunning = false;

    clearInterval(reactionUpdateInterval);
}


// ============================================================
// START REACTION GAME
// ============================================================

if (reactionStartButton) {

    reactionStartButton.addEventListener(
        "click",
        async () => {

        reactionMenu.style.display = "none";

        reactionContainer.style.display = "flex";

        reactionResults.style.display = "none";

        reactionGameRunning = true;

        reactionBox.classList.remove("ready");

        reactionText.textContent = "Asteptati....";

        try {

            const response =
                await fetch(
                    "/api/games/reaction/start",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Server error: " +
                    response.status
                );
            }

            const data =
                await response.json();

            console.log(
                "Reaction game started:",
                data
            );

            /*
             * Actualizez starea jocului
             * periodic pentru a verifica
             * dacă ar trebui să trec la "ready"
             */

            reactionUpdateInterval =
                setInterval(
                    async () => {

                        await checkReactionState();

                    },
                    100
                );

        } catch (error) {

            console.error(
                "Reaction start error:",
                error
            );

            reactionGameRunning = false;

            clearInterval(
                reactionUpdateInterval
            );

            reactionText.textContent =
                "Eroare la pornirea jocului.";
        }

    }
    );

}


// ============================================================
// CHECK REACTION STATE
// ============================================================

async function checkReactionState() {

    if (!reactionGameRunning) {
        return;
    }

    try {

        const response =
            await fetch(
                "/api/games/reaction/state",
                {
                    method: "GET"
                }
            );

        if (!response.ok) {

            throw new Error(
                "Server error: " +
                response.status
            );
        }

        const data =
            await response.json();

        console.log(
            "Reaction state:",
            data
        );

        if (
            data.state === "ready"
        ) {

            reactionBox.classList.add(
                "ready"
            );

            reactionText.textContent =
                "Apasati!";

            /*
             * Elimin intervalul pentru că
             * jocul este pregătit
             */

            clearInterval(
                reactionUpdateInterval
            );

        }

    } catch (error) {

        console.error(
            "Check state error:",
            error
        );

    }

}


// ============================================================
// REACTION BOX CLICK
// ============================================================

if (reactionBox) {

    reactionBox.addEventListener(
        "click",
        async () => {

        if (
            !reactionGameRunning ||
            !reactionBox.classList.contains(
                "ready"
            )
        ) {
            return;
        }

        reactionGameRunning = false;

        clearInterval(
            reactionUpdateInterval
        );

        try {

            const response =
                await fetch(
                    "/api/games/reaction/react",
                    {
                        method: "POST"
                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Server error: " +
                    response.status
                );
            }

            const data =
                await response.json();

            console.log(
                "Reaction result:",
                data
            );

            showReactionResults(data);

        } catch (error) {

            console.error(
                "Reaction react error:",
                error
            );

            reactionText.textContent =
                "Eroare la procesarea reacției.";
        }

    }
    );

}


// ============================================================
// SHOW REACTION RESULTS
// ============================================================

function showReactionResults(data) {

    reactionContainer.style.display =
        "none";

    reactionResults.style.display =
        "flex";

    reactionTimeValue.textContent =
        data.reaction_time;

    reactionScoreValue.textContent =
        data.score;
}


// ============================================================
// NEW REACTION GAME
// ============================================================

if (reactionNewGameButton) {

    reactionNewGameButton.addEventListener(
        "click",
        async () => {

        reactionMenu.style.display = "flex";

        reactionContainer.style.display =
            "none";

        reactionResults.style.display =
            "none";

        reactionGameRunning = false;

        clearInterval(
            reactionUpdateInterval
        );

    }
    );

}


// ============================================================
// BACK TO GAMES MENU (REACTION)
// ============================================================

if (reactionBackButton) {

    reactionBackButton.addEventListener(
        "click",
        () => {

        reactionGame.style.display = "none";

        gamesMenu.style.display = "grid";

        reactionGameRunning = false;

        clearInterval(
            reactionUpdateInterval
        );

    }
    );

}


// ============================================================
// SETTINGS PAGE
// ============================================================

const settingsPage =
    document.getElementById("page-settings");

const settingsButton =
    document.querySelector(
        '.menu-button[data-page="settings"]'
    );

const themeButtons =
    document.querySelectorAll(
        ".theme-button"
    );

// Elemente pentru display-urile nivelelor
const commLevelDisplay =
    document.getElementById("comm-level-display");

const gameLevelDisplay =
    document.getElementById("game-level-display");

const commLevelBar =
    document.getElementById("comm-level-bar");

const gameLevelBar =
    document.getElementById("game-level-bar");

// Elemente pentru statistici Memory
const memoryGamesPlayed =
    document.getElementById("memory-games-played");

const memoryBestScore =
    document.getElementById("memory-best-score");

const memoryAvgScore =
    document.getElementById("memory-avg-score");

// Elemente pentru statistici Reaction
const reactionGamesPlayed =
    document.getElementById("reaction-games-played");

const reactionBestTime =
    document.getElementById("reaction-best-time");

const reactionAvgTime =
    document.getElementById("reaction-avg-time");

const reactionBestScore =
    document.getElementById("reaction-best-score");


// ============================================================
// LOAD SETTINGS ON PAGE OPEN
// ============================================================

if (settingsButton) {

    settingsButton.addEventListener(
        "click",
        loadSettings
    );

}


async function loadSettings() {

    try {

        const response =
            await fetch(
                "/api/settings",
                {
                    method: "GET"
                }
            );

        if (!response.ok) {

            throw new Error(
                "Server error: " +
                response.status
            );
        }

        const data =
            await response.json();

        console.log(
            "Settings loaded:",
            data
        );

        updateSettingsDisplay(data);

    } catch (error) {

        console.error(
            "Settings load error:",
            error
        );

    }

}


// ============================================================
// UPDATE SETTINGS DISPLAY
// ============================================================

function updateSettingsDisplay(data) {

    // Nivele
    const commLevel = data.comm_level;
    const gameLevel = data.game_level;

    commLevelDisplay.textContent = commLevel;
    gameLevelDisplay.textContent = gameLevel;

    commLevelBar.style.width =
        (commLevel * 33) + "%";

    gameLevelBar.style.width =
        (gameLevel * 33) + "%";

    // Statistici Memory
    memoryGamesPlayed.textContent =
        data.memory.games_played;

    memoryBestScore.textContent =
        data.memory.best_score;

    memoryAvgScore.textContent =
        data.memory.average_score;

    // Statistici Reaction
    reactionGamesPlayed.textContent =
        data.reaction.games_played;

    reactionBestTime.textContent =
        data.reaction.best_time;

    reactionAvgTime.textContent =
        data.reaction.average_time;

    reactionBestScore.textContent =
        data.reaction.best_score;

}


// ============================================================
// THEME SYSTEM
// ============================================================

// Inițializez tema din localStorage
function initTheme() {

    const savedTheme =
        localStorage.getItem("theme") || "dark";

    applyTheme(savedTheme);

}


function applyTheme(themeName) {

    document.body.className =
        themeName === "dark" ? "" : `theme-${themeName}`;

    themeButtons.forEach(btn => {

        btn.classList.remove("active");

        if (btn.dataset.theme === themeName) {

            btn.classList.add("active");

        }

    });

    localStorage.setItem("theme", themeName);

}


// Theme buttons event listeners
themeButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            const theme =
                button.dataset.theme;

            applyTheme(theme);

        }
    );

});


// Inițializez tema la încărcare
initTheme();

