        let graphs_data = {0: [], 1: []};
        const max_graph_len = 150;

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
            let dateOfToday = getTodaysDateStr();
            const data = {
                stock_symbol: stock_name,
                from_date: dateOfToday,
                to_date: dateOfToday
            };
            client.sendHttpRequest('POST', '/get_stock_data', data, function(response) {
                let res = JSON.parse(response);
                let parsed_data = JSON.parse(res['data']);
                for (let date in parsed_data["('Close', '"+stock_name+"')"]) {
                    // coin_recent_history[i][0] ==  timestamp (e.g. 1734123653695)
                    // coin_recent_history[i][1] ==  price_at_timestamp (e.g. 3917.13)
                    graphs_data[i].push({x: date, y: parsed_data["('Close', '"+stock_name+"')"][date]});
                }

                updateGraph(stock_name, i);
            });
        }

        function updateGraph(stock_name, i) {
            let ctx = document.getElementById('barChart_'+stock_name).getContext('2d');
            const config = {
                type: 'line', // Simple line chart
                data: {
                    labels: graphs_data[i].map((point, index) => index), // Use indices as x-axis labels
                    datasets: [{
                        label: '',
                        data: graphs_data[i].map(point => point.y), // Use only y-values for the graph
                        borderColor: '#007bff', // Blue line
                        borderWidth: 1.5,
                        radius: 0, // No dots on the line
                        fill: false, // Do not fill under the line
                        tension: 0.2 // Slight curve to the line
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { 
                        legend: { display: false }, // Hide legend
                        tooltip: { enabled: false } // Disable tooltips
                    },
                    scales: {
                        x: {
                            display: false // Hide x-axis
                        },
                        y: {
                            display: false // Hide y-axis
                        }
                    }
                }
            };
        
            if (!window.priceCharts) {
                window.priceCharts = {};
            }
            if (window.priceCharts[i]) {
                window.priceCharts[i].destroy();
            }
            window.priceCharts[i] = new Chart(ctx, config);
        }
        
        function initMiniGraphs() {
            populateMiniGraph('AAPL', 0);
            populateMiniGraph('MSFT', 1);
        }
    
        document.addEventListener("DOMContentLoaded", initMiniGraphs);