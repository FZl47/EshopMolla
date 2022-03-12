// filter
let categoriesSelected = []
let colorsSelected = []
let brandsSelected = []
let inputColorFilter = document.querySelectorAll('[color-input-filter]')
for (let inp of inputColorFilter) {
    inp.onclick = function (e) {
        let selected = this.getAttribute('selected') || 'false'
        if (selected == 'false') {
            this.setAttribute('selected', 'true')
        } else {
            this.setAttribute('selected', 'false')
        }
    }
}

let applyFilters = document.getElementById('applyFilters')
let filterItemsCategory = document.getElementById('filter-items-category')
let filterItemsColor = document.getElementById('filter-items-color')
let filterItemsBrand = document.getElementById('filter-items-brand')

applyFilters.addEventListener('click', function () {
    if (filterItemsCategory) {
        let inputCategories = filterItemsCategory.querySelectorAll('input')
        for (let inp of inputCategories) {
            if (inp.checked) {
                let urlFilter = inp.getAttribute('url-filter')
                categoriesSelected.push(urlFilter)
            }
        }
    }

    if (filterItemsColor) {
        let btntColor = filterItemsColor.querySelectorAll('button')
        for (let btn of btntColor) {
            let checked = (btn.getAttribute('selected') || 'false') == 'true'
            if (checked) {
                let urlFilter = btn.getAttribute('url-filter')
                colorsSelected.push(urlFilter)
            }
        }
    }

    if (filterItemsBrand) {
        let inputBrands = filterItemsBrand.querySelectorAll('input')
        for (let inp of inputBrands) {
            if (inp.checked) {
                let urlFilter = inp.getAttribute('url-filter')
                brandsSelected.push(urlFilter)
            }
        }
    }


    let url = new URLSearchParams(window.location.search);
    url.set('page', '1')
    url.set('filter', 'true')
    url.set('cats', categoriesSelected.join('_'))
    url.set('brands', brandsSelected.join('_'))
    url.set('colors', colorsSelected.join('_'))
    url.set('range', window._rangePriceFilter)
    window.location.search = url;


})


//sort
let sortby = document.getElementById('sortby')
let urlSortBy = new URLSearchParams(window.location.search)
let orderedBy = urlSortBy.get('orderby')
try {
    sortby.querySelector(`[value=${orderedBy}]`).selected = 'selected'
} catch (e) {
}
sortby.onchange = function () {
    urlSortBy.set('orderby', this.value)
    urlSortBy.set('page', 1)
    window.location.search = urlSortBy
}
