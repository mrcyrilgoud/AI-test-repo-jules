chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'pomodoroTimer') {
        chrome.storage.local.get(['settings', 'timerState'], (result) => {
            let { settings, timerState } = result;

            if (!timerState.isRunning) {
                return;
            }

            timerState.timeRemaining--;

            if (timerState.timeRemaining < 0) {
                switch (timerState.timerType) {
                    case 'pomodoro':
                        timerState.sessionCount++;
                        if (timerState.sessionCount % settings.sessionsBeforeLongBreak === 0) {
                            timerState.timerType = 'longBreak';
                            timerState.timeRemaining = settings.longBreakDuration * 60;
                            showNotification('Time for a long break!');
                        } else {
                            timerState.timerType = 'shortBreak';
                            timerState.timeRemaining = settings.shortBreakDuration * 60;
                            showNotification('Time for a short break!');
                        }
                        break;
                    case 'shortBreak':
                    case 'longBreak':
                        timerState.timerType = 'pomodoro';
                        timerState.timeRemaining = settings.pomodoroDuration * 60;
                        showNotification('Time to get back to work!');
                        break;
                }
            }
            chrome.storage.local.set({ timerState });
        });
    }
});

function showNotification(message) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Pomodoro Timer',
        message: message,
        priority: 2
    });
}
