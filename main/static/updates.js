// Many issues here to debug:

// TO-DO: fix auto-get coin price issue (on Create Subscription)

// TO-DO: fix issue when existing subscription's coin range is reached - auto refresh

// TO-DO: force the Notifications Table show only the last 6 Notifications, for the UI to be comfortable
            // it probably requires migrating models.py to use a dict instead of a list,
            // since currently the viewing and deletion of notifications is according to their list index

document.getElementById("stock_sym").addEventListener("focusout", getStockCurrentPrice);

var HttpClient = function () {
    this.sendHttpRequest = function (requestType, aUrl, data, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function () {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        };
        anHttpRequest.open(requestType, aUrl, true);
        anHttpRequest.setRequestHeader("Content-Type", "application/json"); // Set content type to JSON
        anHttpRequest.send(JSON.stringify(data)); // Send data as JSON
    };
};

var client = new HttpClient();

function formatNumToFixed(num, decimals) {
    return (Math.round(num * 100) / 100).toFixed(decimals);
}

function getStockCurrentPrice() {
    let sym = document.getElementById('stock_sym').value;
    if (sym !== '') {
        const data = {
            stock_symbol: sym
        };
        client.sendHttpRequest('POST', '/get_current_stock_price', data, function (response) {
            let res = JSON.parse(response);
            let parsed_data = JSON.parse(res['data']);
            let keys_as_nums = Object.keys(parsed_data['Close']).map((x) => Number(x));
            let lastPrice = parsed_data['Close'][keys_as_nums[keys_as_nums.length - 1].toString()];
            document.getElementById("bound_val").value = formatNumToFixed(lastPrice, 3);
            document.getElementById("value_refresh_disclaimer").innerHTML = `Note: the above price is fetched every minute,<br/> so refrain from taking it as ms/second-accurate`;
        });
    } else {
        alert('Error: No stock symbol input');
    }
}

function remove_subscription(stock_sym, dir, val) {
    document.getElementById('del_stock_sym').value = stock_sym;
    document.getElementById('del_price_direction').value = dir;
    document.getElementById('del_bound_val').value = val;
    document.getElementById('del_' + stock_sym + '_' + dir + '_' + val + '_' + '_btn').innerHTML = 'Loading...';
    document.getElementById('del_' + stock_sym + '_' + dir + '_' + val + '_' + '_btn').className = 'btn btn-secondary';
}

function remove_notification(notification_index) {
    document.getElementById('del_notification_id').value = notification_index;
    document.getElementById('del_' + notification_index).innerHTML = 'Loading...';
}

function reveal_subscription_form() {
    document.getElementById("add_subscription_btn").style.visibility = "hidden";
    document.getElementById("subscribe_form_container").style.visibility = "visible";
}
