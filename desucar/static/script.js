var baseUrl = '';
var searchbar = document.querySelector('.q');
var autocomplete = document.querySelector('.autocomplete');

var q = '';
var cars = [];
var carIndex = -1;
var currentTab = void 0;

if (searchbar) {
  var renderSuggestion = function renderSuggestion() {
    var i = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;

    autocomplete.innerHTML = '';
    cars.forEach(function (car, index) {
      var item = i === index ? '\n          <li class="dropdown-item focused">\n            <a href="/' + car.fields.maker + '/' + car.fields.simple_name + '-' + car.fields.make_start.substr(0, 4) + '-' + car.fields.code + '">' + car.fields.name + '</a>\n          </li>' : '\n          <li class="dropdown-item">\n            <a href="/' + car.fields.maker + '/' + car.fields.simple_name + '-' + car.fields.make_start.substr(0, 4) + '-' + car.fields.code + '">' + car.fields.name + '</a>\n          </li>';
      autocomplete.innerHTML += item;
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
    q = searchbar.value;
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

  var selectCar = function selectCar(i) {
    renderSuggestion(i);
    if (i === -1) {
      searchbar.value = q;
    } else {
      searchbar.value = cars[i].fields.name;
    }
  };

  var shiftFocus = function shiftFocus(i) {
    if (carIndex === -1 && i < 0) {
      carIndex = cars.length - 1;
    } else if (carIndex === cars.length - 1 && i > 0) {
      carIndex = -1;
    } else {
      carIndex += i;
    }
    selectCar(carIndex);
  };

  searchbar.addEventListener('keydown', function (e) {
    // up key
    if (e.keyCode === 38 && cars.length) {
      e.preventDefault();
      shiftFocus(-1);
    }
    // down key
    if (e.keyCode === 40 && cars.length) {
      e.preventDefault();
      shiftFocus(1);
    }
    // FIXME: 텍스트 입력에 해당하는 키만 감지하는 조건문으로 변경
    if (e.key.length === 1 || e.keyCode === 8) {
      getSuggestion();
    }
  });
}

// const toggleTab = (tab) => {
//   if (tab.id !== currentTab.id) {
//     currentTab.classList.remove('active')
//     currentTab = tab
//     currentTab.classList.add('active')
//     renderDefects(currentTab.id)
//   }
// }
//
// const renderDefects = (id) => {
//   defects.forEach(d => {
//     d.style.display = d.className.includes(id) ? '' : 'none'
//   })
// }
//
// if (tabs) {
//   currentTab = Array.from(tabs.children).find(item => !item.classList.contains('no-value'))
//   if (currentTab) {
//     currentTab.classList.add('active')
//     renderDefects(currentTab.id)
//   }
//
//   tabs.addEventListener('click', e => {
//     if (e.target.nodeName === 'LI') {
//       toggleTab(e.target)
//     }
//   })
// }

// const more = document.querySelectorAll('.more')
// more.forEach(function (el) {
//   el.querySelector('.more-toggle').addEventListener('click', function (event) {
//     el.classList.add('visible')
//   })
// })
//
//
// const ellipsis = document.querySelectorAll('.ellipsis')
// ellipsis.forEach(function (el) {
//   el.querySelector('.expand').addEventListener('click', function (event) {
//     el.classList.add('expanded')
//   })
// })


var tabs = document.querySelectorAll('.navbar-tab');
tabs.forEach(function (tab) {
  tab.addEventListener('click', function () {
    tabs.forEach(function (t) {
      t.dataset.tabId === tab.dataset.tabId ? t.classList.add('active') : t.classList.remove('active');
    });
    document.querySelectorAll('.navbar-content').forEach(function (content) {
      content.dataset.tabId === tab.dataset.tabId ? content.classList.add('active') : content.classList.remove('active');
    });
  });
});

var _loop = function _loop(tab) {
  var nText = tab.querySelector('.value').textContent;
  var n = parseInt(nText);
  if (n > 0) {
    tabs.forEach(function (t) {
      t.dataset.tabId === tab.dataset.tabId ? t.classList.add('active') : t.classList.remove('active');
    });
    document.querySelectorAll('.navbar-content').forEach(function (el) {
      if (el.dataset.tabId === tab.dataset.tabId) {
        el.classList.add('active');
      }
    });
    return 'break';
  }
};

var _iteratorNormalCompletion = true;
var _didIteratorError = false;
var _iteratorError = undefined;

try {
  for (var _iterator = tabs[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
    var tab = _step.value;

    var _ret = _loop(tab);

    if (_ret === 'break') break;
  }
} catch (err) {
  _didIteratorError = true;
  _iteratorError = err;
} finally {
  try {
    if (!_iteratorNormalCompletion && _iterator.return) {
      _iterator.return();
    }
  } finally {
    if (_didIteratorError) {
      throw _iteratorError;
    }
  }
}

document.querySelectorAll('.foldable').forEach(function (foldable) {
  foldable.addEventListener('click', function () {
    foldable.classList.toggle('closed');
  });
});