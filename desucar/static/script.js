var baseUrl = '';
var searchbar = document.querySelector('.q');
var autocomplete = document.querySelector('.autocomplete');
var tabs = document.querySelector('.navbar-tabs');
var defects = document.querySelectorAll('.defects');

var cars = [];
var currentTab = void 0;

if (searchbar) {
  var renderSuggestion = function renderSuggestion() {
    autocomplete.innerHTML = '';
    cars.forEach(function (car) {
      autocomplete.innerHTML += '\n          <li class="dropdown-item">\n            <a href="/' + car.fields.maker + '/' + car.fields.simple_name + '-' + car.fields.make_start.substr(0, 4) + '-' + car.fields.code + '">' + car.fields.name + '</a>\n          </li>\n          ';
    });
  };

  var debounce = function debounce(func, wait, immediate) {
    var timeout = void 0;
    return function () {
      var context = this;
      var args = arguments;
      var later = function later() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  };

  var getSuggestion = debounce(function () {
    if (!searchbar.value) {
      cars = [];
      renderSuggestion();
    } else {
      return new Promise(function (resolve, reject) {
        var req = new XMLHttpRequest();
        req.open('GET', baseUrl + '/suggest?q=' + searchbar.value);
        req.send();
        req.onreadystatechange = function () {
          if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
              cars = JSON.parse(req.response);
              renderSuggestion();
            }
          }
        };
      });
    }
  }, 300);

  searchbar.addEventListener('input', getSuggestion);
}

var toggleTab = function toggleTab(tab) {
  if (tab.id !== currentTab.id) {
    currentTab.classList.remove('active');
    currentTab = tab;
    currentTab.classList.add('active');
    renderDefects(currentTab.id);
  }
};

var renderDefects = function renderDefects(id) {
  defects.forEach(function (d) {
    d.style.display = d.className.includes(id) ? '' : 'none';
  });
};

if (tabs) {
  currentTab = Array.from(tabs.children).find(function (item) {
    return !item.classList.contains('no-value');
  });
  if (currentTab) {
    currentTab.classList.add('active');
    renderDefects(currentTab.id);
  }

  tabs.addEventListener('click', function (e) {
    if (e.target.nodeName === 'LI') {
      toggleTab(e.target);
    }
  });
}

var more = document.querySelectorAll('.more');
more.forEach(function (el) {
  el.querySelector('.more-toggle').addEventListener('click', function (event) {
    el.classList.add('visible');
  });
});

var ellipsis = document.querySelectorAll('.ellipsis');
ellipsis.forEach(function (el) {
  el.querySelector('.expand').addEventListener('click', function (event) {
    el.classList.add('expanded');
  });
});