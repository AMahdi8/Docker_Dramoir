const searchBar = document.querySelector(".search-bar-container");  
const magnifier = document.querySelector(".magnifier"); 

magnifier.addEventListener("click", ()=>{ 
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
    const moon=document.getElementById("my-moon");
    moon.style.display="none";
}

const disableDarkmode = () => {
    document.body.classList.remove('darkmode')
    localStorage.setItem('darkmode', null);
    const moon=document.getElementById("my-moon");
    moon.style.display="block";
   
}

if (darkmode === "active") enableDarkmode()

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode')
    darkmode !== "active" ? enableDarkmode() : disableDarkmode()
})


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
            const movieRedirectPath = `../download/imdex.html?id=${foundMovie.id}`;
            window.location.href = movieRedirectPath;
        } else if (foundSerie) {
            // اگر سریال پیدا شد، به صفحه سریال‌ها ریدایرکت کنید
            const serieRedirectPath = `../downloadSerie/imdex.html?id=${foundSerie.id}`;
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
//api

const seriesContainer = document.getElementById("seriesContainer");
const pageTitle = document.getElementById("pageTitle");

// دریافت نوع از URL
const urlParams = new URLSearchParams(window.location.search);
const type = urlParams.get('type');

// تعیین لینک بر اساس نوع
let apiUrl = "";
switch (type) {
    case "best_korean_series":
        apiUrl = "https://api.dramoir.com/main/home/best_korean_series/";
        pageTitle.innerText ="در حال پخش کره ای:";
        break;
    case "best_chineas_series":
        apiUrl = "https://api.dramoir.com/main/home/best_chineas_series/";
        pageTitle.innerText = "سریال های چینی:";
        break;
    case "best_series":
        apiUrl = "https://api.dramoir.com/main/home/best_series/";
        pageTitle.innerText = " سریال های ژاپنی:";
        break;
    case "choosen_korean_series":
        apiUrl = "https://api.dramoir.com/main/home/choosen_korean_series/";
        pageTitle.innerText = " بهترین سریال های کره ای:";
        break;
    case "choosen_movies":
        apiUrl = "https://api.dramoir.com/main/home/choosen_movies/";
        pageTitle.innerText = " فیلم های چینی:";
        break;
    case "choosen_korean_movies":
        apiUrl = "https://api.dramoir.com/main/home/choosen_korean_movies/";
        pageTitle.innerText = "فیلم‌های کره‌ای:";
        break;
    default:
        apiUrl = "https://api.dramoir.com/main/home/best_korean_series/";
        pageTitle.innerText = "در حال پخش کره ای:";
        break;
}


// دریافت داده‌ها از API
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // استفاده از data.results به جای data
        data.results.forEach(item => {
            const seriesItem = document.createElement("div");
            seriesItem.classList="col-md-2 col-4 movie-hover";
            seriesItem.style.marginBottom="30px";
           
            if (apiUrl.includes("series")){
                seriesItem.innerHTML = `
                <a href="../downloadSerie/imdex.html?id=${item.id}" style="position:relative">
                    <img src="https://api.dramoir.com/${item.image}" alt="${item.title}">
                   
                </a>
                                  <div class="shiny-circle">
        <div class="sharp-triangle"></div>
    </div>
                <div style="position:absolute;top:100%; text-align: center; font-size:13px; line-height:2" class="dd-text">${item.title}</div>
            `;
            } else {
                seriesItem.innerHTML = `
                <a href="../download/imdex.html?id=${item.id}">
                    <img src="https://api.dramoir.com/${item.image}"  alt="${item.title}">
                   
                </a>
                                              <div class="shiny-circle">
        <div class="sharp-triangle"></div>
    </div>
                <div style="position:absolute;top:104%; text-align: center; font-size:13px" class="dd-text" > ${item.title}</div>
            `;
            }
          
            seriesContainer.appendChild(seriesItem);
        });
    })
    .catch(error => console.error('Error fetching data:', error));



function toggleSubmenu(element) {
    let parentLi = element.parentElement; // پیدا کردن والد <li>
    let submenu = parentLi.querySelector(".submenu"); // زیرمنو داخل همان <li>
    if (submenu) {
        submenu.style.maxHeight = submenu.style.maxHeight === "0px" || submenu.style.maxHeight === "" 
            ? submenu.scrollHeight + "px" 
            : "0px";
    }
}


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
        dropdownContent.innerHTML = ""; // Clear existing content

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsseries[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            // Create a new link for each category
            const link = document.createElement("a");
            if (apiUrl.includes("best_korean_series")) {
                link.href = "../more/index.html?type=best_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "در حال پخش کره ای";
            } else if (apiUrl.includes("best_chineas_series")) {
                link.href = "../more/index.html?type=best_chineas_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های چینی";
            } else if (apiUrl.includes("best_series")) {
                link.href = "../more/index.html?type=best_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های ژاپنی";
            } else if (apiUrl.includes("choosen_korean_series")) {
                link.href = "../more/index.html?type=choosen_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "بهترین سریال های کره ای";
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
        dropdownContent.innerHTML = ""; // Clear existing content

        results.forEach((data, index) => {
            if (!data) return;
            const apiUrl = apiUrlsmovies[index];
            if (!data.results || !Array.isArray(data.results)) {
                console.warn(`Expected 'results' array in data from ${apiUrl}, but received:`, data);
                return;
            }

            // Create a new link for each category
            const link = document.createElement("a");
            if (apiUrl.includes("choosen_movies")) {
                link.href = "../more/index.html?type=choosen_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "فیلم های چینی";
            } else if (apiUrl.includes("choosen_korean_movies")) {
                link.href = "../more/index.html?type=choosen_korean_movies&series=" + data.results.map(item => item.id).join(",");
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
                link.href = "../more/index.html?type=best_korean_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "در حال پخش کره ای";
            } else if (apiUrl.includes("best_chineas_series")) {
                link.href = "../more/index.html?type=best_chineas_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های چینی";
            } else if (apiUrl.includes("best_series")) {
                link.href = "../more/index.html?type=best_series&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "سریال های ژاپنی";
            } else if (apiUrl.includes("choosen_korean_series")) {
                link.href = "../more/index.html?type=choosen_korean_series&series=" + data.results.map(item => item.id).join(",");
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
                link.href = "../more/index.html?type=choosen_movies&series=" + data.results.map(item => item.id).join(",");
                link.textContent = "فیلم های چینی";
            } else if (apiUrl.includes("choosen_korean_movies")) {
                link.href = "../more/index.html?type=choosen_korean_movies&series=" + data.results.map(item => item.id).join(",");
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