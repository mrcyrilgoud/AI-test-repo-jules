document.addEventListener('DOMContentLoaded', () => {
    const timerDisplay = document.querySelector('.timer-display');
    const sessionCountDisplay = document.querySelector('.session-count');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const resetBtn = document.getElementById('reset-btn');
    const themeToggle = document.getElementById('theme-toggle');

    let settings = {};
    let timerState = {};
    let timerInterval = null;

    const defaultSettings = {
        pomodoroDuration: 25,
        shortBreakDuration: 5,
        longBreakDuration: 15,
        sessionsBeforeLongBreak: 4,
    };

    function updateTimerDisplay() {
        if (timerState.timeRemaining) {
            const minutes = Math.floor(timerState.timeRemaining / 60);
            const seconds = timerState.timeRemaining % 60;
            timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    function updateSessionCountDisplay() {
        if (settings.sessionsBeforeLongBreak) {
            sessionCountDisplay.textContent = `${timerState.sessionCount}/${settings.sessionsBeforeLongBreak}`;
        }
    }

    function applyTheme(isDarkMode) {
        document.body.classList.toggle('dark-mode', isDarkMode);
    }

    function updatePopup() {
        chrome.storage.local.get(['settings', 'timerState', 'isDarkMode'], (result) => {
            settings = { ...defaultSettings, ...result.settings };
            timerState = result.timerState || {
                isRunning: false,
                timerType: 'pomodoro',
                timeRemaining: settings.pomodoroDuration * 60,
                sessionCount: 0,
            };
            applyTheme(result.isDarkMode);
            updateTimerDisplay();
            updateSessionCountDisplay();
        });
    }

    // Update the popup every second
    timerInterval = setInterval(updatePopup, 1000);

    themeToggle.addEventListener('click', () => {
        const isDarkMode = !document.body.classList.contains('dark-mode');
        chrome.storage.local.set({ isDarkMode });
        applyTheme(isDarkMode);
    });

    startBtn.addEventListener('click', () => {
        if (!timerState.isRunning) {
            timerState.isRunning = true;
            chrome.alarms.create('pomodoroTimer', { periodInMinutes: 1 / 60 });
            chrome.storage.local.set({ timerState });
        }
    });

    stopBtn.addEventListener('click', () => {
        if (timerState.isRunning) {
            timerState.isRunning = false;
            chrome.alarms.clear('pomodoroTimer');
            chrome.storage.local.set({ timerState });
        }
    });

    resetBtn.addEventListener('click', () => {
        timerState.isRunning = false;
        timerState.timerType = 'pomodoro';
        timerState.timeRemaining = settings.pomodoroDuration * 60;
        timerState.sessionCount = 0;
        chrome.alarms.clear('pomodoroTimer');
        chrome.storage.local.set({ timerState }, updatePopup);
    });

    // Initial popup update
    updatePopup();
});
