window.addEventListener('load', () => {
    registerSW();
});

// Registro do Service Worker
async function registerSW() {
    if ('serviceWorker' in navigator) {
        try {
            await navigator
                .serviceWorker
                .register('serviceworker.js');
        }
        catch (e) {
            console.log('SW registration failed');
        }
    }
}