'use strict'

if (!('content' in document.createElement('template'))) {
    alert('Your browser doesn’t support the HTML template.')
}

document.getElementById('noti-file-input')
    .addEventListener('change', function(event) {
        var file = event.target.files[0];
        noti_input(file);
    });

function noti_input(file) {
    var reader = new FileReader();
    reader.addEventListener('load', function() {
        var noti = JSON.parse(this.result);
        deal_with_noti(noti);
    });
    reader.readAsText(file);
}

var notisTable;

function deal_with_noti(noti) {
    let notifications_list = noti.notifications_list;
    let url_content_pair = noti.url_content_pair;

    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template
    var tbody = document.querySelector('tbody');
    var template = document.querySelector('#tr-temp');

    notifications_list.forEach(function(item, index) {
        var clone = template.content.cloneNode(true);
        var td = clone.querySelectorAll('td');
        td[0].textContent = item[0] + ' (' + (index + 1).toString() + ')';
        td[1].textContent = item[1];
        td[2].textContent = item[2];
        td[3].textContent = 'u:' + item[3];
        td[4].textContent = 's:' + item[4];

        let s_url = item[4];
        let s_content;
        if (s_url == '-') {
            s_content = 'Type follow or follow_request doesn’t have a status.';
        } else {
            s_content = url_content_pair[s_url];
        }
        td[5].textContent = s_content;

        tbody.appendChild(clone);
    })

    var options = {
        valueNames: ['i', 't', 'a', 'u', 's', 'c'],
        listClass: 'notifications',
        searchClass: 'search-status',
        searchColumns: ['u', 's', 'c'],
        searchDelay: 500,
        pagination: false,
    };

    notisTable = new List('notis', options);
}

// https://stackoverflow.com/questions/14544104/
var checkboxes = document.querySelectorAll('input[type=checkbox][name=c-type]');
checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        let selected_tpye =
            Array.from(checkboxes)
            .filter(i => i.checked)
            .map(i => i.value);
        notisTable.filter(function(item) {
            if (selected_tpye.includes(item.values().t)) {
                return true;
            } else {
                return false;
            }
        });
    })
});

function show(e) {
    // https://developer.mozilla.org/zh-CN/docs/Web/API/Element/previousElementSibling
    let content = e.previousElementSibling.textContent;
    // innerHTML to escape; textContent parse them.
    document.getElementById('content').innerHTML = content;
}
