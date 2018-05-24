import 'babel-polyfill';


const baseUrl = ''
const searchbar = document.querySelector('.q')
const autocomplete = document.querySelector('.autocomplete')

let q = ''
let cars = []
let carIndex = -1


if (searchbar) {
  const renderSuggestion = (i = null) => {
    autocomplete.innerHTML = ''
    cars.forEach((car, index) => {
      const item = i === index
        ? `
          <li class="dropdown-item focused">
            <a href="/${car.fields.maker}/${car.fields.simple_name}-${car.fields.make_start.substr(0, 4)}-${car.fields.code}">${car.fields.name}</a>
          </li>`
        : `
          <li class="dropdown-item">
            <a href="/${car.fields.maker}/${car.fields.simple_name}-${car.fields.make_start.substr(0, 4)}-${car.fields.code}">${car.fields.name}</a>
          </li>`
      autocomplete.innerHTML += item
    })
  }

  const debounce = (func, wait, immediate) => {
    let timeout
    return function () {
      const context = this
      const args = arguments
      const later = () => {
        timeout = null
        if (!immediate) func.apply(context, args)
      }
      const callNow = immediate && !timeout
      clearTimeout(timeout)
      timeout = setTimeout(later, wait)
      if (callNow) func.apply(context, args)
    }
  }

  const getSuggestion = debounce(() => {
    q = searchbar.value
    if (!searchbar.value) {
      cars = []
      renderSuggestion()
    } else {
      return new Promise((resolve, reject) => {
        const req = new XMLHttpRequest()
        req.open('GET', `${baseUrl}/suggest?q=${searchbar.value}`)
        req.onreadystatechange = function () {
          if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
              cars = JSON.parse(req.response)
              renderSuggestion()
            }
          }
        }
        req.send()
      })
    }
  }, 300)

  const selectCar = (i) => {
    renderSuggestion(i)
    if (i === -1) {
      searchbar.value = q
    } else {
      searchbar.value = cars[i].fields.name
    }
  }

  const shiftFocus = (i) => {
    if (carIndex === -1 && i < 0) {
      carIndex = cars.length - 1
    } else if (carIndex === cars.length - 1 && i > 0) {
      carIndex = -1
    } else {
      carIndex += i
    }
    selectCar(carIndex)
  }

  searchbar.addEventListener('keydown', e => {
    // up key
    if (e.keyCode === 38 && cars.length) {
      e.preventDefault()
      shiftFocus(-1)
    }
    // down key
    if (e.keyCode === 40 && cars.length) {
      e.preventDefault()
      shiftFocus(1)
    }
    // FIXME: 텍스트 입력에 해당하는 키만 감지하는 조건문으로 변경
    if (e.key.length === 1 || e.keyCode === 8) {
      getSuggestion()
    }
  })
}


class Floating {
  constructor(el) {
    this.el = el
    this.tabShare = this.el.querySelector('.utils .util.share')
    this.tabReport = this.el.querySelector('.utils .util.report')
    this.tabShare.querySelector('.btn-close').addEventListener('click', this.closeAll)
    this.tabReport.querySelector('.btn-close').addEventListener('click', this.closeAll)
    this.btnShare = this.el.querySelector('.btns .btn.share')
    this.btnReport = this.el.querySelector('.btns .btn.report')
    this.btnShare.addEventListener('click', this.showShare)
    this.btnReport.addEventListener('click', this.showReport)
  }

  closeAll = () => {
    this.tabShare.classList.remove('active')
    this.tabReport.classList.remove('active')
  }

  showShare = () => {
    if (this.tabShare.classList.contains('active')) {
      this.tabShare.classList.remove('active')
    } else {
      this.tabReport.classList.remove('active')
      this.tabShare.classList.add('active')
    }
  }

  showReport = () => {
    if (this.tabReport.classList.contains('active')) {
      this.tabReport.classList.remove('active')
    } else {
      this.tabShare.classList.remove('active')
      this.tabReport.classList.add('active')
      window.dispatchEvent(new Event('resize'))
    }
  }
}


if (document.querySelector('.floating')) {
  new Floating(document.querySelector('.floating'))
}


document.querySelectorAll('.overview').forEach(overview => {
  const desc = overview.querySelector('.status-desc')
  const btn = overview.querySelector('.btn-show-desc')
  btn.addEventListener('click', () => {
      desc.classList.toggle('visible')
  })
})


const tabs = document.querySelectorAll('.navbar-tab');
tabs.forEach(function (tab) {
  tab.addEventListener('click', function() {
    tabs.forEach(function (t) {
      t.dataset.tabId === tab.dataset.tabId ?
        t.classList.add('active') :
        t.classList.remove('active')
    });
    document.querySelectorAll('.navbar-content').forEach(function (content) {
      content.dataset.tabId === tab.dataset.tabId ?
        content.classList.add('active') :
        content.classList.remove('active')
    })
  })
})


for (const tab of tabs) {
  const nText = tab.querySelector('.value').textContent
  const n = parseInt(nText)
  if (n > 0) {
    tabs.forEach(function (t) {
        t.dataset.tabId === tab.dataset.tabId ?
            t.classList.add('active') :
            t.classList.remove('active')
    });
    document.querySelectorAll('.navbar-content').forEach(function (el) {
      if (el.dataset.tabId === tab.dataset.tabId) {
        el.classList.add('active')
      }
    })
    break
  }
}


document.querySelectorAll('.foldable').forEach(function (foldable) {
  foldable.querySelector('.title').addEventListener('click', function() {
    foldable.classList.toggle('closed')
  })
})



