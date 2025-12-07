const anchors = [
  {
    ref: "Psalm 1:2-3",
    text: "His delight is in the law of the LORD... He is like a tree planted by streams of water.",
    theme: "Delight & rootedness",
    prayer: "Ask for joy in Scripture and fruit in season.",
  },
  {
    ref: "Hebrews 4:12",
    text: "The word of God is living and active, sharper than any two-edged sword...",
    theme: "Living word",
    prayer: "Invite God to search motives and shape desires.",
  },
  {
    ref: "2 Timothy 3:16-17",
    text: "All Scripture is breathed out by God and profitable for teaching...",
    theme: "Equipped for every good work",
    prayer: "Thank God for equipping you to serve and love well.",
  },
];

const passages = {
  "Philippians 4:4-9": {
    text: "Rejoice in the Lord always... and the peace of God will guard your hearts and minds.",
    tags: ["Joy", "Anxiety"],
    cross: ["Psalm 37:4", "John 16:33", "1 Peter 5:7"],
    keywords: [
      { word: "Rejoice", note: "Commanded joy rooted in the Lord." },
      { word: "Guard", note: "Military term for protective peace." },
      { word: "Think", note: "Intentional meditation on what is true and lovely." },
    ],
    context:
      "Paul writes from prison, inviting the church to rejoice, pray with gratitude, and meditate on what is true.",
    applications: [
      "Name anxieties, pray specifically, and pair each with gratitude.",
      "Audit your mental diet: what inputs fuel worry or worship?",
      "Choose a daily 'think on these things' replacement thought.",
    ],
  },
  "John 15:1-11": {
    text: "I am the true vine... abide in me and you will bear much fruit; apart from me you can do nothing.",
    tags: ["Abiding", "Fruitfulness"],
    cross: ["Psalm 80:8-9", "Galatians 5:22-23", "1 John 2:6"],
    keywords: [
      { word: "Abide", note: "Remain, dwell, continue in intimate dependence." },
      { word: "Prune", note: "Loving discipline that increases fruit." },
      { word: "Joy", note: "Jesus' own joy placed in disciples." },
    ],
    context:
      "In the upper room discourse, Jesus calls disciples to stay connected to Him as the life source, promising joy and fruit.",
    applications: [
      "Identify practices that keep you aware of Jesus' presence today.",
      "Name a 'pruning' moment God might be using to grow you.",
      "Pray verse 11 over a friend who feels weary.",
    ],
  },
  "Micah 6:6-8": {
    text: "What does the LORD require of you? To act justly, love mercy, and walk humbly with your God.",
    tags: ["Justice", "Mercy"],
    cross: ["Isaiah 1:17", "Luke 11:42", "James 1:27"],
    keywords: [
      { word: "Justice", note: "Align life with God's righteous standards." },
      { word: "Mercy", note: "Steadfast covenant love toward others." },
      { word: "Humbly", note: "Walk low before God, aware of dependence." },
    ],
    context: "Micah confronts empty ritual and calls for embodied faith that mirrors God's heart for people.",
    applications: [
      "List a neighbor in need and one tangible act of mercy this week.",
      "Assess where convenience eclipses justice in your habits.",
      "Pray the verse before meetings to posture your heart.",
    ],
  },
};

const flashcards = [
  { ref: "Romans 12:2", text: "Do not be conformed to this world, but be transformed by the renewal of your mind..." },
  { ref: "Joshua 1:8", text: "Meditate on the Book of the Law day and night, so you may be careful to do all that is written." },
  { ref: "Psalm 119:105", text: "Your word is a lamp to my feet and a light to my path." },
];

const quizQuestions = [
  {
    question: "According to John 15, what is the result of abiding in Jesus?",
    options: [
      "Growing in wealth",
      "Bearing much fruit",
      "Escaping hardship",
      "Learning secret knowledge",
    ],
    answer: 1,
    explanation: "Abiding produces fruit and joy, not immunity from pruning or hardship.",
  },
  {
    question: "Micah 6:8 highlights which trio?",
    options: ["Faith, hope, love", "Justice, mercy, humility", "Prayer, fasting, giving", "Joy, peace, patience"],
    answer: 1,
    explanation: "The prophet summarizes true devotion as justice, mercy, and humble walking with God.",
  },
  {
    question: "Philippians 4:6-7 ties God's peace to what practice?",
    options: ["Studying Greek", "Serving the poor", "Prayer with thanksgiving", "Fasting weekly"],
    answer: 2,
    explanation: "Paul links peace with bringing requests to God with gratitude.",
  },
];

const characters = [
  {
    name: "Ruth",
    era: "Judges",
    summary: "A Moabite widow whose loyalty and courage led to redemption and inclusion in Jesus' lineage.",
    virtues: ["Loyal love", "Courage"],
    struggle: "Loss and uncertainty",
    passages: ["Ruth 1:16-17", "Ruth 2:12"],
  },
  {
    name: "David",
    era: "United Kingdom",
    summary: "Shepherd king, poet of the Psalms, who modeled repentance after failure.",
    virtues: ["Worship", "Courage"],
    struggle: "Impulsiveness",
    passages: ["1 Samuel 17", "Psalm 51"],
  },
  {
    name: "Mary of Bethany",
    era: "Gospels",
    summary: "Disciple who sat at Jesus' feet and anointed Him before His death, valuing presence over busyness.",
    virtues: ["Devotion", "Discernment"],
    struggle: "Grief",
    passages: ["Luke 10:38-42", "John 12:1-8"],
  },
];

const timelineEvents = [
  {
    era: "Creation & Fall",
    note: "God creates, humanity falls, promise of a future Deliverer (Genesis 3:15).",
  },
  {
    era: "Patriarchs",
    note: "Abrahamic covenant launches a family blessed to bless the nations.",
  },
  {
    era: "Exodus & Law",
    note: "God rescues Israel, gives the law, and forms a worshiping people.",
  },
  {
    era: "Kings & Prophets",
    note: "Monarchy rises and falls; prophets call for covenant faithfulness and justice.",
  },
  {
    era: "Exile & Return",
    note: "Judah exiled, then restored; hope grows for a Messianic King.",
  },
  {
    era: "Jesus & Early Church",
    note: "Christ's life, death, resurrection, and the Spirit empowering the church's mission.",
  },
  {
    era: "New Creation",
    note: "Consummation of all things; God dwells with His people forever.",
  },
];

const planTemplates = {
  gospel: ["Matthew 5", "Mark 1", "Luke 15", "John 3", "John 15"],
  wisdom: ["Psalm 1", "Psalm 23", "Proverbs 3", "Proverbs 31", "Ecclesiastes 3"],
  pauline: ["Romans 8", "1 Corinthians 13", "Ephesians 2", "Philippians 2", "Colossians 3"],
  prophets: ["Isaiah 40", "Jeremiah 29", "Daniel 6", "Micah 6", "Habakkuk 3"],
};

const state = {
  flashIndex: 0,
  flashHidden: true,
  questionIndex: 0,
  notes: JSON.parse(localStorage.getItem("rooted_notes") || "[]"),
  prayers: JSON.parse(localStorage.getItem("rooted_prayers") || "[]"),
};

function $(selector) {
  return document.querySelector(selector);
}

function updateAnchor() {
  const anchor = anchors[Math.floor(Math.random() * anchors.length)];
  $("#anchor-ref").textContent = anchor.ref;
  $("#anchor-text").textContent = anchor.text;
  $("#anchor-theme").textContent = anchor.theme;
  $("#anchor-prayer").textContent = anchor.prayer;
}

function populatePassages() {
  const select = $("#passage-select");
  Object.keys(passages).forEach((p) => {
    const option = document.createElement("option");
    option.value = p;
    option.textContent = p;
    select.appendChild(option);
  });
  select.addEventListener("change", () => renderPassage(select.value));
  renderPassage(select.value || Object.keys(passages)[0]);
}

function renderPassage(key) {
  const p = passages[key];
  $("#passage-text").textContent = p.text;
  $("#passage-context").textContent = p.context;

  const meta = $("#passage-meta");
  meta.innerHTML = "";
  p.tags.forEach((t) => {
    const pill = document.createElement("div");
    pill.className = "pill";
    pill.textContent = t;
    meta.appendChild(pill);
  });

  const cross = $("#cross-list");
  cross.innerHTML = "";
  p.cross.forEach((c) => {
    const li = document.createElement("li");
    li.textContent = c;
    cross.appendChild(li);
  });

  const keywords = $("#keyword-list");
  keywords.innerHTML = "";
  p.keywords.forEach((k) => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${k.word}</strong><br>${k.note}`;
    keywords.appendChild(li);
  });

  const apps = $("#application-list");
  apps.innerHTML = "";
  p.applications.forEach((a) => {
    const card = document.createElement("div");
    card.className = "card-inline";
    card.textContent = a;
    apps.appendChild(card);
  });
}

function generatePlan(evt) {
  evt.preventDefault();
  const name = $("#plan-name").value.trim();
  const focus = $("#plan-focus").value;
  const pace = Number($("#plan-pace").value) || 1;
  const days = Number($("#plan-days").value) || 7;
  if (!name) return;

  $("#plans-created").textContent = Number($("#plans-created").textContent) + 1;
  const template = planTemplates[focus];
  const plan = Array.from({ length: days }, (_, i) => {
    const passage = template[(i * pace) % template.length];
    return `Day ${i + 1}: ${passage}`;
  });

  $("#preview-title").textContent = name;
  $("#preview-badge").textContent = `${days} days · ${pace}/day`;

  const list = $("#preview-list");
  list.innerHTML = "";
  plan.forEach((item) => {
    const div = document.createElement("div");
    div.className = "plan-item";
    div.textContent = item;
    list.appendChild(div);
  });
}

function renderFlashcard() {
  const card = flashcards[state.flashIndex % flashcards.length];
  $("#flash-ref").textContent = card.ref;
  $("#flash-text").textContent = state.flashHidden ? "Tap reveal to view" : card.text;
  $("#flash-badge").textContent = `${state.flashIndex + 1}/${flashcards.length}`;
}

function nextFlash() {
  state.flashIndex = (state.flashIndex + 1) % flashcards.length;
  state.flashHidden = true;
  renderFlashcard();
}

function toggleFlash() {
  state.flashHidden = !state.flashHidden;
  renderFlashcard();
}

function renderQuiz() {
  const current = quizQuestions[state.questionIndex % quizQuestions.length];
  $("#quiz-question").textContent = current.question;
  const options = $("#quiz-options");
  options.innerHTML = "";
  current.options.forEach((opt, idx) => {
    const btn = document.createElement("button");
    btn.className = "button button--ghost";
    btn.textContent = opt;
    btn.addEventListener("click", () => gradeQuiz(idx));
    options.appendChild(btn);
  });
  $("#quiz-feedback").textContent = "";
}

function gradeQuiz(choice) {
  const current = quizQuestions[state.questionIndex % quizQuestions.length];
  const feedback = choice === current.answer ? "Correct!" : "Try again.";
  const detail = choice === current.answer ? current.explanation : "Review the passage above.";
  $("#quiz-feedback").textContent = `${feedback} ${detail}`;
}

function nextQuestion() {
  state.questionIndex = (state.questionIndex + 1) % quizQuestions.length;
  renderQuiz();
}

function saveNotes() {
  localStorage.setItem("rooted_notes", JSON.stringify(state.notes));
}

function savePrayers() {
  localStorage.setItem("rooted_prayers", JSON.stringify(state.prayers));
  $("#prayers-logged").textContent = state.prayers.length;
}

function addNote(evt) {
  evt.preventDefault();
  const ref = $("#note-ref").value.trim();
  const text = $("#note-text").value.trim();
  if (!ref || !text) return;
  state.notes.unshift({ ref, text, created: new Date().toLocaleDateString() });
  saveNotes();
  renderNotes();
  evt.target.reset();
}

function addPrayer(evt) {
  evt.preventDefault();
  const text = $("#prayer-text").value.trim();
  const status = $("#prayer-status").value;
  if (!text) return;
  state.prayers.unshift({ text, status, created: new Date().toLocaleDateString() });
  savePrayers();
  renderPrayers();
  evt.target.reset();
}

function renderNotes() {
  const list = $("#notes-list");
  list.innerHTML = state.notes
    .map((note) => `<div class="note-item"><strong>${note.ref}</strong><span>${note.text}</span><br><small>${note.created}</small></div>`)
    .join("");
}

function renderPrayers() {
  const list = $("#prayers-list");
  list.innerHTML = state.prayers
    .map((p) => `<div class="prayer-item"><strong>${p.text}</strong><span class="status">${p.status}</span><br><small>${p.created}</small></div>`)
    .join("");
}

function setupTabs() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((c) => c.classList.add("hidden"));
      tab.classList.add("active");
      document.getElementById(`${tab.dataset.tab}-list`).classList.remove("hidden");
    });
  });
}

function renderCharacters() {
  const grid = $("#character-grid");
  grid.innerHTML = "";
  characters.forEach((c) => {
    const card = document.createElement("div");
    card.className = "character-card";
    card.innerHTML = `<div class="character-meta"><span class="pill">${c.era}</span></div><h4>${c.name}</h4><p>${c.summary}</p><p><strong>Virtues:</strong> ${c.virtues.join(", ")}</p><p><strong>Struggle:</strong> ${c.struggle}</p><p><strong>Passages:</strong> ${c.passages.join(", ")}</p>`;
    grid.appendChild(card);
  });
}

function renderTimeline() {
  const list = $("#timeline");
  list.innerHTML = "";
  timelineEvents.forEach((ev) => {
    const item = document.createElement("div");
    item.className = "timeline-item";
    item.innerHTML = `<span class="era">${ev.era}</span><span>${ev.note}</span>`;
    list.appendChild(item);
  });
}

function renderStats() {
  $("#prayers-logged").textContent = state.prayers.length;
}

function init() {
  updateAnchor();
  populatePassages();
  renderFlashcard();
  renderQuiz();
  renderNotes();
  renderPrayers();
  renderCharacters();
  renderTimeline();
  renderStats();
  setupTabs();

  $("#plan-form").addEventListener("submit", generatePlan);
  $("#shuffle-anchor").addEventListener("click", updateAnchor);
  $("#show-flash").addEventListener("click", toggleFlash);
  $("#next-flash").addEventListener("click", nextFlash);
  $("#next-question").addEventListener("click", nextQuestion);
  $("#note-form").addEventListener("submit", addNote);
  $("#prayer-form").addEventListener("submit", addPrayer);
}

document.addEventListener("DOMContentLoaded", init);
