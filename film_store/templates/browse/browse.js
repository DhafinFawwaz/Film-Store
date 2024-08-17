const resultDiv = document.getElementById('result');

async function refresh() {
    try {
        let href = window.location.href;
        if (href.endsWith('/')) href = href.slice(0, -1);
        const url = href + '/polling';
        const res = await fetch(url); // might wait a long time
        const data = await res.json();
        updateFilmList(data.films);
    } catch (e) {}

    await wait(5000);
    refresh();
}

function updateFilmList(filmData) {
    console.log(filmData);
}

async function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

refresh(); 