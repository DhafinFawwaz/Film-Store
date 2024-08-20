(() => {

const resultDiv = document.getElementById('results');
const origin = window.location.origin;
let path = "";
const pathName = window.location.pathname;

if (pathName.includes('bought')) path = '/polling/bought';
else if (pathName.includes('wishlist')) path = '/polling/wishlist';
else path = '/polling/film';

let url = origin + path;

const urlParams = new URLSearchParams(window.location.search);
const page = urlParams.get('page');
const search = urlParams.get('search');
if (page) url += `?page=${ page }`;
else url += '?page=1';
if (search) url += `&search=${ search }`;


async function refresh() {
    while(true) {
        try {
            const res = await fetch(url); // might wait a long time
            const json = await res.json();
            if (json.data.films) {
                updateFilmList(json.data.films);
                continue;
            }
        } catch (e) {
            // console.error(e);
        }
        await wait(1000);
    }
}

function updateFilmList(films) {
    resultDiv.innerHTML = '';
    films.forEach(film => {
        const card = buildCard(film);
        resultDiv.appendChild(card);
    });
}

async function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

refresh(); 

function formatPrice(price) {
    // if no decimal, add .00
    const str = price.toString();
    if (str.indexOf('.') === -1) return price + '.0';
    return price;
}

function buildCard(film) {
    // This is very unsafe, but we trust the data from the server
    const str = `<a href="/details/${ film.id }" class="max-w-56 rounded-2xl hover:scale-105 ease-out-back-expo duration-150 focus:ring-4 focus:scale-107 focus:ring-indigo-600 drop-shadow-md relative h-80   xxs:h-88 md:h-96 focus:z-10 hover:z-10">
        <div class="px-3 h-full justify-end flex flex-col pt-2 pb-2 sm:px-4 sm:pt-3 sm:pb-4 text-white absolute z-10 bg-gradient-to-t from-black from-20% to-80% rounded-2xl w-full line-clamp-2">
            <div class="flex gap-x-2 flex-wrap">
                <div class="text-md sm:text-xl font-bold tracking-wider leading-6 line-clamp-2">${ film.title }</div>
                <div class="text-md sm:text-xl leading-6 line-clamp-2">(${ film.release_year })</div>
            </div>
            <div class="font-light text-xs text-gray-300 line-clamp-1">Directed by ${ film.director }</div>
            
            
            <div class="flex gap-2 mt-1 sm:mt-2 flex-wrap">
                ${
                    film.genre.reduce((res, genre) => res + `<div class="text-xs rounded-lg px-1 py-0.5 sm:px-2 text-night-100 bg-night-800 font-semibold shadow-rim-sm drop-shadow-sm">${ genre }</div>`, '')
                }
            </div>

            <div class="flex flex-row justify-between font-bold text-sm mt-2">
                <div class="font-light text-xs text-gray-300 line-clamp-1">${ film.duration }</div>
                <div class="font-semibold text-xs line-clamp-1">🪙 ${ formatPrice(film.price) }</div>
            </div>
        </div>
        <div class="w-full overflow-hidden hover:z-10 focus:z-10">
            <img alt="film-thumbnail" src="${ film.cover_image_url }" class="object-cover object-center rounded-2xl w-full h-80 xxs:h-88 md:h-96"></img>
        </div>
    </a>`

    const div = document.createElement('div');
    div.innerHTML = str;
    return div.firstChild;
}

})()
