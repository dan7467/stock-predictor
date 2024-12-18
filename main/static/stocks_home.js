        let graphs_data = {0: [], 1: []};
        const max_graph_len = 150;
        let chart = {};
        Date.prototype.timeNow = function () {
            return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
        }
        function getTodaysDateStr() {  // formatted: YYYY-MM-DD
            var today = new Date();
            return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        }
        var HttpClient = function() {
            this.sendHttpRequest = function(requestType, aUrl, data, aCallback) {
                var anHttpRequest = new XMLHttpRequest();
                anHttpRequest.onreadystatechange = function() {
                    if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                        aCallback(anHttpRequest.responseText);
                };
                anHttpRequest.open(requestType, aUrl, true);
                anHttpRequest.setRequestHeader("Content-Type", "application/json"); // Set content type to JSON
                anHttpRequest.send(JSON.stringify(data)); // Send data as JSON
            };
        };
        
        var client = new HttpClient();
        function populateMiniGraph(stock_name, i) {
            return new Promise((resolve, reject) => {
                let dateOfToday = getTodaysDateStr();
                const data = { stock_symbol: stock_name, from_date: dateOfToday, to_date: dateOfToday };
                
                client.sendHttpRequest('POST', '/get_stock_data', data, function(response) {
                    try {
                        let res = JSON.parse(response);
                        let parsed_data = JSON.parse(res['data']);
                        document.getElementById('tile_'+i).innerHTML += `&emsp;&ensp; <b style="font-size: 14px;">${res['last_price'].toLocaleString()}</b>`;
                        for (let date in parsed_data["('Close', '"+stock_name+"')"]) {
                            graphs_data[i].push({x: date, y: parsed_data["('Close', '"+stock_name+"')"][date]});
                        }
                        updateGraph(stock_name, i);
                        resolve();
                    } catch (error) {   
                        console.error("Error parsing data for", stock_name, error);
                        reject(error);
                    }
                });
            });
        }

        let width, height, gradient;

        function getGradient(ctx, chartArea) {
            const chartWidth = chartArea.right - chartArea.left;
            const chartHeight = chartArea.bottom - chartArea.top;
            if (!gradient || width !== chartWidth || height !== chartHeight) {
                width = chartWidth;
                height = chartHeight;
                gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                gradient.addColorStop(1, 'rgb(0, 123, 255)');
                gradient.addColorStop(.25, 'rgba(0,128, 0, 0)');
            }
            return gradient;
        }

        function updateGraph(stock_name, i) {
            let ctx = document.getElementById('barChart_'+stock_name).getContext('2d');
            const config = {
                type: 'line',
                data: {
                    labels: graphs_data[i].map((point, index) => index),
                    datasets: [{
                        label: '',
                        data: graphs_data[i].map(point => point.y),
                        borderColor: '#007bff',
                        pointBackgroundColor: 'transparent',
                        pointBorderColor: 'transparent',
                        borderJoinStyle: 'bevel',
                        // the following 2 properties are the ones that need to be set
                        fill: {
                            value: -25,
                        },
                        backgroundColor: (context) => {
                        const chart = context.chart;
                        const {ctx, chartArea} = chart;
                        if (!chartArea) {
                            // This case happens on initial chart load
                            return;
                        }
                        return getGradient(ctx, chartArea);
                        },
                    }]
                },
                options: { responsive: true, scales: { x: { display: false }, y: { display: false } } }
            };
            chart['chart_'+i] = new Chart(ctx, config);
        }
        
        async function initMiniGraphs() {
            const number_of_tiles = 2;
            try {
                for (let i = 0; i < number_of_tiles; i++) {
                    if (document.getElementById('tile_'+i) != null) {
                        await populateMiniGraph(document.getElementById('tile_'+i).innerText, i);
                    }
                }
            } catch (error) {
                console.error("Error initializing graphs:", error);
            }
        }

        document.addEventListener("DOMContentLoaded", initMiniGraphs);