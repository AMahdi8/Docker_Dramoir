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


document.getElementById('download-button').addEventListener('click', function () {
    const myDiv = document.getElementById('parts');
    if (myDiv.style.display === 'none') {
        myDiv.style.display = 'block';
    } else {
        myDiv.style.display = 'none';
    }
});

document.getElementById("quality1").addEventListener("click", function () {
    const quality1 = document.getElementById("open-quality1");
    if (quality1.style.display === "none") {
        quality1.style.display = "block";
    }
    else {
        quality1.style.display = "none"
    }
})

document.getElementById("quality2").addEventListener("click", function () {
    const quality2 = document.getElementById("open-quality2");
    if (quality2.style.display === "none") {
        quality2.style.display = "block";
    }
    else {
        quality2.style.display = "none"
    }
})

document.getElementById("quality3").addEventListener("click", function () {
    const quality3 = document.getElementById("open-quality3");
    if (quality3.style.display === "none") {
        quality3.style.display = "block";
    }
    else {
        quality3.style.display = "none"
    }
})

document.getElementById("quality4").addEventListener("click", function () {
    const quality4 = document.getElementById("open-quality4");
    if (quality4.style.display === "none") {
        quality4.style.display = "block";
    }
    else {
        quality4.style.display = "none"
    }
})

document.getElementById("quality5").addEventListener("click", function () {
    const quality5 = document.getElementById("open-quality5");
    if (quality5.style.display === "none") {
        quality5.style.display = "block";
    }
    else {
        quality5.style.display = "none"
    }
})

document.getElementById("quality6").addEventListener("click", function () {
    const quality6 = document.getElementById("open-quality6");
    if (quality6.style.display === "none") {
        quality6.style.display = "block";
    }
    else {
        quality6.style.display = "none"
    }
})

document.getElementById("quality7").addEventListener("click", function () {
    const quality7 = document.getElementById("open-quality7");
    if (quality7.style.display === "none") {
        quality7.style.display = "block";
    }
    else {
        quality7.style.display = "none"
    }
})

document.getElementById("quality8").addEventListener("click", function () {
    const quality8 = document.getElementById("open-quality8");
    if (quality8.style.display === "none") {
        quality8.style.display = "block";
    }
    else {
        quality8.style.display = "none"
    }
})

document.getElementById("quality9").addEventListener("click", function () {
    const quality9 = document.getElementById("open-quality9");
    if (quality9.style.display === "none") {
        quality9.style.display = "block";
    }
    else {
        quality9.style.display = "none"
    }
})

document.getElementById("quality10").addEventListener("click", function () {
    const quality10 = document.getElementById("open-quality10");
    if (quality10.style.display === "none") {
        quality10.style.display = "block";
    }
    else {
        quality10.style.display = "none"
    }
})




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


let movieVideo = document.getElementById("myVideo");
let movieDescription = document.getElementById("movie-description");
let movieGenres = document.getElementById("genres");
let movieRelease = document.getElementById("release_year");
let movieRank = document.getElementById("rank");

const fetchSeries = async () => {
    try {
        const response = await fetch(apiUrlGeneratorSeries());
        const data = await response.json();
       
        addDataToHTMLSeries(data, document.querySelector(".part-of-movie"));
    } catch (error) {
        console.error("Error fetching series", error);
    }
};

function apiUrlGeneratorSeries() {
    let idParam = new URLSearchParams(window.location.search).get("id");
    return `https://api.dramoir.com/main/series/${idParam}`;
}

function addDataToHTMLSeries(data, parts) {
    if (!data || !data.seasons || !Array.isArray(data.seasons)) {
        console.error("Invalid data structure: seasons is missing or not an array");
        return;
    }


const trailerLink = data.seasons[0].trailer_link; 
movieVideo.innerHTML=`<source type="video/mp4" src="${trailerLink}">`;
    movieDescription.innerHTML = data.description || "توضیحات موجود نیست";
    movieGenres.textContent = data.genres.map(genre => genre.name).join(" ، ") || "ژانر نامشخص";
    movieRelease.textContent = data.release_year || "سال انتشار نامشخص";
    movieRank.textContent = data.rate || "امتیاز نامشخص";

    parts.innerHTML = ""; 

    const seasonList = document.createElement("ul");

    data.seasons.forEach((season, index) => {
       
        const seasonItem = document.createElement("li");
        seasonItem.classList.add("col-12", "quality", "set-center"); 
        seasonItem.innerHTML = ` 
            <i class="fa-solid fa-folder-open dark-purple"></i> فصل ${season.number}
        `;
        seasonItem.style.cursor = "pointer";
        seasonItem.style.marginBottom = "10px"; 
    

        const episodeList = document.createElement("div");
        episodeList.style.display = "none";

        seasonItem.addEventListener("click", (event) => {
            event.stopPropagation();
            episodeList.style.display = episodeList.style.display === "none" ? "block" : "none";
        });

        season.episodes.forEach(episode => {
            const episodeItem = document.createElement("li");
            episodeItem.classList.add("col-12", "quality", "set-center");
            episodeItem.innerHTML = ` 
                <i class="fa-solid fa-download dark-purple"></i> قسمت ${episode.number}
            `;
            episodeItem.style.cursor = "pointer";

            const qualityList = document.createElement("ul");
            qualityList.style.display = "none"; 
            qualityList.style.paddingRight = "5px"; 

         
            episodeItem.addEventListener("click", (event) => {
                event.stopPropagation();
                qualityList.style.display = qualityList.style.display === "none" ? "block" : "none";
            });

            if (episode.download_urls && Array.isArray(episode.download_urls)) {
                episode.download_urls.forEach(download => {
                    const qualityItem = document.createElement("li");
                    qualityItem.style.marginBottom = "20px";

                    const link = document.createElement("a");
                    link.setAttribute("href", download.download_url);
                    link.className = "q-y";
                    link.style.padding = "5px 25px";
                    link.textContent = download.quality;

                    qualityItem.appendChild(link);
                    qualityList.appendChild(qualityItem);
                });
            }

            episodeItem.appendChild(qualityList);
            episodeList.appendChild(episodeItem);
        });

   
        seasonList.appendChild(seasonItem);
        seasonList.appendChild(episodeList);
    });

    parts.appendChild(seasonList);
}

fetchSeries();

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
                link.textContent = " بهترین سریال های کره ای" ;
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