const SIDEBAR_STATE_KEY = "lc2024.sidebar.visitedLessons";

const TOEIC_TESTS = [
  {
    num: "01",
    color: "blue",
    folder: "Test 1",
    prefix: "T1",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
  {
    num: "02",
    color: "purple",
    folder: "Test 2",
    prefix: "T2",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
  {
    num: "03",
    color: "green",
    folder: "Test 3",
    prefix: "T3",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
  {
    num: "04",
    color: "orange",
    folder: "Test 4",
    prefix: "T4",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
  {
    num: "05",
    color: "red",
    folder: "Test 5",
    prefix: "T5",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
  {
    num: "06",
    color: "indigo",
    folder: "Test 6",
    prefix: "T6",
    part3: [
      "32-34",
      "35-37",
      "38-40",
      "41-43",
      "44-46",
      "47-49",
      "50-52",
      "53-55",
      "56-58",
      "59-61",
      "62-64",
      "65-67",
      "68-70",
    ],
    part4: [
      "71-73",
      "74-76",
      "77-79",
      "80-82",
      "83-85",
      "86-88",
      "89-91",
      "92-94",
      "95-97",
      "98-100",
    ],
  },
];

function parseLessonState(rawValue) {
  if (!rawValue) return [];

  const decodedValue = safeDecodeURIComponent(rawValue);

  try {
    const parsed = JSON.parse(decodedValue);
    if (Array.isArray(parsed)) return parsed.filter(Boolean);
    if (parsed && Array.isArray(parsed.visitedLessons)) {
      return parsed.visitedLessons.filter(Boolean);
    }
  } catch (error) {
    // Fall through to support older hash formats.
  }

  return decodedValue
    .split(/[|,]/)
    .map((lessonFile) => lessonFile.trim())
    .filter(Boolean);
}

function safeDecodeURIComponent(value) {
  try {
    return decodeURIComponent(value);
  } catch (error) {
    return value;
  }
}

function isLessonFileName(fileName) {
  return /^LC-T\d+-P\d+-Q[\d-]+\.html$/.test(fileName);
}

function readVisitedLessons() {
  const visitedLessons = new Set();

  try {
    const hashParams = new URLSearchParams(window.location.hash.slice(1));
    parseLessonState(hashParams.get("visited")).forEach((lessonFile) => {
      if (isLessonFileName(lessonFile)) visitedLessons.add(lessonFile);
    });
  } catch (error) {
    // Ignore malformed hash values.
  }

  try {
    parseLessonState(localStorage.getItem(SIDEBAR_STATE_KEY)).forEach(
      (lessonFile) => {
        if (isLessonFileName(lessonFile)) visitedLessons.add(lessonFile);
      },
    );
  } catch (error) {
    // localStorage can be restricted in some file-based browser sessions.
  }

  try {
    parseLessonState(window.name).forEach((lessonFile) => {
      if (isLessonFileName(lessonFile)) visitedLessons.add(lessonFile);
    });
  } catch (error) {
    // Ignore invalid window.name payloads.
  }

  return visitedLessons;
}

function writeVisitedLessons(visitedLessons) {
  const serialized = JSON.stringify([...visitedLessons]);

  try {
    localStorage.setItem(SIDEBAR_STATE_KEY, serialized);
  } catch (error) {
    // window.name below keeps same-tab navigation working without reloads.
  }

  try {
    window.name = serialized;
  } catch (error) {
    // Ignore window.name write failures.
  }
}

function clearVisitedLessons() {
  try {
    localStorage.removeItem(SIDEBAR_STATE_KEY);
  } catch (error) {
    // Ignore storage access errors.
  }

  try {
    window.name = "";
  } catch (error) {
    // Ignore window.name clear failures.
  }

  if (window.location.hash) {
    try {
      history.replaceState(null, "", window.location.href.split("#")[0]);
    } catch (error) {
      window.location.hash = "";
    }
  }
}

function getProjectRoot() {
  const currentPath = window.location.pathname;
  const marker = "/LC2024/";
  const markerIndex = currentPath.indexOf(marker);

  if (markerIndex >= 0) {
    return currentPath.slice(0, markerIndex + marker.length);
  }

  return currentPath.replace(/(?:Test%20\d|Test \d)\/[^/]*$/, "");
}

function splitChunkText(text) {
  return text
    .replace(/\s*\/\s*/g, "\n")
    .split("\n")
    .map((part) => part.replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

function scrollSidebarLessonIntoView(link, behavior = "auto") {
  const sidebar = document.querySelector(".sidebar");
  if (!sidebar || !link) return;

  const sidebarRect = sidebar.getBoundingClientRect();
  const linkRect = link.getBoundingClientRect();
  const targetTop =
    sidebar.scrollTop +
    (linkRect.top - sidebarRect.top) -
    sidebar.clientHeight / 2 +
    linkRect.height / 2;

  sidebar.scrollTo({
    top: Math.max(0, targetTop),
    behavior,
  });
}

function enhanceChunkingLayout() {
  const shadowingContainer = document.getElementById("shadowingContainer");
  if (
    !shadowingContainer ||
    shadowingContainer.dataset.chunkEnhanced === "true"
  ) {
    return;
  }

  shadowingContainer
    .querySelectorAll(".flex.gap-4 .w-full > div")
    .forEach((contentHost) => {
      const englishElement = contentHost.querySelector("strong");
      const vietnameseElement = contentHost.querySelector(".chunk-vi");
      if (!englishElement || !vietnameseElement) return;

      const englishChunks = splitChunkText(englishElement.textContent || "");
      const vietnameseChunks = splitChunkText(
        vietnameseElement.textContent || "",
      );
      const chunkCount = Math.max(
        englishChunks.length,
        vietnameseChunks.length,
      );
      if (chunkCount === 0) return;

      contentHost.classList.add("chunk-grid");
      contentHost.replaceChildren();

      for (let index = 0; index < chunkCount; index += 1) {
        const chunkPair = document.createElement("span");
        chunkPair.className = "chunk-pair";
        if (index < chunkCount - 1) {
          chunkPair.classList.add("has-next");
        }

        const englishLine = document.createElement("strong");
        englishLine.className = "chunk-en";
        englishLine.textContent = englishChunks[index] || "";

        const vietnameseLine = document.createElement("span");
        vietnameseLine.className = "chunk-vi";
        vietnameseLine.textContent = vietnameseChunks[index] || "";

        chunkPair.append(englishLine, vietnameseLine);
        contentHost.appendChild(chunkPair);
      }
    });

  shadowingContainer.dataset.chunkEnhanced = "true";
}

let appInitialized = false;

function initApp() {
  if (appInitialized) return;
  appInitialized = true;

  injectSidebar();
  injectAudioPlayer();
  enhanceChunkingLayout();
  initTranslationToggle();
  initAnswerChecker();
  initPracticeMode();
}

function initPracticeMode() {
  const sections = document.querySelectorAll('section');
  let questionsSection;

  sections.forEach(s => {
    const h2 = s.querySelector('h2');
    if (h2 && h2.querySelector('.fa-question-circle')) questionsSection = s;
  });

  if (!questionsSection) return;

  const questionBlocks = questionsSection.querySelectorAll('.bg-slate-50.p-5');
  questionBlocks.forEach((block) => {
    const grid = block.querySelector('.grid');
    const questionTrans = block.querySelector('.text-slate-500.text-sm.mb-4');
    const explanation = block.querySelector('.mt-4.p-4, .mt-4.p-3');
    
    if (!grid) return;

    // Hide question translation
    if (questionTrans) questionTrans.classList.add('practice-hidden');
    // Hide explanation
    if (explanation) explanation.classList.add('practice-hidden');

    const options = grid.querySelectorAll('div');
    options.forEach((opt) => {
      // Detect if this is the correct option
      const isCorrect = opt.classList.contains('font-bold') || opt.querySelector('.font-bold');
      
      // Clean text to separate English and Vietnamese
      const fullText = opt.innerText.trim();
      const lines = fullText.split('\n').map(l => l.trim()).filter(Boolean);
      
      const letterMatch = lines[0].match(/^\(([A-D])\)/);
      const letter = letterMatch ? letterMatch[1] : "";
      const englishText = lines[0].replace(/^\([A-D]\)/, "").trim();
      const vietnameseText = lines[1] || "";

      // Rebuild option structure
      opt.className = 'question-option';
      opt.dataset.letter = letter;
      if (isCorrect) opt.dataset.correct = "true";

      opt.innerHTML = `
        <div class="flex items-start">
          <span class="option-letter">${letter}</span>
          <div class="flex-grow">
            <div class="font-medium text-slate-800">${englishText}</div>
            <div class="text-slate-500 text-sm mt-1 practice-hidden vi-trans">${vietnameseText}</div>
          </div>
        </div>
      `;

      opt.addEventListener('click', () => {
        if (block.dataset.submitted === "true") return;
        grid.querySelectorAll('.question-option').forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        checkSubmitReady();
      });
    });
  });

  const submitBtn = document.createElement('button');
  submitBtn.id = 'submitPracticeBtn';
  submitBtn.innerHTML = '<i class="fas fa-paper-plane mr-2"></i> Nộp bài & Xem kết quả';
  submitBtn.disabled = true;
  questionsSection.appendChild(submitBtn);

  function checkSubmitReady() {
    const totalQuestions = questionBlocks.length;
    const answeredQuestions = questionsSection.querySelectorAll('.question-option.selected').length;
    submitBtn.disabled = answeredQuestions < totalQuestions;
  }

  submitBtn.addEventListener('click', () => {
    let score = 0;
    questionBlocks.forEach((block) => {
      block.dataset.submitted = "true";
      
      // Reveal question translation
      const qTrans = block.querySelector('.text-slate-500.text-sm.mb-4');
      if (qTrans) qTrans.classList.remove('practice-hidden');

      const selected = block.querySelector('.question-option.selected');
      const correct = block.querySelector('.question-option[data-correct="true"]');
      const explanation = block.querySelector('.practice-hidden:not(.vi-trans)');
      
      // Reveal all option translations
      block.querySelectorAll('.vi-trans').forEach(vi => vi.classList.remove('practice-hidden'));

      if (selected) {
        if (selected.dataset.correct === "true") {
          selected.classList.add('correct');
          score++;
        } else {
          selected.classList.add('wrong');
          if (correct) correct.classList.add('correct');
        }
      }

      if (explanation) {
        explanation.classList.remove('practice-hidden');
        explanation.classList.add('explanation-card');
      }
    });

    submitBtn.innerHTML = `<i class="fas fa-check-double mr-2"></i> Kết quả: ${score}/${questionBlocks.length}`;
    submitBtn.disabled = true;
    submitBtn.classList.replace('bg-blue-600', 'bg-green-600');
  });
}

if (
  document.readyState === "loading" &&
  !document.querySelector(".main-container")
) {
  document.addEventListener("DOMContentLoaded", initApp, { once: true });
} else {
  initApp();
}

function initTranslationToggle() {
  const toggleBtn = document.getElementById("toggleTranslation");
  const shadowingContainer = document.getElementById("shadowingContainer");
  if (!toggleBtn || !shadowingContainer) return;

  let isHidden = false;
  toggleBtn.addEventListener("click", () => {
    isHidden = !isHidden;

    if (isHidden) {
      shadowingContainer.classList.add("hidden-vi");
      toggleBtn.innerHTML = '<i class="fas fa-eye mr-1"></i> Hiện tiếng Việt';
      toggleBtn.classList.replace("bg-purple-100", "bg-slate-200");
      toggleBtn.classList.replace("text-purple-700", "text-slate-700");
      return;
    }

    shadowingContainer.classList.remove("hidden-vi");
    toggleBtn.innerHTML = '<i class="fas fa-eye-slash mr-1"></i> Ẩn tiếng Việt';
    toggleBtn.classList.replace("bg-slate-200", "bg-purple-100");
    toggleBtn.classList.replace("text-slate-700", "text-purple-700");
  });
}

function initAnswerChecker() {
  const checkBtn = document.getElementById("checkAnswersBtn");
  const inputs = document.querySelectorAll(".input-blank");
  if (!checkBtn || inputs.length === 0) return;

  checkBtn.addEventListener("click", () => {
    let correctCount = 0;

    inputs.forEach((input) => {
      const correctAnswer = (input.getAttribute("data-answer") || "")
        .trim()
        .toLowerCase();
      const userAnswer = input.value.trim().toLowerCase();

      input.classList.remove("input-correct", "input-wrong");
      if (userAnswer === correctAnswer) {
        input.classList.add("input-correct");
        correctCount += 1;
      } else {
        input.classList.add("input-wrong");
      }
    });

    if (correctCount === inputs.length) {
      checkBtn.innerHTML =
        '<i class="fas fa-star text-yellow-300 mr-2"></i> Xuất Sắc!';
      checkBtn.classList.replace("bg-cyan-500", "bg-green-500");
      checkBtn.classList.replace("hover:bg-cyan-600", "hover:bg-green-600");
      return;
    }

    checkBtn.innerHTML = `<i class="fas fa-redo mr-2"></i> Đúng ${correctCount}/${inputs.length} - Thử lại`;
    checkBtn.classList.replace("bg-green-500", "bg-cyan-500");
    checkBtn.classList.replace("hover:bg-green-600", "hover:bg-cyan-600");
  });
}

function injectAudioPlayer() {
  const currentPath = window.location.pathname;
  const fileName = currentPath.split("/").pop() || "";
  const match = fileName.match(/LC-T(\d+)-P\d+-Q([\d-]+)\.html/);
  if (!match) return;

  const testNum = match[1].padStart(2, "0");
  const qRange = match[2];
  const audioFile = `Test_${testNum}-${qRange}.mp3`;
  const audioPath = `${getProjectRoot()}audio/Test_${testNum}/${audioFile}`;

  const audioHTML = `
    <div class="sticky-audio-container">
      <section class="glass-card p-4 md:p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-100 shadow-inner">
        <div class="flex items-center gap-6">
          <div class="flex-grow w-full">
            <audio id="mainAudio" controls class="w-full h-10 mb-4 rounded-lg">
              <source src="${audioPath}" type="audio/mpeg">
            </audio>

            <div class="flex flex-wrap gap-2 items-center justify-start">
              <button id="back5s" class="bg-slate-600 hover:bg-slate-700 text-white px-3 py-2 rounded-lg text-xs font-bold shadow-md transition flex items-center" title="Lùi 5s - Phím tắt: ←">
                <i class="fas fa-backward mr-1"></i> -5s
              </button>

              <button id="skipIntroBtn" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition transform active:scale-95 flex items-center" title="Bắt đầu - Phím tắt: S">
                <i class="fas fa-forward-step mr-2"></i> Bắt đầu <span class="ml-1 opacity-60 font-normal">(S)</span>
              </button>

              <button id="forward5s" class="bg-slate-600 hover:bg-slate-700 text-white px-3 py-2 rounded-lg text-xs font-bold shadow-md transition flex items-center" title="Tiến 5s - Phím tắt: →">
                +5s <i class="fas fa-forward ml-1"></i>
              </button>

              <div class="h-6 w-px bg-slate-300 mx-2"></div>

              <button id="setPointABtn" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition flex items-center" title="Phím tắt: A">
                <i class="fas fa-map-pin mr-2"></i> Điểm A <span class="ml-1 opacity-60 font-normal">(A)</span> <span id="labelA" class="ml-2 bg-black/20 px-1.5 py-0.5 rounded text-[10px]">--:--</span>
              </button>

              <button id="setPointBBtn" class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition flex items-center" title="Phím tắt: B">
                <i class="fas fa-map-pin mr-2"></i> Điểm B <span class="ml-1 opacity-60 font-normal">(B)</span> <span id="labelB" class="ml-2 bg-black/20 px-1.5 py-0.5 rounded text-[10px]">--:--</span>
              </button>

              <button id="clearLoopBtn" class="bg-slate-400 hover:bg-slate-500 text-white px-4 py-2 rounded-lg text-xs font-bold shadow-md transition flex items-center opacity-50 pointer-events-none" title="Phím tắt: C">
                <i class="fas fa-times-circle mr-2"></i> Xóa <span class="ml-1 opacity-60 font-normal">(C)</span>
              </button>

              <div class="h-6 w-px bg-slate-300 mx-2"></div>

              <div class="flex items-center bg-white/50 px-3 py-1.5 rounded-lg border border-slate-200">
                <span class="text-[10px] font-bold text-slate-500 uppercase mr-3">Speed</span>
                <button id="speedDown" class="w-6 h-6 flex items-center justify-center rounded bg-white border border-slate-200 text-slate-600 hover:bg-blue-50 transition">-</button>
                <span id="speedValue" class="mx-3 text-xs font-bold text-blue-700 min-w-[35px] text-center">1.1x</span>
                <button id="speedUp" class="w-6 h-6 flex items-center justify-center rounded bg-white border border-slate-200 text-slate-600 hover:bg-blue-50 transition">+</button>
              </div>

              <div id="loopStatus" class="ml-auto text-[10px] font-bold text-indigo-600 uppercase tracking-tighter hidden animate-bounce">
                <i class="fas fa-sync fa-spin mr-1"></i> Đang Lặp A-B
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  `;

  const container = document.querySelector(".main-container");
  if (!container) return;

  container.insertAdjacentHTML("afterbegin", audioHTML);
  initAudioControls();
}

function initAudioControls() {
  const audio = document.getElementById("mainAudio");
  if (!audio) return;

  const skipBtn = document.getElementById("skipIntroBtn");
  const backBtn = document.getElementById("back5s");
  const forwardBtn = document.getElementById("forward5s");
  const btnA = document.getElementById("setPointABtn");
  const btnB = document.getElementById("setPointBBtn");
  const btnClear = document.getElementById("clearLoopBtn");
  const labelA = document.getElementById("labelA");
  const labelB = document.getElementById("labelB");
  const loopStatus = document.getElementById("loopStatus");
  const speedDown = document.getElementById("speedDown");
  const speedUp = document.getElementById("speedUp");
  const speedValue = document.getElementById("speedValue");

  if (
    !skipBtn ||
    !backBtn ||
    !forwardBtn ||
    !btnA ||
    !btnB ||
    !btnClear ||
    !labelA ||
    !labelB ||
    !loopStatus ||
    !speedDown ||
    !speedUp ||
    !speedValue
  ) {
    return;
  }

  audio.playbackRate = 1.1;

  let pointA = null;
  let pointB = null;

  const formatTime = (time) => {
    const min = Math.floor(time / 60);
    const sec = Math.floor(time % 60);
    return `${min}:${sec.toString().padStart(2, "0")}`;
  };

  const actionSetA = () => {
    pointA = audio.currentTime;
    labelA.innerText = formatTime(pointA);
    checkLoop();
  };

  const actionSkip = () => {
    audio.currentTime = 5;
    actionSetA();
    audio.play().catch(() => {
      console.log(
        "Auto-play prevented by browser. Click 'Bắt đầu' or press 'S' to start.",
      );
    });
  };

  const actionSeek = (delta) => {
    const targetTime = Math.max(0, audio.currentTime + delta);
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      audio.currentTime = Math.min(audio.duration, targetTime);
      return;
    }

    audio.currentTime = targetTime;
  };

  const actionSetB = () => {
    pointB = audio.currentTime;
    labelB.innerText = formatTime(pointB);
    checkLoop();
  };

  const actionClear = () => {
    pointA = null;
    pointB = null;
    labelA.innerText = "--:--";
    labelB.innerText = "--:--";
    loopStatus.classList.add("hidden");
    btnClear.classList.add("opacity-50", "pointer-events-none");
  };

  const actionTogglePlay = () => {
    if (audio.paused) {
      audio.play();
      return;
    }

    audio.pause();
  };

  const updateSpeed = (delta) => {
    const currentSpeed = parseFloat(audio.playbackRate.toFixed(1));
    const newSpeed = Math.max(0.5, Math.min(2.0, currentSpeed + delta));
    audio.playbackRate = newSpeed;
    speedValue.innerText = `${newSpeed.toFixed(1)}x`;
  };

  speedDown.addEventListener("click", () => updateSpeed(-0.1));
  speedUp.addEventListener("click", () => updateSpeed(0.1));
  skipBtn.addEventListener("click", actionSkip);
  backBtn.addEventListener("click", () => actionSeek(-5));
  forwardBtn.addEventListener("click", () => actionSeek(5));
  btnA.addEventListener("click", actionSetA);
  btnB.addEventListener("click", actionSetB);
  btnClear.addEventListener("click", actionClear);

  document.addEventListener("keydown", (event) => {
    if (
      event.target instanceof HTMLElement &&
      (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA")
    ) {
      return;
    }

    const key = event.key.toLowerCase();
    if (key === "s") {
      event.preventDefault();
      actionSkip();
    } else if (key === "a") {
      event.preventDefault();
      actionSetA();
    } else if (key === "b") {
      event.preventDefault();
      actionSetB();
    } else if (key === "c") {
      event.preventDefault();
      actionClear();
    } else if (key === " ") {
      event.preventDefault();
      actionTogglePlay();
    } else if (key === "[") {
      event.preventDefault();
      updateSpeed(-0.1);
    } else if (key === "]") {
      event.preventDefault();
      updateSpeed(0.1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      actionSeek(-5);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      actionSeek(5);
    }
  });

  audio.addEventListener("timeupdate", () => {
    if (pointA !== null && pointB !== null && audio.currentTime >= pointB) {
      audio.currentTime = pointA;
    }
  });

  function checkLoop() {
    if (pointA === null || pointB === null) return;

    if (pointA > pointB) {
      const temp = pointA;
      pointA = pointB;
      pointB = temp;
      labelA.innerText = formatTime(pointA);
      labelB.innerText = formatTime(pointB);
    }

    loopStatus.classList.remove("hidden");
    btnClear.classList.remove("opacity-50", "pointer-events-none");
  }

  actionSkip();
}

function injectSidebar() {
  const currentFileName = window.location.pathname.split("/").pop() || "";
  const projectRoot = getProjectRoot();
  const getPath = (subPath) => `${projectRoot}${subPath}`;
  const visitedLessons = readVisitedLessons();

  if (isLessonFileName(currentFileName)) {
    visitedLessons.add(currentFileName);
    writeVisitedLessons(visitedLessons);
  }

  let sidebarHTML = `
    <aside class="sidebar" aria-label="Danh sách bài học">
      <div class="sidebar-top">
        <a href="${getPath("index.html")}" class="sidebar-brand">
          <i class="fas fa-graduation-cap"></i>
          <span>TOEIC Coach</span>
        </a>

        <button id="sidebarRefreshBtn" class="sidebar-refresh" type="button" title="Xóa trạng thái bài đã học">
          <i class="fas fa-arrows-rotate"></i>
          <span>Refresh</span>
        </button>
      </div>

      <div class="sidebar-tree">
  `;

  TOEIC_TESTS.forEach((test) => {
    sidebarHTML += `
      <div class="tree-item">
        <div class="tree-header px-4">
          <i class="fas fa-file-audio mr-2 text-${test.color}-500"></i> Test ${test.num}
        </div>
        <div class="tree-branch">
          <div class="tree-part-label">Part 3</div>
          ${renderLessonLinks(test, "P3", test.part3, currentFileName, visitedLessons, getPath)}

          <div class="tree-part-label mt-2">Part 4</div>
          ${renderLessonLinks(test, "P4", test.part4, currentFileName, visitedLessons, getPath)}
        </div>
      </div>
    `;
  });

  sidebarHTML += `
      </div>
    </aside>
  `;

  const originalContent = document.body.innerHTML;
  document.body.innerHTML = `
    <div class="app-wrapper">
      ${sidebarHTML}
      <main class="main-content">
        ${originalContent}
      </main>
    </div>
  `;

  bindSidebarEvents(visitedLessons);

  requestAnimationFrame(() => {
    const currentLink = document.querySelector(
      '.tree-link[data-current="true"]',
    );
    scrollSidebarLessonIntoView(currentLink, "auto");
  });
}

function renderLessonLinks(
  test,
  part,
  ranges,
  currentFileName,
  visitedLessons,
  getPath,
) {
  return ranges
    .map((qRange) => {
      const fileName = `LC-${test.prefix}-${part}-Q${qRange}.html`;
      const isCurrent = fileName === currentFileName;
      const isActive = visitedLessons.has(fileName);
      const classes = ["tree-link"];

      if (isActive) classes.push("active");
      if (isCurrent) classes.push("current");

      return `<a href="${getPath(`${test.folder}/${fileName}`)}" data-lesson-file="${fileName}" data-current="${isCurrent ? "true" : "false"}" class="${classes.join(" ")}">Q${qRange}</a>`;
    })
    .join("");
}

function bindSidebarEvents(visitedLessons) {
  document.querySelectorAll(".tree-link").forEach((link) => {
    link.addEventListener("click", () => {
      const lessonFile = link.getAttribute("data-lesson-file");
      if (!lessonFile) return;

      visitedLessons.add(lessonFile);
      writeVisitedLessons(visitedLessons);
      link.classList.add("active");
    });
  });

  const refreshBtn = document.getElementById("sidebarRefreshBtn");
  if (!refreshBtn) return;

  refreshBtn.addEventListener("click", () => {
    visitedLessons.clear();
    clearVisitedLessons();

    document.querySelectorAll(".tree-link").forEach((link) => {
      link.classList.remove("active", "current");
      link.dataset.current = "false";
    });

    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
      sidebar.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
}
