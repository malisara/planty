// Taken from https://stackoverflow.com/a/2880929.
let urlParams = {};
(window.onpopstate = function () {
    let match,
        pl = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) {
            return decodeURIComponent(s.replace(pl, " "));
        },
        query = window.location.search.substring(1);

    while (match = search.exec(query)) {
        if (decode(match[1]) in urlParams) {
            if (!Array.isArray(urlParams[decode(match[1])])) {
                urlParams[decode(match[1])] = [urlParams[decode(match[1])]];
            }
            urlParams[decode(match[1])].push(decode(match[2]));
        } else {
            urlParams[decode(match[1])] = decode(match[2]);
        }
    }
})();


// Sort by category   
if (Array.isArray(urlParams.category)) {
    // More than 1 boxes are checked
    for (const one_category of urlParams.category) {
        document.getElementById("category_" + one_category).checked = true;
    }
} else if (typeof urlParams.category !== 'undefined') {
    // One box is checked
    document.getElementById("category_" + urlParams.category).checked = true;
}

// Max Price
if (typeof urlParams.price_value !== 'undefined') {
    var max_price_input = document.getElementById('price_value');
    max_price_input.value = urlParams.price_value;
    max_price_input.nextElementSibling.value = urlParams.price_value;
}

// Search field  
if (typeof urlParams.searched !== 'undefined' && urlParams.searched !== '') {
    document.getElementById('searched').value = urlParams.searched
}

// Sort by date    
if (typeof urlParams.date !== 'undefined') {
    document.getElementById("date_" + urlParams.date).checked = true;
}

// Sort results  
if (typeof urlParams.sort !== 'undefined') {
    document.getElementById("sort-by_" + urlParams.sort).checked = true;
}