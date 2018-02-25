const baseUrl = 'http://127.0.0.1:8000'
const searchbar = document.querySelector('.q')
const dropdown = document.querySelector('.dropdown')
const autocomplete = document.querySelector('.autocomplete')

let cars = [];

const render = () => {
    autocomplete.innerHTML = '';
    cars.forEach(car => {
        autocomplete.innerHTML += `
        <li class="dropdown-item"><a href="/${car.fields.maker}/${car.fields.simple_name}-${car.fields.make_start.substr(0, 4)}-${car.fields.code}">${car.fields.name}</a></li>
        `            
    })
}

const debounce = (func, wait, immediate) => {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

const getSuggestion = debounce(() => {
    if (!searchbar.value) {
        cars = [];
        render();
    }
    return new Promise((res, rej) => {
        const req = new XMLHttpRequest();
        req.open('GET', `${baseUrl}/suggest?q=${searchbar.value}`);
        if (searchbar.value)
        req.send();
        req.onreadystatechange = function () {
            if (req.readyState === XMLHttpRequest.DONE) {
                if (req.status === 200) {
                    cars = JSON.parse(req.response)
                    render()
                }
            }
        };
    })
}, 300)

searchbar.addEventListener('input', getSuggestion)