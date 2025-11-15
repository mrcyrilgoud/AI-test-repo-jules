document.addEventListener('DOMContentLoaded', () => {
    const settingsForm = document.getElementById('settings-form');
    const pomodoroDurationInput = document.getElementById('pomodoro-duration');
    const shortBreakDurationInput = document.getElementById('short-break-duration');
    const longBreakDurationInput = document.getElementById('long-break-duration');
    const sessionsBeforeLongBreakInput = document.getElementById('sessions-before-long-break');

    const defaultSettings = {
        pomodoroDuration: 25,
        shortBreakDuration: 5,
        longBreakDuration: 15,
        sessionsBeforeLongBreak: 4,
    };

    function applyTheme(isDarkMode) {
        document.body.classList.toggle('dark-mode', isDarkMode);
    }

    // Load settings and theme, then populate the form
    chrome.storage.local.get(['settings', 'isDarkMode'], (result) => {
        const settings = { ...defaultSettings, ...result.settings };
        pomodoroDurationInput.value = settings.pomodoroDuration;
        shortBreakDurationInput.value = settings.shortBreakDuration;
        longBreakDurationInput.value = settings.longBreakDuration;
        sessionsBeforeLongBreakInput.value = settings.sessionsBeforeLongBreak;
        applyTheme(result.isDarkMode);
    });

    // Save settings when the form is submitted
    settingsForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const newSettings = {
            pomodoroDuration: parseInt(pomodoroDurationInput.value, 10),
            shortBreakDuration: parseInt(shortBreakDurationInput.value, 10),
            longBreakDuration: parseInt(longBreakDurationInput.value, 10),
            sessionsBeforeLongBreak: parseInt(sessionsBeforeLongBreakInput.value, 10),
        };
        chrome.storage.local.set({ settings: newSettings }, () => {
            // Optional: Provide feedback to the user
            const saveButton = settingsForm.querySelector('button');
            saveButton.textContent = 'Saved!';
            setTimeout(() => {
                saveButton.textContent = 'Save';
            }, 1000);
        });
    });
});
