const searchBar = document.querySelector(".search-bar-container");
const magnifier = document.querySelector(".magnifier");

magnifier.addEventListener("click", () => {
    searchBar.classList.toggle("active");
});


let currentIndex = 0;
const slides = document.querySelector('.slides');
const totalSlides = document.querySelectorAll('.slide').length;

function showSlide(index) {
    if (index >= totalSlides) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = totalSlides - 1;
    } else {
        currentIndex = index;
    }
    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
}

function nextSlide() {
    showSlide(currentIndex + 1);
}

function prevSlide() {
    showSlide(currentIndex - 1);
}


let darkmode = localStorage.getItem('darkmode')
const themeSwitch = document.getElementById('theme-switch')

const enableDarkmode = () => {
    document.body.classList.add('darkmode')
    localStorage.setItem('darkmode', 'active')
    const moon = document.getElementById("my-moon");
    moon.style.display = "none";
}

const disableDarkmode = () => {
    document.body.classList.remove('darkmode')
    localStorage.setItem('darkmode', null);
    const moon = document.getElementById("my-moon");
    moon.style.display = "block";

}

if (darkmode === "active") enableDarkmode()

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode')
    darkmode !== "active" ? enableDarkmode() : disableDarkmode()
})


//api

const fetchTrends = async (apiUrl) => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        if (data.trend_movies && data.trend_movies.length > 0) {
            addDataToHTMLTrends(data.trend_movies, "movies");
        } else {
            console.log("No trend movies found.");
        }

        if (data.trend_series && data.trend_series.length > 0) {
            addDataToHTMLTrends(data.trend_series, "series");
        } else {
            console.log("No trend series found.");
        }

        initializeSwiper();

    } catch (error) {
        console.error("Error fetching trends:", error);
    }
};

const addDataToHTMLTrends = (items, kind) => {
    const swiperWrapper = document.getElementById("swiper");
    items.forEach((item) => {
        const slideItem = document.createElement("div");
        slideItem.classList.add("swiper-slide");

        // ایجاد لینک و محتوای اسلاید
        const link = document.createElement("a");
        link.href = kind === "movies"
            ? `download/imdex.html?id=${item.id}`
            : `downloadSerie/imdex.html?id=${item.id}`;
        link.classList.add("first-slide", "p-0");

        // ایجاد تصویر
        const image = document.createElement("img");
        image.src = `https://api.dramoir.com${item.image}`;
        image.alt = item.title;

        // ایجاد جزئیات اسلاید
        const sliderDetails = document.createElement("div");
        sliderDetails.classList.add("slider-details");

        const detail = document.createElement("div");
        detail.classList.add("detail");

        const title = document.createElement("h3");
        title.classList.add("h-sm");
        title.textContent = item.title;

        const button = document.createElement("button");
        button.classList.add("spanb-sm");
        button.style.marginTop = "90px";
        button.style.marginRight = "-60px";
        button.textContent = "مشاهده";

        // اضافه کردن عناصر به DOM
        detail.appendChild(title);
        detail.appendChild(button);
        sliderDetails.appendChild(detail);
        link.appendChild(image);
        link.appendChild(sliderDetails);
        slideItem.appendChild(link);
        swiperWrapper.appendChild(slideItem);
    });
};
const initializeSwiper = () => {
    var swiper = new Swiper(".mySwiper", {
        spaceBetween: 30,
        centeredSlides: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
    });
};

// فراخوانی تابع fetchTrends با آدرس API
fetchTrends("https://api.dramoir.com/main/home/?format=json");

const fetchTrendsDesktop = async (apiUrl) => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        if (data.trend_movies && data.trend_movies.length > 0) {
            addDataToHTMLTrendsDesctop(data.trend_movies, "movies");
        } else {
            console.log("No trend movies found.");
        }

        if (data.trend_series && data.trend_series.length > 0) {
            addDataToHTMLTrendsDesctop(data.trend_series, "series");
        } else {
            console.log("No trend series found.");
        }


    } catch (error) {
        console.error("Error fetching trends:", error);
    }
};

const addDataToHTMLTrendsDesctop = (items, kind) => {
    const poster = document.getElementById("poster");
    items.forEach((item) => {
        const link = document.createElement("a");
        link.classList.add("trend-poster");
        link.href = kind === "movies"
            ? `download/imdex.html?id=${item.id}`
            : `downloadSerie/imdex.html?id=${item.id}`;
            const swiperSlide=document.createElement("swiper-slide");
            link.innerHTML=`
                           <div class="tt">
                            <img src="https://api.dramoir.com${item.image}"  class="trend-photo">
                           </div>
                            <div class="trend-items">                          
                                 <img src="assets/images/Group 106.a1e198e3.svg">
                            </div>
                            <span class="trend-title">
                              ${item.title}
                            </span>
            `
            swiperSlide.appendChild(link);
            poster.appendChild(swiperSlide);
    })


}


fetchTrendsDesktop("https://api.dramoir.com/main/home/?format=json");
//fetch navbar
const apiUrlsseries = [
    "https://api.dramoir.com/main/home/best_korean_series/",
    "https://api.dramoir.com/main/home/best_chineas_series/",
    "https://api.dramoir.com/main/home/best_series/",
    "https://api.dramoir.com/main/home/choosen_korean_series/",

];


const apiUrlsmovies = [

    "https://api.dramoir.com/main/home/choosen_movies/",
    "https://api.dramoir.com/main/home/choosen_korean_movies/"
];


const fetchNavbar = async (apiUrlsseries) => {
    try {
        const fetchPromises = apiUrlsseries.map(async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.warn(`Failed to fetch ${url}: ${response.status}`);
                    return null;
                }
                return await response.json();
            } catch (error) {
                console.warn(`Error fetching ${url}:`, error);
                return null;
            }
        });

        const results = await Promise.all(fetchPromises);

        const dropdownContent = document.getElementById("dropdown-content1");
        if (!dropdownContent) {
            console.error("Element with id 'dropdown-content1' not found");
            return;
        }
        dropdownContent.innerHTML = "";

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsseries[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }


            const link = document.createElement("a");
            if (apiUrl.includes("best_korean_series")) {
                link.href = "more/index.html?type=best_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "در حال پخش کره ای";
            } else if (apiUrl.includes("best_chineas_series")) {
                link.href = "more/index.html?type=best_chineas_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های چینی";
            } else if (apiUrl.includes("best_series")) {
                link.href = "more/index.html?type=best_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های ژاپنی";
            } else if (apiUrl.includes("choosen_korean_series")) {
                link.href = "more/index.html?type=choosen_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = " بهترین سریال های کره ای ";
            }

            dropdownContent.appendChild(link);
        });
    } catch (error) {
        console.error("Error fetching series:", error);
    }
};

fetchNavbar(apiUrlsseries);

// fetch navbar2
const fetchNavbar2 = async (apiUrlsmovies) => {
    try {
        const fetchPromises = apiUrlsmovies.map(async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.warn(`Failed to fetch ${url}: ${response.status}`);
                    return null;
                }
                return await response.json();
            } catch (error) {
                console.warn(`Error fetching ${url}:`, error);
                return null;
            }
        });

        const results = await Promise.all(fetchPromises);

        const dropdownContent = document.getElementById("dropdown-content2");
        if (!dropdownContent) {
            console.error("Element with id 'dropdown-content2' not found");
            return;
        }
        dropdownContent.innerHTML = "";

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsmovies[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            const link = document.createElement("a");
            if (apiUrl.includes("choosen_movies")) {
                link.href = "more/index.html?type=choosen_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "فیلم های چینی";
            } else if (apiUrl.includes("choosen_korean_movies")) {
                link.href = "more/index.html?type=choosen_korean_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = " فیلم های کره ای";
            }
            dropdownContent.appendChild(link);
        });
    } catch (error) {
        console.error("Error fetching series:", error);
    }
};

fetchNavbar2(apiUrlsmovies);





// phone navbar


const fetchNavbarphone = async (apiUrlsseries) => {
    try {
        const fetchPromises = apiUrlsseries.map(async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.warn(`Failed to fetch ${url}: ${response.status}`);
                    return null;
                }
                return await response.json();
            } catch (error) {
                console.warn(`Error fetching ${url}:`, error);
                return null;
            }
        });

        const results = await Promise.all(fetchPromises);

        const dropdownContent = document.getElementById("submenu1");
        if (!dropdownContent) {
            console.error("Element with id 'submenu1' not found");
            return;
        }
        dropdownContent.innerHTML = ""; // Clear existing content

        // Create a <ul> element
        const ul = document.createElement("ul");
        ul.className = "submenu";

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsseries[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            // Create a new <li> element for each category
            const li = document.createElement("li");
            li.className = "submenu-item";

            // Create a new <a> element
            const link = document.createElement("a");
            if (apiUrl.includes("best_korean_series")) {
                link.href = "more/index.html?type=best_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "در حال پخش کره ای";
            } else if (apiUrl.includes("best_chineas_series")) {
                link.href = "more/index.html?type=best_chineas_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های چینی";
            } else if (apiUrl.includes("best_series")) {
                link.href = "more/index.html?type=best_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های ژاپنی";
            } else if (apiUrl.includes("choosen_korean_series")) {
                link.href = "more/index.html?type=choosen_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = " بهترین سریال های کره ای";
            }

            // Append the <a> to the <li>, and the <li> to the <ul>
            li.appendChild(link);
            ul.appendChild(li);
        });

        // Append the <ul> to the dropdown content
        dropdownContent.appendChild(ul);
    } catch (error) {
        console.error("Error fetching series:", error);
    }
};

fetchNavbarphone(apiUrlsseries);

const fetchNavbar3 = async (apiUrlsmovies) => {
    try {
        const fetchPromises = apiUrlsmovies.map(async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    console.warn(`Failed to fetch ${url}: ${response.status}`);
                    return null;
                }
                return await response.json();
            } catch (error) {
                console.warn(`Error fetching ${url}:`, error);
                return null;
            }
        });

        const results = await Promise.all(fetchPromises);

        const dropdownContent = document.getElementById("submenu2");
        if (!dropdownContent) {
            console.error("Element with id 'submenu2' not found");
            return;
        }
        dropdownContent.innerHTML = ""; // Clear existing content

        // Create a <ul> element
        const ul = document.createElement("ul");
        ul.className = "submenu";

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsmovies[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            // Create a new <li> element for each category
            const li = document.createElement("li");
            li.className = "submenu-item";

            // Create a new <a> element
            const link = document.createElement("a");
            if (apiUrl.includes("choosen_movies")) {
                link.href = "more/index.html?type=choosen_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "فیلم های چینی";
            } else if (apiUrl.includes("choosen_korean_movies")) {
                link.href = "more/index.html?type=choosen_korean_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "فیلم های کره ای";
            }

            // Append the <a> to the <li>, and the <li> to the <ul>
            li.appendChild(link);
            ul.appendChild(li);
        });

        // Append the <ul> to the dropdown content
        dropdownContent.appendChild(ul);
    } catch (error) {
        console.error("Error fetching series:", error);
    }
};

fetchNavbar3(apiUrlsmovies);



// more page
const fetchMore = async (apiUrls) => {
    try {
        const fetchPromises = apiUrls.map(url => fetch(url).then(response => {
            if (!response.ok) {
                console.warn(`Failed to fetch ${url}: ${response.status}`);
                return null; // بازگشت null برای URLهای ناموفق
            }
            return response.json();
        }));

        const results = await Promise.all(fetchPromises);

        results.forEach((data, index) => {
            if (!data) return; // اگر داده null باشد، از آن صرف‌نظر کنید

            const apiUrl = apiUrls[index];


            // بررسی وجود `results` و اینکه یک آرایه است
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            // ارسال `data.results` به تابع `addDataToHTMLMore`
            if (apiUrl.includes("best_korean_series")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec1"), "در حال پخش کره ای:", "best_korean_series");
            } else if (apiUrl.includes("best_chineas_series")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec2"), " سریال های چینی:", "best_chineas_series");
            } else if (apiUrl.includes("best_series")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec3"), "سریال های ژاپنی:", "best_series");
            } else if (apiUrl.includes("choosen_korean_series")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec4"), " بهترین سریال های کره ای:", "choosen_korean_series");
            } else if (apiUrl.includes("choosen_korean_movies")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec5"), "فیلم های کره ای:", "choosen_korean_movies");
            }
            else if (apiUrl.includes("choosen_movies")) {
                addDataToHTMLMore(data.results, document.getElementById("headerSec6"), "فیلم های چینی :", "choosen_movies");
            }
        });

    } catch (error) {
        console.error("Error fetching series:", error);
    }
};

const addDataToHTMLMore = (series, keenSlider, title, type) => {
    if (!keenSlider) return;

    keenSlider.innerHTML = "";


    if (!Array.isArray(series)) {
        console.error("Expected an array, but received:", series);
        return;
    }

    const slideItem = document.createElement("div");


    const seriesIds = series.map(item => item.id).join(",");

    slideItem.innerHTML = `
        <h4 class="spanb-sm dark-mc my-60" style="font-weight:bolder;">${title}</h4>
        <a href="more/index.html?type=${type}&series=${seriesIds}"><span class="all" style="font-weight: bolder;">مشاهده همه</span></a>
    `;

    keenSlider.appendChild(slideItem);
};


const apiUrls = [
    "https://api.dramoir.com/main/home/best_korean_series/",
    "https://api.dramoir.com/main/home/best_chineas_series/",
    "https://api.dramoir.com/main/home/best_series/",
    "https://api.dramoir.com/main/home/choosen_korean_series/",
    "https://api.dramoir.com/main/home/choosen_movies/",
    "https://api.dramoir.com/main/home/choosen_korean_movies/"
];

// اجرای تابع `fetchMore` با لیست URLها
fetchMore(apiUrls);


function toggleSubmenu(element) {
    let parentLi = element.parentElement; // پیدا کردن والد <li>
    let submenu = parentLi.querySelector(".submenu"); // زیرمنو داخل همان <li>
    if (submenu) {
        submenu.style.maxHeight = submenu.style.maxHeight === "0px" || submenu.style.maxHeight === ""
            ? submenu.scrollHeight + "px"
            : "0px";
    }
}



const fetchSeries = async (apiUrl) => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        // ارسال داده‌ها به تابع `addDataToHTML` بر اساس نوع سریال
        if (data.best_korean_series) {
            addDataToHTML(data.best_korean_series, document.getElementById("keen-slider"));

        }
        if (data.best_chineas_series) {
            addDataToHTML(data.best_chineas_series, document.getElementById("keen-slider2"));
        }
        if (data.best_series) {
            addDataToHTML(data.best_series, document.getElementById("keen-slider3"));
        }
        if (data.choosen_korean_series) {
            addDataToHTML(data.choosen_korean_series, document.getElementById("keen-slider4"));
        }
    } catch (error) {
        console.error("Error fetching series:", error);
    }
};



const addDataToHTML = (series, keenSlider) => {
    if (!keenSlider) return;

    keenSlider.innerHTML = "";

    series.forEach((serie) => {
        const slideItem = document.createElement("swiper-slide");
        slideItem.innerHTML = `
         <div style="padding:0 15px">
            <a class="row" href="downloadSerie/imdex.html?id=${serie.id}">
                <div class="Serie-container">
                    <img src="https://api.dramoir.com/${serie.image}" width="100%">
                    <div style="padding:10px 15px">
                        <div class="serie-id">
                            <div class="co" style="display:block;color:var(--dd-text);font-size:15px;">
                                <span class="sp">
                                    ${serie.title}
                                </span>
                            </div>
                        </div>
                        <div class="row" style="display:flex; justify-content:center; margin-top:10px">
                            <div class="col-5" style="background-color: var(--rank-color); border-radius: 10px;">
                                <div>
                                    <div class="row">
                                        <div class="col-6" style="color:black; font-size:12px; margin-top:4px; padding:2px 5px">
                                            ${serie.rate}
                                        </div>
                                        <div class="col-6" style="padding:0">
                                            <svg version="1.1" width="15px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" xml:space="preserve">
                                                <path class="outline" d="M12,4.2L14.5,9l0.2,0.5l0.5,0.1l5.5,0.8L16.8,14l-0.4,0.4l0.1,0.5l1,5.3l-5-2.5L12,17.5l-0.4,0.2l-5,2.5L7.5,15l0.1-0.5 L7.2,14l-4-3.7l5.5-0.8l0.5-0.1L9.5,9L12,4.2 M11.9,2L8.6,8.6L1,9.7l5.5,5.1L5.2,22l6.8-3.4l6.8,3.4l-1.3-7.2L23,9.6l-7.6-1L11.9,2 L11.9,2z" fill="gold" stroke="gold" />
                                                <polygon class="full" points="18.8,22 12,18.6 5.2,22 6.5,14.8 1,9.7 8.6,8.6 11.9,2 15.4,8.6 23,9.6 17.5,14.7" fill="gold" stroke="gold" />
                                                <polyline class="left-half" points="12,18.6 5.2,22 6.5,14.8 1,9.7 8.6,8.6 11.9,2" fill="gold" stroke="gold" />
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-7">
                                <span style="color:#e89631; font-size:15px; float: left; margin-top: 5px;">
                                    ${serie.release_year}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </a>
        </div>
        `;

    
        const titleElement = slideItem.querySelector('.serie-id');
        const movieTitle = slideItem.querySelector(".co");
        const movieTitlesp = slideItem.querySelector(".sp");
        if (serie.title.length > 9) {
            titleElement.classList.add('text-container');
            movieTitle.classList.add("serie-title");
            movieTitlesp.classList.add("horizontal-scrolling-items__item");
        }

        keenSlider.appendChild(slideItem);
    });
};

fetchSeries("https://api.dramoir.com/main/home/?format=json");



//search
document.querySelector('.search-btn').addEventListener('click', async function () {
    const inputElement = document.querySelector('input[data-search]');
    const searchValue = inputElement.value.trim().toLowerCase();
    const searchMessage = document.getElementById('search-message');

    if (!searchValue) {
        searchMessage.textContent = 'لطفاً عنوانی را وارد کنید!';
        searchMessage.style.color = 'red';
        return;
    }

    try {
        const response = await fetch(`https://api.dramoir.com/main/search/?q=${encodeURIComponent(searchValue)}`);
        if (!response.ok) {
            throw new Error('خطا در دریافت داده‌ها');
        }
        const data = await response.json();

        // بررسی ساختار داده‌ها
        if (!data.movies || !data.series) {
            throw new Error('فرمت داده‌ها نادرست است!');
        }


        const foundMovie = data.movies.find(movie => movie.title.toLowerCase().includes(searchValue));

        const foundSerie = data.series.find(serie => serie.title.toLowerCase().includes(searchValue));

        if (foundMovie) {

            window.location.href = `download/imdex.html?id=${foundMovie.id}`;
            inputElement.value = '';
        } else if (foundSerie) {

            window.location.href = `downloadSerie/imdex.html?id=${foundSerie.id}`;
            inputElement.value = '';
        } else {

            searchMessage.textContent = 'فیلم یا سریالی با این عنوان پیدا نشد!';
            searchMessage.style.color = 'red';
            inputElement.value = '';
        }
    } catch (error) {
        console.error('خطا در دریافت داده‌ها:', error);
        searchMessage.textContent = 'مشکلی در دریافت اطلاعات پیش آمده!';
        searchMessage.style.color = 'red';
    }
});

document.querySelector('.delete-btn').addEventListener('click', function () {
    document.querySelector('input[data-search]').value = '';
});


// top search
document.addEventListener("DOMContentLoaded", function () {
    const searchIcon = document.querySelector(".magnifier");
    const searchInput = document.querySelector(".input");

    async function fetchProducts(query) {
        try {
            const response = await fetch(`https://api.dramoir.com/main/search/?q=${encodeURIComponent(query)}`);
            return await response.json();
        } catch (error) {
            console.error("Error fetching products:", error);
            return [];
        }
    }

    async function handleSearch() {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) return;

        const products = await fetchProducts(query);
        if (!products || typeof products !== "object") {
            console.error("فرمت داده‌های دریافتی نادرست است!");
            return;
        }

        const allMovies = products.movies || [];
        const allSeries = products.series || [];

        const foundMovie = allMovies.find(movie => movie.title.toLowerCase().includes(query));
        const foundSerie = allSeries.find(serie => serie.title.toLowerCase().includes(query));

        if (foundMovie) {
            // اگر فیلم پیدا شد، به صفحه فیلم‌ها ریدایرکت کنید
            const movieRedirectPath = `download/imdex.html?id=${foundMovie.id}`;
            window.location.href = movieRedirectPath;
        } else if (foundSerie) {
            // اگر سریال پیدا شد، به صفحه سریال‌ها ریدایرکت کنید
            const serieRedirectPath = `downloadSerie/imdex.html?id=${foundSerie.id}`;
            window.location.href = serieRedirectPath;
        } else {
            // اگر هیچ محصولی پیدا نشد، پیام مناسب نمایش دهید
            const searchMessage1 = document.getElementById('search-message1');
            if (searchMessage1) {
                searchMessage1.textContent = 'فیلم یا سریالی با این عنوان پیدا نشد!';
                setTimeout(() => {
                    searchMessage1.textContent = "";
                }, 2000);
            }
        }

        searchInput.value = ""; // پاک کردن مقدار ورودی پس از جستجو
    }

    searchIcon.addEventListener("click", handleSearch);
});

const fetchMovies = async (apiUrl) => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();


        // ارسال داده‌ها به تابع `addDataToHTML` بر اساس نوع سریال
        if (data.choosen_korean_movie) {
            addDataToHTMLMovie(data.choosen_korean_movie, document.getElementById("slider1"));
        }
        if (data.choosen_movie) {
            addDataToHTMLMovie(data.choosen_movie, document.getElementById("slider2"));
        }

    } catch (error) {
        console.error("Error fetching series:", error);
    }
};


const addDataToHTMLMovie = (series, keenSlider) => {
    if (!keenSlider) return;

    keenSlider.innerHTML = "";

    let container = document.createElement("div");
    container.classList.add("container-fluid");

    for (let i = 0; i < Math.min(12, series.length); i += 6) {
        const row = document.createElement("div");
        row.classList.add("row");

        if (i >= 6) {
            row.style.marginTop = "30px";
        }

        for (let j = i; j < i + 6 && j < Math.min(12, series.length); j++) {
            const serie = series[j];
            const col = document.createElement("div");
            col.classList.add("col-md-2", "movie-hover");

            col.innerHTML = `
 <div class="col-md-3 movie-hover" style="    display: flex;
    align-items: center;
    justify-content: center;">
        <a href="download/imdex.html?id=${serie.id}"  style="display: flex;justify-content: center;" >
            <img src="https://api.dramoir.com/${serie.image}">
            <div class="shiny-circle">
                <div class="sharp-triangle"></div>
            </div>
            <div class="serie-id1" style="position:absolute; background-color:rgb(255,0,0,.5);border-radius:10px; ;top:65%; width:150%; display:flex;justify-content: center;" >
            <div class="co1" >
                <div style="color:white; font-size:15px" class="sp1">
                    ${serie.title}
                </div>
            </div>
            </div>
        </a>
    </div>
            `;
            const titleElement = col.querySelector('.serie-id1');
            const movieTitle = col.querySelector(".co1");
            const movieTitlesp = col.querySelector(".sp1");
            if (serie.title.length >7) {
                titleElement.classList.add('text-container1');
                movieTitle.classList.add("serie-title1");
                movieTitlesp.classList.add("horizontal-scrolling-items__item1");
            }
            row.appendChild(col);
           
        
        }
        container.appendChild(row);
    }
    keenSlider.appendChild(container);
};


fetchMovies("https://api.dramoir.com/main/home/?format=json");


const fetchPhone = async (apiUrl) => {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();


        if (data.choosen_movie) {
            addDataToHTMLPhone(data.choosen_movie, document.getElementById("keen-slider6"));
        }

        if (data.choosen_korean_movie) {
            addDataToHTMLPhone(data.choosen_korean_movie, document.getElementById("keen-slider5"));
        }

    } catch (error) {
        console.error("Error fetching series:", error);
    }
};


const addDataToHTMLPhone = (series, keenSlider) => {
    if (!keenSlider) return;

    keenSlider.innerHTML = "";

    for (let i = 0; i < series.length / 2; i++) {
        const topSerie = series[i];
        const bottomSerie = series[i + Math.floor(series.length / 2)];

        const slideItem = document.createElement("swiper-slide");


        slideItem.innerHTML = `
            <div class="col-md-3 movie-hover" id="first-half" style="display: flex; align-items: center; justify-content: center;">
                <a href="download/imdex.html?id=${topSerie.id}" style="display: flex; justify-content: center;">
                    <img src="https://api.dramoir.com/${topSerie.image}">
                    <div class="shiny-circle">
                        <div class="sharp-triangle"></div>
                    </div>
                     <div class="serie-id2" style="position:absolute; background-color:rgb(255,0,0,.5);border-radius:10px; ;top:65%; width:60%; display:flex;justify-content: center;" >
            <div class="co2" >
                <div style="color:white; font-size:15px" class="sp2">
                    ${topSerie.title}
                </div>
            </div>
            </div>
                </a>
            </div>
            <div class="col-md-3 movie-hover" id="second-half" style="display: flex; align-items: center; justify-content: center;">
                <a href="download/imdex.html?id=${bottomSerie.id}" style="display: flex; justify-content: center;">
                    <img src="https://api.dramoir.com/${bottomSerie.image}">
                    <div class="shiny-circle">
                        <div class="sharp-triangle"></div>
                    </div>
                     <div class="serie-id3" style="position:absolute; background-color:rgb(255,0,0,.5);border-radius:10px; ;top:65%; width:60%; display:flex;justify-content: center;" >
            <div class="co3" >
                <div style="color:white; font-size:15px" class="sp3">
                    ${bottomSerie.title}
                </div>
            </div>
            </div>
                </a>
            </div>
        `;
        const titleElement = slideItem.querySelector('.serie-id2');
        const movieTitle = slideItem.querySelector(".co2");
        const movieTitlesp = slideItem.querySelector(".sp2");
        if (topSerie.title.length >7) {
            titleElement.classList.add('text-container1');
            movieTitle.classList.add("serie-title1");
            movieTitlesp.classList.add("horizontal-scrolling-items__item1");
        }
        const titleElement1 = slideItem.querySelector('.serie-id3');
        const movieTitle1 = slideItem.querySelector(".co3");
        const movieTitlesp1 = slideItem.querySelector(".sp3");
        if (bottomSerie.title.length >7) {
            titleElement1.classList.add('text-container1');
            movieTitle1.classList.add("serie-title1");
            movieTitlesp1.classList.add("horizontal-scrolling-items__item1");
        }
        keenSlider.appendChild(slideItem);
    }
};

// اجرای تابع `fetchPhone`
fetchPhone("https://api.dramoir.com/main/home/?format=json");



