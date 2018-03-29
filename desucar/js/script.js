const baseUrl = ''
const searchbar = document.querySelector('.q')
const autocomplete = document.querySelector('.autocomplete')
const tabs = document.querySelector('.navbar-tabs')
const defects = document.querySelectorAll('.defect')

let cars = []
let currentTab

if (searchbar) {
  const renderSuggestion = () => {
    autocomplete.innerHTML = ''
    cars.forEach(car => {
      autocomplete.innerHTML += `
          <li class="dropdown-item">
            <a href="/${car.fields.maker}/${car.fields.simple_name}-${car.fields.make_start.substr(0, 4)}-${car.fields.code}">${car.fields.name}</a>
          </li>
          `
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
    if (!searchbar.value) {
      cars = []
      renderSuggestion()
    } else {
      return new Promise((resolve, reject) => {
        const req = new XMLHttpRequest()
        req.open('GET', `${baseUrl}/suggest?q=${searchbar.value}`)
        req.send()
        req.onreadystatechange = function () {
          if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
              cars = JSON.parse(req.response)
              renderSuggestion()
            }
          }
        }
      })
    }
  }, 300)

  searchbar.addEventListener('input', getSuggestion)
}

const toggleTab = (tab) => {
  if (tab.id !== currentTab.id) {
    currentTab.classList.remove('active')
    currentTab = tab
    currentTab.classList.add('active')
    renderDefects(currentTab.id)
  }
}

const renderDefects = (id) => {
  defects.forEach(d => {
    d.style.display = d.className.includes(id) ? '' : 'none'
  })
}

if (tabs) {
  currentTab = Array.from(tabs.children).find(item => !item.classList.contains('no-value'))
  if (currentTab) {
    currentTab.classList.add('active')
    renderDefects(currentTab.id)
  }

  tabs.addEventListener('click', e => {
    if (e.target.nodeName === 'LI') {
      toggleTab(e.target)
    }
  })
}
