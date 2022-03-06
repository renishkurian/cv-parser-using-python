debug = false;
siteUrl=''

    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)',
        darkorange: 'rgb(255,140,0)',
        darkkhaki: 'rgb(189,183,107)',
        yellowgreen: 'rgb(154,205,50)',
        olive: 'rgb(128,128,0)',
        mediumaquamarine: 'rgb(102,205,170)'
    };

$.ajaxSetup({
    accepts: {
        json: 'application/json',
    },
    headers: {
     /*   'csrfmiddlewaretoken': $('meta[name="csrf-token"]').attr('content')*/
    },
    xhr: function () {
        var xhr = new window.XMLHttpRequest();
        //Upload progress
        xhr.upload.addEventListener("progress", function (evt) {
            if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                //Do something with upload progress
                console.log(percentComplete + evt.total + '%' + evt.loaded);
            }
        }, false);
        //Download progress
        xhr.addEventListener("progress", function (evt) {
            if (evt.lengthComputable) {
                var percentComplete = evt.loaded / evt.total;
                //Do something with download progress
                console.log(evt.loaded + ' ' + percentComplete + ' ' + evt.total + '%');
            }
        }, false);
        return xhr;
    },
    'dataType': 'json',
    'error': function (jqXHR, exception) {
        if (jqXHR.status === 0) {
            alert('Not connect.\n Verify Network.');
        } else if (jqXHR.status == 404) {
            alert('Requested page not found. [404]');
        } else if (jqXHR.status == 500) {
            alert('Internal Server Error [500].');
        } else if (exception === 'parsererror') {
            alert(JSON.stringify(jqXHR));
            alert('Requested JSON parse failed.');
        } else if (exception === 'timeout') {
            alert('Time out error.');
        } else if (exception === 'abort') {
            alert('Ajax request aborted.');
        } else if (jqXHR.status == 401) {
            alert('Unauthorized Access!! Try relogin');
        } else if (jqXHR.status == 403) {
            alert('Access Forbidden');
        } else {
            alert('Uncaught Error.' + jqXHR.responseText);
        }
    },
});
function apicall(configparam) {
    configparam.data[ 'csrfmiddlewaretoken']=$('meta[name="csrf-token"]').attr('content')

    Url = siteUrl;
    var requesttype = 'POST';
    var datauploaded = configparam.data === undefined ? {} : configparam.data;
    var successfn = configparam.success;
    debug ? console.log('===============================================================' +
            '  ' +
            'api call started' +
            '  ' +
            '===============================================================') : null;
    debug ? console.log('Ajax parameters: ' + JSON.stringify(configparam)) : null;
    debug ? console.log(JSON.stringify(datauploaded)) : '';
    $.ajax({
        type: 'POST',
        url: Url + configparam.url,
        data: datauploaded,
        success: function (response) {
            debug ? console.log('===============================================================' +
                    '  ' +
                    'ajax call successful' +
                    '  ' +
                    '===============================================================') : null;
            debug && response.query !== undefined ? console.log(response.query) : null;
            successfn === undefined ? console.log('Success function undefined') : successfn(response);
        }
    });

}
function createtable(data, selector, options = {}) {

    var tbloption = options;
    tbloption.placeholder = tbloption.placeholder === undefined ? '<strong><i class="fa fa-warning"></i></strong> No Data Available' : tbloption.placeholder;
    tbloption.tooltips = tbloption.tooltips === undefined ? true : tbloption.tooltips;
    tbloption.responsiveLayout = true;
    tbloption.layout = tbloption.layout === undefined ? "fitColumns" : tbloption.layout;
    tbloption.columns = options.columns === undefined ? createcolumns(data) : options.columns;
    debug ? console.log('Tabulator options ' + JSON.stringify(tbloption)) : '';
    debug ? console.log('Data: ' + JSON.stringify(data)) : '';
    debug ? console.log('Data loading to tabulator...') : '';
    tbloption.data = data;
    debug ? console.log('Creating table in ' + selector + '...') : '';
    $(selector).tabulator(tbloption);
}

function currenttimestamp() {
    var d = new Date();
    var fullmonth = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    var shortmonth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    return d.getDate() + '-' + shortmonth[d.getMonth()] + '-' + d.getFullYear() + ' ' + d.toLocaleTimeString('en-US');
}


/*
$(document).on('focus', '.datepicker', function () {
    $(this).daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        maxDate: moment(),
        minDate: '01/01/1800',
        drops: 'up',
        locale: {
            format: 'DD-MMM-YYYY'
        }

    });
});
*/

function generatedd(dddata, selector, selected = '') {
    var dd = '';
    var select_option = selected === '' ? 'selected' : '';
    dd = '<option value="" ' + select_option + '>' + dddata.default + '</option>';
    $.each(dddata.response.data, function (index, value) {
        select_option = selected === value[dddata.val_col] ? 'selected' : '';
        dd += '<option value="' + value[dddata.val_col] + '" ' + select_option + '>' + value[dddata.option_col] + '</option>';
//        debug ? console.log(dd) : null;
    });
    $(selector+' #'+dddata.id).remove();
    $(selector).append('<select class="' + dddata.class + '" id="' + dddata.id + '">'+dd+'</select>');
}