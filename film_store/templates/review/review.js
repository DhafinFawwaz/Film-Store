(() => {

const origin = window.location.origin;
const urlParts = window.location.href.split('/');
const id = urlParts[urlParts.length - 2];
let url = origin + "/polling/details/" + id + "/review";

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
            if (json.data) {
                updateReview(json.data);
                continue;
            }
        } catch (e) {
            // console.error(e);
        }
        await wait(5000);
    }
}

const allReview = document.getElementById('all-review');

function updateReview(data) {
    const reviews = data.all_review;
    const allReviewDivStr = reviews.reduce((res, review) => {
        let star = review.rating !== null ? review.rating : 0;
        
        let starSvg = '';
        // let fractionalPercentage = 0;
    
        for (let i = 0; i < 5; i++) {
            starSvg += `<svg class="w-4 h-4 duration-150 ease-out-back text-night-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>`;
        }
    
        let ratedSvg = '';
        for (let i = 0; i < star; i++) {
            ratedSvg += `<svg class="w-4 h-4 duration-150 ease-out-back text-yellow-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
                        <path d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
                    </svg>`;
        }
    
        let ratingDisplay = star === 0 ? 
            `<p class="text-sm ml-26 mt-0 -translate-y-0.5 font-medium text-night-100">Unrated</p>` : 
            `<p class="text-sm ml-26 mt-0 -translate-y-0.5 font-medium text-night-100">${star} out of 5</p>`;
    
        res += `
            <div class="px-4 py-3 text-md bg-night-600 rounded-xl shadow-rim-sm drop-shadow-lg mt-4">
            <div class="grid grid-cols-2">
                <div class="font-bold tracking-wide text-lg -translate-y-0.5">${review.user.first_name} ${review.user.last_name}</div>
                <div class="font-thin text-xs mb-1 text-end">${review.updated_at}</div>
            </div>
            ${review.rating !== null ? `
                <div class="relative flex flex-wrap gap-1">
                    <div class="absolute flex items-center gap-1 mr-1">
                        ${starSvg}
                    </div>
                    <div class="absolute flex items-center gap-1">
                        ${ratedSvg}
                    </div>
                    ${ratingDisplay}
                </div>
                <div class="h-1"></div>
            ` : ''}
            ${review.review}
        </div>`;
        
        return res;
    }, '');

    allReview.innerHTML = allReviewDivStr;
    
}

async function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

refresh(); 


})()
    