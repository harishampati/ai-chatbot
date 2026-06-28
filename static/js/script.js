const chatWindow = document.getElementById("chat-window");
const userInput  = document.getElementById("user-input");
const sendBtn    = document.getElementById("send-btn");
const clearBtn   = document.getElementById("clear-btn");

let history = [];

// Orange toy robot SVG reused everywhere
const BOT_SVG = `<svg viewBox="0 0 130 130" xmlns="http://www.w3.org/2000/svg">
  <line x1="65" y1="22" x2="65" y2="6" stroke="#f6ad55" stroke-width="4" stroke-linecap="round"/>
  <circle cx="65" cy="2" r="7" fill="#f6ad55"/>
  <rect x="14" y="24" width="102" height="100" rx="32" fill="#c05621"/>
  <rect x="18" y="28" width="94" height="92" rx="30" fill="#f6ad55"/>
  <circle cx="48" cy="68" r="20" fill="#fff"/>
  <circle cx="48" cy="70" r="14" fill="#7b341e"/>
  <circle cx="48" cy="72" r="8" fill="#1a0800"/>
  <circle cx="42" cy="63" r="4" fill="#fff" opacity=".7"/>
  <circle cx="82" cy="68" r="20" fill="#fff"/>
  <circle cx="82" cy="70" r="14" fill="#7b341e"/>
  <circle cx="82" cy="72" r="8" fill="#1a0800"/>
  <circle cx="76" cy="63" r="4" fill="#fff" opacity=".7"/>
  <ellipse cx="30" cy="96" rx="14" ry="9" fill="#ff9eb5" opacity=".55"/>
  <ellipse cx="100" cy="96" rx="14" ry="9" fill="#ff9eb5" opacity=".55"/>
  <path d="M42 108 Q65 126 88 108" fill="none" stroke="#7b341e" stroke-width="3" stroke-linecap="round"/>
  <circle cx="14" cy="76" r="10" fill="#c05621" stroke="#7b341e" stroke-width="2"/>
  <circle cx="116" cy="76" r="10" fill="#c05621" stroke="#7b341e" stroke-width="2"/>
</svg>`;

const CHIPS = [
  "✨ Write me a poem",
  "🧠 Explain quantum computing",
  "💡 Give me a business idea",
  "🐛 Help me debug my code",
];

showWelcome();

// ── Events ──
sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
});

userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 140) + "px";
});

clearBtn.addEventListener("click", () => { history = []; showWelcome(); userInput.focus(); });

// ── Core ──
async function handleSend(prefill = null) {
  const text = prefill || userInput.value.trim();
  if (!text) return;

  const welcome = chatWindow.querySelector(".welcome");
  if (welcome) welcome.remove();

  appendMessage("user", text);
  userInput.value = "";
  userInput.style.height = "auto";

  const loader = appendLoading();
  setDisabled(true);

  try {
    const reply = await fetchReply(text);
    loader.remove();
    appendMessage("ai", reply);
    history.push({ role: "assistant", content: reply });
  } catch (err) {
    loader.remove();
    appendMessage("error", err.message || "Something went wrong. Please try again.");
  } finally {
    setDisabled(false);
    userInput.focus();
  }
}

async function fetchReply(message) {
  history.push({ role: "user", content: message });
  const res  = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  const data = await res.json();
  if (!res.ok || data.error) { history.pop(); throw new Error(data.error || `Error ${res.status}`); }
  return data.reply;
}

// ── UI ──
function appendMessage(role, content) {
  const isUser = role === "user";
  const time   = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  const wrapper = document.createElement("div");
  wrapper.className = `message ${role === "error" ? "error ai" : role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.innerHTML = isUser ? "🧑" : BOT_SVG;

  const wrap = document.createElement("div");
  wrap.className = "msg-wrap";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  const ts = document.createElement("div");
  ts.className = "msg-time";
  ts.textContent = time;

  wrap.appendChild(bubble);
  wrap.appendChild(ts);
  wrapper.appendChild(avatar);
  wrapper.appendChild(wrap);
  chatWindow.appendChild(wrapper);
  scrollBottom();
  return wrapper;
}

function appendLoading() {
  const wrapper = document.createElement("div");
  wrapper.className = "message ai loading";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.innerHTML = BOT_SVG;

  const wrap = document.createElement("div");
  wrap.className = "msg-wrap";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';

  wrap.appendChild(bubble);
  wrapper.appendChild(avatar);
  wrapper.appendChild(wrap);
  chatWindow.appendChild(wrapper);
  scrollBottom();
  return wrapper;
}

function showWelcome() {
  chatWindow.innerHTML = `
    <div class="welcome">
      <div class="welcome-face">${BOT_SVG}</div>
      <h2>Hi, I'm Aria! 👋</h2>
      <p>Your personal AI assistant. Ask me anything — I'm here to help!</p>
      <div class="welcome-chips">
        ${CHIPS.map(c => `<button class="chip">${c}</button>`).join("")}
      </div>
    </div>`;

  chatWindow.querySelectorAll(".chip").forEach(btn => {
    btn.addEventListener("click", () => handleSend(btn.textContent));
  });
}

function setDisabled(v) { userInput.disabled = v; sendBtn.disabled = v; }
function scrollBottom()  { chatWindow.scrollTop = chatWindow.scrollHeight; }
