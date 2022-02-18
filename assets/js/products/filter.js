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

function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);
    var kvp = document.location.search.substr(1).split('&');
    let i = 0;
    for (; i < kvp.length; i++) {
        if (kvp[i].startsWith(key + '=')) {
            let pair = kvp[i].split('=');
            pair[1] = value;
            kvp[i] = pair.join('=');
            break;
        }
    }
    if (i >= kvp.length) {
        kvp[kvp.length] = [key, value].join('=');
    }
    let params = kvp.join('&');
    document.location.search = params;
}

function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        if (params_arr.length) rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

// Pagination

let btnsPage = document.querySelectorAll('[btn-page-pagination]')
for (let btn of btnsPage) {
    btn.addEventListener('click', function () {
        console.log(this)
        let pageNum = this.getAttribute('pageNum')
        insertParam('page', pageNum)
    })
}

let btnNextPage = document.querySelector('[btn-next-page-pagination]')
let btnPreVioustPage = document.querySelector('[btn-previous-page-pagination]')

if (btnNextPage) {
    btnNextPage.addEventListener('click', function () {
        insertParam('page', window._pageNum + 1)
    })
}
if (btnPreVioustPage) {
    btnPreVioustPage.addEventListener('click', function () {
        insertParam('page', window._pageNum - 1)
    })
}


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
