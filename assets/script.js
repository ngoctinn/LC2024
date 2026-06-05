document.addEventListener('DOMContentLoaded', () => {
    // 1. Inject Navigation Sidebar
    injectSidebar();

    // 2. Inject Audio Player
    injectAudioPlayer();

    // 3. Toggle Translation
    const toggleBtn = document.getElementById('toggleTranslation');
    const shadowingContainer = document.getElementById('shadowingContainer');
    if (toggleBtn && shadowingContainer) {
        let isHidden = false;
        toggleBtn.addEventListener('click', () => {
            isHidden = !isHidden;
            if (isHidden) {
                shadowingContainer.classList.add('hidden-vi');
                toggleBtn.innerHTML = '<i class="fas fa-eye mr-1"></i> Hiện tiếng Việt';
                toggleBtn.classList.replace('bg-purple-100', 'bg-slate-200');
                toggleBtn.classList.replace('text-purple-700', 'text-slate-700');
            } else {
                shadowingContainer.classList.remove('hidden-vi');
                toggleBtn.innerHTML = '<i class="fas fa-eye-slash mr-1"></i> Ẩn tiếng Việt';
                toggleBtn.classList.replace('bg-slate-200', 'bg-purple-100');
                toggleBtn.classList.replace('text-slate-700', 'text-purple-700');
            }
        });
    }

    // 4. Check Fill-in-the-blank Answers
    const checkBtn = document.getElementById('checkAnswersBtn');
    const inputs = document.querySelectorAll('.input-blank');
    if (checkBtn && inputs.length > 0) {
        checkBtn.addEventListener('click', () => {
            let correctCount = 0;
            inputs.forEach(input => {
                const correctAnswer = input.getAttribute('data-answer').toLowerCase();
                const userAnswer = input.value.trim().toLowerCase();
                input.classList.remove('input-correct', 'input-wrong');
                if (userAnswer === correctAnswer) {
                    input.classList.add('input-correct');
                    correctCount++;
                } else {
                    input.classList.add('input-wrong');
                }
            });

            if (correctCount === inputs.length) {
                checkBtn.innerHTML = '<i class="fas fa-star text-yellow-300 mr-2"></i> Xuất Sắc!';
                checkBtn.classList.replace('bg-cyan-500', 'bg-green-500');
                checkBtn.classList.replace('hover:bg-cyan-600', 'hover:bg-green-600');
            } else {
                checkBtn.innerHTML = `<i class="fas fa-redo mr-2"></i> Đúng ${correctCount}/${inputs.length} - Thử lại`;
                checkBtn.classList.replace('bg-green-500', 'bg-cyan-500');
            }
        });
    }

    // 5. Scroll active link into view in sidebar
    const activeLink = document.querySelector('.tree-link.active');
    if (activeLink) {
        activeLink.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

function injectAudioPlayer() {
    const currentPath = window.location.pathname;
    const fileName = currentPath.split('/').pop();
    
    const match = fileName.match(/LC-T(\d+)-P\d+-Q([\d-]+)\.html/);
    if (match) {
        const testNum = match[1].padStart(2, '0');
        const qRange = match[2];
        const audioFile = `Test_${testNum}-${qRange}.mp3`;
        
        const projectRoot = currentPath.substring(0, currentPath.indexOf('/LC2024/') + 8);
        const audioPath = `${projectRoot}audio/Test_${testNum}/${audioFile}`;

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

                                <!-- Speed Control -->
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

        const container = document.querySelector('.main-container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', audioHTML);
            initAudioControls();
        }
    }
}

function initAudioControls() {
    const audio = document.getElementById('mainAudio');
    if (!audio) return;

    const skipBtn = document.getElementById('skipIntroBtn');
    const backBtn = document.getElementById('back5s');
    const forwardBtn = document.getElementById('forward5s');
    const btnA = document.getElementById('setPointABtn');
    const btnB = document.getElementById('setPointBBtn');
    const btnClear = document.getElementById('clearLoopBtn');
    const labelA = document.getElementById('labelA');
    const labelB = document.getElementById('labelB');
    const loopStatus = document.getElementById('loopStatus');
    const speedDown = document.getElementById('speedDown');
    const speedUp = document.getElementById('speedUp');
    const speedValue = document.getElementById('speedValue');

    audio.playbackRate = 1.1;

    let pointA = null;
    let pointB = null;

    const formatTime = (time) => {
        const min = Math.floor(time / 60);
        const sec = Math.floor(time % 60);
        return `${min}:${sec.toString().padStart(2, '0')}`;
    };

    const actionSkip = () => {
        audio.currentTime = 5;
        actionSetA();
        audio.play().catch(err => {
            console.log("Auto-play prevented by browser. Click 'Bắt đầu' or press 'S' to start.");
        });
    };

    const actionSeek = (delta) => {
        audio.currentTime = Math.max(0, Math.min(audio.duration, audio.currentTime + delta));
    };

    const actionSetA = () => {
        pointA = audio.currentTime;
        labelA.innerText = formatTime(pointA);
        checkLoop();
    };

    const actionSetB = () => {
        pointB = audio.currentTime;
        labelB.innerText = formatTime(pointB);
        checkLoop();
    };

    const actionClear = () => {
        pointA = null;
        pointB = null;
        labelA.innerText = '--:--';
        labelB.innerText = '--:--';
        loopStatus.classList.add('hidden');
        btnClear.classList.add('opacity-50', 'pointer-events-none');
    };

    const actionTogglePlay = () => {
        if (audio.paused) audio.play();
        else audio.pause();
    };

    // Speed Control Logic
    const updateSpeed = (delta) => {
        let currentSpeed = parseFloat(audio.playbackRate.toFixed(1));
        let newSpeed = Math.max(0.5, Math.min(2.0, currentSpeed + delta));
        audio.playbackRate = newSpeed;
        speedValue.innerText = newSpeed.toFixed(1) + 'x';
    };

    speedDown.addEventListener('click', () => updateSpeed(-0.1));
    speedUp.addEventListener('click', () => updateSpeed(0.1));

    // Click Listeners
    skipBtn.addEventListener('click', actionSkip);
    backBtn.addEventListener('click', () => actionSeek(-5));
    forwardBtn.addEventListener('click', () => actionSeek(5));
    btnA.addEventListener('click', actionSetA);
    btnB.addEventListener('click', actionSetB);
    btnClear.addEventListener('click', actionClear);

    // Keyboard Listeners
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        const key = e.key.toLowerCase();
        if (key === 's') { e.preventDefault(); actionSkip(); }
        else if (key === 'a') { e.preventDefault(); actionSetA(); }
        else if (key === 'b') { e.preventDefault(); actionSetB(); }
        else if (key === 'c') { e.preventDefault(); actionClear(); }
        else if (key === ' ') { e.preventDefault(); actionTogglePlay(); }
        else if (key === '[') { e.preventDefault(); updateSpeed(-0.1); }
        else if (key === ']') { e.preventDefault(); updateSpeed(0.1); }
        else if (e.key === 'ArrowLeft') { e.preventDefault(); actionSeek(-5); }
        else if (e.key === 'ArrowRight') { e.preventDefault(); actionSeek(5); }
    });

    audio.addEventListener('timeupdate', () => {
        if (pointA !== null && pointB !== null) {
            if (audio.currentTime >= pointB) {
                audio.currentTime = pointA;
            }
        }
    });

    function checkLoop() {
        if (pointA !== null && pointB !== null) {
            if (pointA > pointB) {
                const temp = pointA;
                pointA = pointB;
                pointB = temp;
                labelA.innerText = formatTime(pointA);
                labelB.innerText = formatTime(pointB);
            }
            loopStatus.classList.remove('hidden');
            btnClear.classList.remove('opacity-50', 'pointer-events-none');
        }
    }

    // Auto-skip and set point A on load
    // Note: Most browsers require a user interaction to play audio. 
    // This will set the time and mark A, and attempt to play.
    actionSkip();
}

function injectSidebar() {
    const currentPath = window.location.pathname;
    const projectRoot = currentPath.substring(0, currentPath.indexOf('/LC2024/') + 8);
    const getPath = (subPath) => projectRoot + subPath;

    const tests = [
        {
            num: '01',
            color: 'blue',
            folder: 'Test 1',
            prefix: 'T1',
            part3: ['32-34', '35-37', '38-40', '41-43', '44-46', '47-49', '50-52', '53-55', '56-58', '59-61', '62-64', '65-67', '68-70'],
            part4: ['71-73', '74-76', '77-79', '80-82', '83-85', '86-88', '89-91', '92-94', '95-97', '98-100']
        },
        {
            num: '02',
            color: 'purple',
            folder: 'Test 2',
            prefix: 'T2',
            part3: ['32-34', '35-37', '38-40', '41-43', '44-46', '47-49', '50-52', '53-55', '56-58', '59-61', '62-64', '65-67', '68-70'],
            part4: ['71-73', '74-76', '77-79', '80-82', '83-85', '86-88', '89-91', '92-94', '95-97', '98-100']
        },
        {
            num: '03',
            color: 'green',
            folder: 'Test 3',
            prefix: 'T3',
            part3: ['32-34', '35-37', '38-40', '41-43', '44-46', '47-49', '50-52', '53-55', '56-58', '59-61', '62-64', '65-67', '68-70'],
            part4: ['71-73', '74-76', '77-79', '80-82', '83-85', '86-88', '89-91', '92-94', '95-97', '98-100']
        },
        {
            num: '04',
            color: 'orange',
            folder: 'Test 4',
            prefix: 'T4',
            part3: ['32-34', '35-37', '38-40', '41-43', '44-46', '47-49', '50-52', '53-55', '56-58', '59-61', '62-64', '65-67', '68-70'],
            part4: ['71-73', '74-76', '77-79', '80-82', '83-85', '86-88', '89-91', '92-94', '95-97', '98-100']
        }
    ];

    let sidebarHTML = `
    <div class="sidebar">
        <div class="mb-8 px-4">
            <a href="${getPath('index.html')}" class="flex items-center text-blue-800 font-bold text-xl hover:text-blue-600 transition">
                <i class="fas fa-graduation-cap mr-3 text-2xl text-blue-600"></i>
                <span>TOEIC Coach</span>
            </a>
        </div>
        
        <div class="space-y-6 pb-20">
    `;

    tests.forEach(test => {
        sidebarHTML += `
            <div class="tree-item">
                <div class="tree-header px-4">
                    <i class="fas fa-file-audio mr-2 text-${test.color}-500"></i> Test ${test.num}
                </div>
                <div class="ml-4 border-l border-slate-200 pl-2 mt-2 space-y-1">
                    <div class="text-[9px] font-black text-slate-400 px-3 py-1 uppercase tracking-widest">Part 3</div>
                    ${test.part3.map(q => {
                        const fileName = `LC-${test.prefix}-P3-Q${q}.html`;
                        const isActive = currentPath.includes(fileName);
                        return `<a href="${getPath(`${test.folder}/${fileName}`)}" class="tree-link ${isActive ? 'active' : ''}">Q${q}</a>`;
                    }).join('')}
                    
                    <div class="text-[9px] font-black text-slate-400 px-3 py-1 uppercase tracking-widest mt-2">Part 4</div>
                    ${test.part4.map(q => {
                        const fileName = `LC-${test.prefix}-P4-Q${q}.html`;
                        const isActive = currentPath.includes(fileName);
                        return `<a href="${getPath(`${test.folder}/${fileName}`)}" class="tree-link ${isActive ? 'active' : ''}">Q${q}</a>`;
                    }).join('')}
                </div>
            </div>
        `;
    });

    sidebarHTML += `
        </div>
    </div>
    `;

    // Wrap body content to support flex sidebar
    const originalContent = document.body.innerHTML;
    document.body.innerHTML = `
        <div class="app-wrapper">
            ${sidebarHTML}
            <main class="main-content">
                ${originalContent}
            </main>
        </div>
    `;
}
