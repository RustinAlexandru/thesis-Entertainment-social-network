/**
 * Created by alexandrurustin on 7/26/16.
 */


var orderByPoints = 'points';
var orderByDate = 'date_added';
var itemType = 'Any';

var data = {
    date_orderBy: orderByDate,
    points_orderBy: orderByPoints,
    itemType: itemType
};

function sendRequest() {


    $.ajax({
        url: '',
        type: 'GET',
        data: data,
        success: function (data) {
            $(".endless_page_template").html(data)
        },
        error: function (err) {
            console.log('err: ' + err);
        }
    });
}

function changeIcons(selector){

    var checkbox = $(selector + " :checkbox");
    var icon_var = $(selector).children(":nth-child(2)");
    if (checkbox.is(':checked')) {
        // the checkbox was checked
        icon_var.removeClass("fa-arrow-down");
        icon_var.addClass("fa-arrow-up");
    } else {
        // the checkbox was unchecked
        icon_var.removeClass("fa-arrow-up");
        icon_var.addClass("fa-arrow-down");

    }
}



$(document).ready(function () {

    var date_orderby_selector = '#date_orderBy';
    var points_orderby_selector = '#points_orderBy';
    var date_checkbox_selector = date_orderby_selector + " :checkbox";
    var points_checkbox_selector = points_orderby_selector + " :checkbox";


    $("body").tooltip({
        selector: '[data-toggle="tooltip"]'
    });

    $(date_checkbox_selector).on('change', function () {
        changeIcons(date_orderby_selector);

        data['date_orderBy'] = ($(date_checkbox_selector).is(':checked') ? '-date_added' : 'date_added');
        sendRequest();
    });

    $(points_checkbox_selector).on('change', function () {
        changeIcons(points_orderby_selector);

        data['points_orderBy'] = ($(points_checkbox_selector).is(':checked') ? '-points' : 'points');
        sendRequest();
    });


    page_href = window.location.href;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('click', '.save_item', function () {

        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");

        itemType = $(this).attr("data-item-type");

        url = page_href;
        if (url.indexOf("page") !== -1) { //  url contains 'page' in it, needs adjustment
            // get_params_pos= url.indexOf("?")  // insert 'add_to_savelist' before get parameters
            if (url.indexOf("ninegags") !== -1) {
                url = url.replace("/ninegags/", "/ninegags/add_to_savelist/");
            } else if (url.indexOf("videos") !== -1) {
                url = url.replace("/videos/", "/videos/add_to_savelist/");
            } else if (url.indexOf("jokes") !== -1) {
                url = url.replace("/jokes/", "/videos/add_to_savelist/");
            }
        } else {
            url = page_href + 'add_to_savelist/'; // first page in a paginated list, url doesnt contain 'page' in it
        }

        data_received = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                "data": JSON.stringify(data_received)
            },
            dataType: "json",
            success: function (data) {
                if (!data["integrity_error"]) {
                    swal(
                        'Good job!',
                        'You added the item to your personal save list!',
                        'success'
                    )
                }
                else {  // integrity_error message alert
                    sweetAlert(
                        'Oops...',
                        "We're sorry, you've already added this item, you cannot add the same item twice!",
                        'error'
                    )
                }

            },
            error: function (data) {
                sweetAlert(
                    'Oops...',
                    'Something went wrong!',
                    'error'
                )
            }
        });
    });

    $(document).on('click', '.add_point', function () {
        item_id = $(this).attr("data-item-id");
        item_type = $(this).attr("data-item-type");

        $("#likes").toggleClass('text-primary');
        $(this).toggleClass('text-primary');

        url = page_href;
        if (url.indexOf("page") !== -1) { //  url contains 'page' in it, needs adjustment
            // get_params_pos= url.indexOf("?")  // insert 'add_to_savelist' before get parameters
            if (url.indexOf("ninegags") !== -1) {
                url = url.replace("/ninegags/", "/ninegags/add_point/");
            } else if (url.indexOf("videos") !== -1) {
                url = url.replace("/videos/", "/videos/add_point/");
            } else if (url.indexOf("jokes") !== -1) {
                url = url.replace("/jokes/", "/videos/add_point/");
            }
        } else {
            url = page_href + 'add_point/'; // first page in a paginated list, url doesnt contain 'page' in it
        }

        data_sent = {
            "item_id": item_id,
            "item_type": item_type
        };
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'data': JSON.stringify(data_sent)
            },
            dataType: "json",
            success: function (data) {
                $('#points').html(data['points']);
                selector = "i[data-item-id=" + item_id + "]";
                $(selector).parents()[0].remove()
            },
            error: function (data) {
                sweetAlert(
                    'Oops...',
                    'Something went wrong!',
                    'error'
                )
            }
        });
    });

    $("#filter_sort_form").on('submit', function (e) {
        current_page = $('.endless_page_current > strong:nth-child(1)').text();
        // url = window.location.href + '?page=' + current_page + '&querystring_key=page'
        data['itemType'] = $('.selectpicker').val();
            $.ajax({
                url: '',
                type: 'GET',
                data: data,
                success: function (data) {
                    $(".endless_page_template").html(data)
                },
                error: function (err) {
                    console.log('err: ' + err);
                }
            });
            e.preventDefault();
        });

    $("#filter_sort_form").on('change', "[data-input]", function () {
        $("#filter_sort_form").submit()
    });

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
