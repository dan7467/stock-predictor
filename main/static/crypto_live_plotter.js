        // TO-DO (small bug): after saving a coin from this page, the init data of the graph is still that of the crypto_live menu
        var params = new URLSearchParams(window.location.search);
        const coin_name = params.get('requested_coin');
        const from_page_num = params.get('from_page_num');
        document.title = `i-Stocks | ${coin_name.charAt(0).toUpperCase() + coin_name.substring(1)} Live Graph`;
        const coin_recent_history = JSON.parse(params.get('last_data'));
        // console.log(coin_recent_history); // [[1734123060388,"3921.60"],[1734123062128,"3921.59"]]
        const socket = new WebSocket('wss://ws.coincap.io/prices?assets='+coin_name);
        const data = [];
        for (let i in coin_recent_history) {
            // coin_recent_history[i][0] ==  timestamp (e.g. 1734123653695)
            // coin_recent_history[i][1] ==  price_at_timestamp (e.g. 3917.13)
            data.push({x: coin_recent_history[i][0], y: parseFloat(coin_recent_history[i][1])});
        }
        const max_graph_len = 150;
        if (coin_name !== "") {
            document.getElementById('coin_title_and_price').innerHTML = `<div id="${coin_name}" class="price" style="font-size: 34px;">${coin_name.charAt(0).toUpperCase()}${coin_name.substring(1)} = <span id="${coin_name}_price">Loading...</span></div>`;
        }
        else {
            document.getElementById('coin_title_and_price').innerText = "An Error has occured, please go back and try again!";
        }
        Date.prototype.timeNow = function () {
            return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
        }
        function setBackButton() {
            document.getElementById('back_to_crypto_menu_btn').setAttribute('href', '/crypto_live?page_num='+from_page_num);
        }
        function getCookie(cname) {
            let ca = decodeURIComponent(document.cookie).split(';');
            let c;
            for(let i = 0; i <ca.length; i++) {
                c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(cname + "=") == 0) {
                    return c.substring(cname.length + 1, c.length);
                }
            }
            return "";
        }
        function update_name() {
            document.getElementById('_symbol').value = coin_name;
        }

        function setCookie(cname, cvalue, hours_to_expire) {
            const d = new Date();
            d.setTime(d.getTime() + (hours_to_expire*60*60*1000));
            document.cookie = cname + "=" + cvalue + ";" + "expires="+ d.toUTCString() + ";path=/";
        }
    
        document.addEventListener("DOMContentLoaded", function () {
            setBackButton();
            let ctx = document.getElementById('barChart').getContext('2d');
            const config = {
                type: 'line',
                data: {
                    datasets: [{
                        label: coin_name.charAt(0).toUpperCase()+coin_name.substring(1)+' Price ($)',
                        borderWidth: 2,
                        radius: 0,
                        data: data,
                        segment: {
                        borderColor: (ctx) => {
                            return ctx.p1.parsed.y > ctx.p0.parsed.y ? '#66ff33' : '#ff1a1a';
                        }
                    }
                    }]
                },
                options: {
                    interaction: {
                        intersect: false
                    },
                    plugins: { 
                        legend: {display: false}
                    },
                    scales: {
                        x: {
                            type: 'time', // Use time scale for X-axis
                            time: {
                                unit: 'second', // Format by seconds
                                displayFormats: {
                                    second: 'HH:mm:ss' // Format as HH:MM:SS:MS
                                }
                            },
                            title: { display: true, text: 'Time (HH:mm:ss)' }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Price ($)'
                            },
                            beginAtZero: false,
                        }
                    }
                }
            };

            Chart.defaults.color = "#fff";
    
            let priceChart = new Chart(ctx, config);
    
            socket.onmessage =  function (event) {
                const prices = JSON.parse(event.data);
                if (coin_name in prices) {
                    const price = parseFloat(prices[coin_name]).toFixed(3);
                    
                    const elem = document.getElementById(coin_name + '_price');

                    elem.textContent = `${Number(price).toLocaleString("en-US")} $ (USD)`;

                    data.push({ x: new Date().timeNow(), y: parseFloat(price) });

                    const lastPrice = parseFloat(getCookie(coin_name)).toFixed(3);

                    if (lastPrice !== "") {
                        config.data.datasets[0].borderColor = price > lastPrice ? '#66ff33' : '#ff1a1a';
                        elem.style.color = config.data.datasets[0].borderColor;
                    }
    
                    if (data.length > max_graph_len) {
                        data.shift();
                    }

                    setCookie(coin_name, prices[coin_name], 0.15);
    
                    priceChart.update();
                }
            };
        });