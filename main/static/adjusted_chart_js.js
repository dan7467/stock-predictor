function update_name() {
    document.getElementById('_symbol').value = document.getElementById('stock_sym').value;
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

function getStockData() {
    let sym = document.getElementById('stock_sym').value;
    if (sym !== '') {
        const data = {
            stock_symbol: sym,
            from_date: document.getElementById('date_start').value,
            to_date: document.getElementById('date_end').value
        };
        client.sendHttpRequest('POST', 'http://127.0.0.1:8000/get_stock_data', data, function(response) {
            refreshStockData(response, sym);
            refreshCompanyInfo(sym);
        });
    } else {
        alert('Error: No stock symbol input');
    }
}
function formatNumToFixed(num, decimals){
    return (Math.round(num * 100) / 100).toFixed(decimals);
}
(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('chart.js'), require('chart.js/helpers')) :
    typeof define === 'function' && define.amd ? define(['chart.js', 'chart.js/helpers'], factory) :
    (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.Chart, global.Chart.helpers));
    })(this, (function (chart_js, helpers) { 'use strict';
    
    class FinancialController extends chart_js.BarController {
    
    static overrides = {
        label: '',
    
        parsing: false,
    
        hover: {
        mode: 'label'
        },
        animations: {
        numbers: {
            type: 'number',
            properties: ['x', 'y', 'base', 'width', 'open', 'high', 'low', 'close']
        }
        },
    
        scales: {
        x: {
            type: 'time', // or 'linear' depending on your data
            time: {
                displayFormats: {
                        day: 'DD, hh:mm'
                    }
            },
            ticks: {
                autoSkip: false, // Ensures all labels are shown
                maxRotation: 45, // Adjust for better readability
                minRotation: 45
            }
        },
        y: {
            type: 'linear'
        }
        },
    
        plugins: {
            tooltip: {
                intersect: false,
                mode: 'index',
                callbacks: {
                    label(ctx) {
                        const point = ctx.parsed;
                        if (!helpers.isNullOrUndef(point.y)) {
                            return chart_js.defaults.plugins.tooltip.callbacks.label(ctx);
                        }
                        const {o, h, l, c, v} = point;
                        return `O: ${o}  H: ${h}  L: ${l}  C: ${c} V: ${v}`;
                    }
                }
            }
        }
    };
    
    getLabelAndValue(index) {
        const me = this;
        const parsed = me.getParsed(index);
        const axis = me._cachedMeta.iScale.axis;
    
        const {o, h, l, c, v} = parsed;
        const value = `O: ${o}  H: ${h}  L: ${l}  C: ${c} V: ${v}`;
    
        return {
        label: `${me._cachedMeta.iScale.getLabelForValue(parsed[axis])}`,
        value
        };
    }
    
    getUserBounds(scale) {
        const {min, max, minDefined, maxDefined} = scale.getUserBounds();
        return {
        min: minDefined ? min : Number.NEGATIVE_INFINITY,
        max: maxDefined ? max : Number.POSITIVE_INFINITY
        };
    }
    
    /**
        * Implement this ourselves since it doesn't handle high and low values
        * https://github.com/chartjs/Chart.js/issues/7328
        * @protected
        */
    getMinMax(scale) {
        const meta = this._cachedMeta;
        const _parsed = meta._parsed;
        const axis = meta.iScale.axis;
        const otherScale = this._getOtherScale(scale);
        const {min: otherMin, max: otherMax} = this.getUserBounds(otherScale);
    
        if (_parsed.length < 2) {
        return {min: 0, max: 1};
        }
    
        if (scale === meta.iScale) {
        return {min: _parsed[0][axis], max: _parsed[_parsed.length - 1][axis]};
        }
    
        const newParsedData = _parsed.filter(({x}) => x >= otherMin && x < otherMax);
    
        let min = Number.POSITIVE_INFINITY;
        let max = Number.NEGATIVE_INFINITY;
        for (let i = 0; i < newParsedData.length; i++) {
        const data = newParsedData[i];
        min = Math.min(min, data.l);
        max = Math.max(max, data.h);
        }
        return {min, max};
    }
    
    /**
        * @protected
        */
    calculateElementProperties(index, ruler, reset, options) {
        const me = this;
        const vscale = me._cachedMeta.vScale;
        const base = vscale.getBasePixel();
        const ipixels = me._calculateBarIndexPixels(index, ruler, options);
        const data = me.chart.data.datasets[me.index].data[index];
        const open = vscale.getPixelForValue(data.o);
        const high = vscale.getPixelForValue(data.h);
        const low = vscale.getPixelForValue(data.l);
        const close = vscale.getPixelForValue(data.c);
        const vol = vscale.getPixelForValue(data.v);
    
        return {
        base: reset ? base : low,
        x: ipixels.center,
        y: (low + high) / 2,
        width: ipixels.size,
        open,
        high,
        low,
        close,
        vol
        };
    }
    
    draw() {
        const me = this;
        const chart = me.chart;
        const rects = me._cachedMeta.data;
        helpers.clipArea(chart.ctx, chart.chartArea);
        for (let i = 0; i < rects.length; ++i) {
            rects[i].draw(me._ctx);
        }
        helpers.unclipArea(chart.ctx);
    }
    
    }
    
    /**
    * Helper function to get the bounds of the bar regardless of the orientation
    * @param {Rectangle} bar the bar
    * @param {boolean} [useFinalPosition]
    * @return {object} bounds of the bar
    * @private
    */
    function getBarBounds(bar, useFinalPosition) {
    const {x, y, base, width, height} = bar.getProps(['x', 'low', 'high', 'width', 'height'], useFinalPosition);
    
    let left, right, top, bottom, half;
    
    if (bar.horizontal) {
        half = height / 2;
        left = Math.min(x, base);
        right = Math.max(x, base);
        top = y - half;
        bottom = y + half;
    } else {
        half = width / 2;
        left = x - half;
        right = x + half;
        top = Math.min(y, base); // use min because 0 pixel at top of screen
        bottom = Math.max(y, base);
    }
    
    return {left, top, right, bottom};
    }
    
    function inRange(bar, x, y, useFinalPosition) {
    const skipX = x === null;
    const skipY = y === null;
    const bounds = !bar || (skipX && skipY) ? false : getBarBounds(bar, useFinalPosition);
    
    return bounds
            && (skipX || x >= bounds.left && x <= bounds.right)
            && (skipY || y >= bounds.top && y <= bounds.bottom);
    }
    
    class FinancialElement extends chart_js.BarElement {
    
    static defaults = {
        backgroundColors: {
        up: 'rgba(75, 192, 192, 0.5)',
        down: 'rgba(255, 99, 132, 0.5)',
        unchanged: 'rgba(201, 203, 207, 0.5)',
        },
        borderColors: {
        up: 'rgb(75, 192, 192)',
        down: 'rgb(255, 99, 132)',
        unchanged: 'rgb(201, 203, 207)',
        }
    };
    
    height() {
        return this.base - this.y;
    }
    
    inRange(mouseX, mouseY, useFinalPosition) {
        return inRange(this, mouseX, mouseY, useFinalPosition);
    }
    
    inXRange(mouseX, useFinalPosition) {
        return inRange(this, mouseX, null, useFinalPosition);
    }
    
    inYRange(mouseY, useFinalPosition) {
        return inRange(this, null, mouseY, useFinalPosition);
    }
    
    getRange(axis) {
        return axis === 'x' ? this.width / 2 : this.height / 2;
    }
    
    getCenterPoint(useFinalPosition) {
        const {x, low, high} = this.getProps(['x', 'low', 'high'], useFinalPosition);
        return {
            x,
            y: (high + low) / 2
        };
    }
    
    tooltipPosition(useFinalPosition) {
        const {x, open, close} = this.getProps(['x', 'open', 'close'], useFinalPosition);
        return {
            x,
            y: (open + close) / 2
        };
    }
    }
    
    class CandlestickElement extends FinancialElement {
        static id = 'candlestick';
        
        static defaults = {
            ...FinancialElement.defaults,
            borderWidth: 1,
        };
        
        draw(ctx) {
            const me = this;
        
            const {x, open, high, low, close, vol} = me;
        
            let borderColors = me.options.borderColors;
            if (typeof borderColors === 'string') {
                borderColors = {
                    up: borderColors,
                    down: borderColors,
                    unchanged: borderColors
                };
            }
        
            let borderColor;
            if (close < open) {
                borderColor = helpers.valueOrDefault(borderColors ? borderColors.up : undefined, chart_js.defaults.elements.candlestick.borderColors.up);
                ctx.fillStyle = helpers.valueOrDefault(me.options.backgroundColors ? me.options.backgroundColors.up : undefined, chart_js.defaults.elements.candlestick.backgroundColors.up);
            } else if (close > open) {
                borderColor = helpers.valueOrDefault(borderColors ? borderColors.down : undefined, chart_js.defaults.elements.candlestick.borderColors.down);
                ctx.fillStyle = helpers.valueOrDefault(me.options.backgroundColors ? me.options.backgroundColors.down : undefined, chart_js.defaults.elements.candlestick.backgroundColors.down);
            } else {
                borderColor = helpers.valueOrDefault(borderColors ? borderColors.unchanged : undefined, chart_js.defaults.elements.candlestick.borderColors.unchanged);
                ctx.fillStyle = helpers.valueOrDefault(me.backgroundColors ? me.backgroundColors.unchanged : undefined, chart_js.defaults.elements.candlestick.backgroundColors.unchanged);
            }
        
            ctx.lineWidth = helpers.valueOrDefault(me.options.borderWidth, chart_js.defaults.elements.candlestick.borderWidth);
            ctx.strokeStyle = borderColor;
        
            const maxWidth = 20;
            const candleWidth = Math.min(me.width, maxWidth);
        
            ctx.beginPath();
            ctx.moveTo(x, high);
            ctx.lineTo(x, Math.min(open, close));
            ctx.moveTo(x, low);
            ctx.lineTo(x, Math.max(open, close));
            ctx.stroke();
            ctx.fillRect(x - candleWidth / 2, close, candleWidth, open - close);
            ctx.strokeRect(x - candleWidth / 2, close, candleWidth, open - close);
            ctx.closePath();
        }
        
    }
    
    class CandlestickController extends FinancialController {
    
        static id = 'candlestick';
        
        static defaults = {
            ...FinancialController.defaults,
            dataElementType: CandlestickElement.id
        };
        
        static defaultRoutes = chart_js.BarController.defaultRoutes;
        
        updateElements(elements, start, count, mode) {
            const reset = mode === 'reset';
            const ruler = this._getRuler();
            const {sharedOptions, includeOptions} = this._getSharedOptions(start, mode);
        
            for (let i = start; i < start + count; i++) {
            const options = sharedOptions || this.resolveDataElementOptions(i, mode);
        
            const baseProperties = this.calculateElementProperties(i, ruler, reset, options);
        
            if (includeOptions) {
                baseProperties.options = options;
            }
            this.updateElement(elements[i], i, baseProperties, mode);
            }
        }
    
    }
    
    const defaults = chart_js.Chart.defaults;
    
    chart_js.Chart.register(CandlestickController, CandlestickElement);
    
    }));

    // randomization data (only for testing):

    var barCount = 60;
    var initialDateStr = new Date(document.getElementById('date_start').value).toUTCString();

    var ctx = document.getElementById('chart').getContext('2d');
    ctx.canvas.width = 1000;
    ctx.canvas.height = 250;

    const resolution = 20;

    var barData = new Array(barCount);
    var lineData = new Array(barCount);

    var curr_stock_sym = '(No stock was chosen yet)';

    document.getElementById('stock_sym_title').innerHTML = `<b>${curr_stock_sym}</b> Chart`;

    getRandomData(initialDateStr);



    var chart = new Chart(ctx, {
    type: 'candlestick',
    data: {
        datasets: [{
        label: curr_stock_sym+' Daily change & volume',
        data: barData,
        }, {
        label: curr_stock_sym+' Close price',
        type: 'line',
        data: lineData,
        hidden: true,
        }]
    }
    });

    function randomNumber(min, max) {
    return Math.random() * (max - min) + min;
    }

    function randomBar(target, index, date, lastClose) {
        var open = +randomNumber(lastClose * 0.95, lastClose * 1.05).toFixed(2);
        var close = +randomNumber(open * 0.95, open * 1.05).toFixed(2);
        var high = +randomNumber(Math.max(open, close), Math.max(open, close) * 1.1).toFixed(2);
        var low = +randomNumber(Math.min(open, close) * 0.9, Math.min(open, close)).toFixed(2);
        var vol = 0;

        if (!target[index]) {
            target[index] = {};
        }

        Object.assign(target[index], {
            x: date.valueOf(),
            o: open,
            h: high,
            l: low,
            c: close,
            v: vol
        });

    }

    var update = function() {

        curr_stock_sym = document.getElementById('stock_sym').value;

        document.getElementById('stock_sym_title').innerHTML = `<b>${curr_stock_sym}</b> Chart`;

        chart.config.data.datasets = [{
            label: curr_stock_sym+' Daily change & volume',
            data: barData,
            }, {
            label: curr_stock_sym + ' Close price',
            type: 'line',
            data: lineData,
            hidden: true,
        }];

        var dataset = chart.config.data.datasets[0];

        // candlestick vs ohlc
        var type = document.getElementById('type').value;
        chart.config.type = type;

        // linear vs log
        var scaleType = document.getElementById('scale-type').value;
        chart.config.options.scales.y.type = scaleType;

        // color
        var colorScheme = document.getElementById('color-scheme').value;
        if (colorScheme === 'neon') {
            chart.config.data.datasets[0].backgroundColors = {
            up: '#01ff01',
            down: '#fe0000',
            unchanged: '#999',
            };
        } else {
            delete chart.config.data.datasets[0].backgroundColors;
        }

        // border
        var border = document.getElementById('border').value;
        if (border === 'false') {
            dataset.borderColors = 'rgba(0, 0, 0, 0)';
        } else {
            delete dataset.borderColors;
        }

        // mixed charts
        chart.config.data.datasets[1].hidden = document.getElementById('mixed').value == 'true' ? false : true;
        chart.update();
    };

    [...document.getElementsByTagName('select')].forEach(element => element.addEventListener('change', update));

    function refreshStockData(new_stock_data, stock_symbol) {
        let res = JSON.parse(new_stock_data);
        let parsed_data = JSON.parse(res['data']);
        if (
            res['status'] !== 'success' || 
            !(`('Open', '${stock_symbol}')` in parsed_data) || 
            (`('Open', '${stock_symbol}')` in parsed_data && parsed_data[`('Open', '${stock_symbol}')`].length === 0)
        ) {
            console.log('Error: stock data unavailable');
        }
        else {
            // process data
            const numOfDates = Object.keys(parsed_data[`('Open', '${stock_symbol}')`]).length;
            let date_info = {};
            for (let key in parsed_data) {
                const property_name_processed = key.substring(2, key.indexOf(',') - 1); // Extract quality name (e.g., 'Open', 'Close', etc.)
                for (let date in parsed_data[key]) {
                    if (!date_info[date]) {
                        date_info[date] = {}; // Initialize the date key if it doesn't exist
                    }
                    date_info[date][property_name_processed] = parsed_data[key][date];
                }
            }
            barData = new Array(numOfDates);
            lineData = new Array(numOfDates);
            let dates = Object.keys(date_info);
            for (let i = 0; i < numOfDates; i = i + 1) {
                barData[i] = {
                    x: luxon.DateTime.fromMillis(Number(dates[i])).valueOf(),
                    o: formatNumToFixed(date_info[dates[i]]['Open'], 3),
                    h: formatNumToFixed(date_info[dates[i]]['High'], 3),
                    l: formatNumToFixed(date_info[dates[i]]['Low'], 3),
                    c: formatNumToFixed(date_info[dates[i]]['Close'], 3),
                    v: formatNumToFixed(date_info[dates[i]]['Volume'], 3)
                };
                lineData[i] = {x: barData[i].x, y: barData[i].c};
            }
            update();
        }
    }

    function is_number(s) {
        return /^\d+$/.test(s);
    }

    function normalizeValue(s, stock_currency) {
        if (is_number(s)) {  // if s is not a number, e.g. "USD", leave it untouched
            return s.toLocaleString("en-US", {style: "currency", currency: stock_currency});
        }
        return s;
    }

    function normalizeKey(s) {
        if (!s || typeof s !== "string") {
            return ""; // Handle invalid input
        }
        const spaced = s.replace(/([a-z])([A-Z])/g, "$1 $2");
        const capitalized = spaced.replace(/\b\w/g, (char) => char.toUpperCase());
        return capitalized;
    }

    function refreshCompanyInfo(stock_sym) {
        if (stock_sym !== ''){
            client.sendHttpRequest('POST', 'http://127.0.0.1:8000/get_company_info', {stock_symbol: stock_sym}, function(response) {
                let res_parsed = JSON.parse(response)['data'];
                let keys = Object.keys(res_parsed);
                let stock_currency = res_parsed['financialCurrency'];
                let relevant_keys = [['industry', 'sector', 'website', 'financialCurrency'], // each row should contain 4 keys
                                    ['previousClose', 'open', 'dayLow', 'dayHigh'],
                                    ['bid', 'ask', 'profitMargins', 'twoHundredDayAverage'],
                                    ['totalCash', 'totalCashPerShare', 'totalDebt', 'freeCashflow'],
                                    ['revenuePerShare', 'totalRevenue', 'dividendYield', 'shortRatio'],
                                    ['returnOnEquity', 'operatingMargins', 'mostRecentQuarter', '52WeekChange']];
                document.getElementById('company_info_container').innerHTML = `<h1>${res_parsed['longName']}</h2><br/> ${document.getElementById('company_info_container').innerHTML}`;
                for (let row = 0; row < relevant_keys.length; row++) {
                    document.getElementById('company_info').innerHTML += `<tr id="row_${row}"></tr>`;
                    for (let property = 0; property < relevant_keys[row].length; property++){
                        document.getElementById('row_'+row).innerHTML += `
                            <td><b><u>${normalizeKey(relevant_keys[row][property])}</u></b>:</td><td>${normalizeValue(res_parsed[relevant_keys[row][property]], stock_currency)}</td>
                        `;
                    }
                }
                document.getElementById('company_info_container').innerHTML += `<br/><br/><div>${res_parsed['longBusinessSummary']}</div>`;
            });
        }
        else {
            console.log("Can't retrieve company info: stock symbol is not valid.");
        }
    }

    function getRandomData(dateStr) {
        var date = luxon.DateTime.fromRFC2822(dateStr);

        for (let i = 0; i < barData.length;) {
            date = date.plus({days: 1});
            if (date.weekday <= 5) {
                randomBar(barData, i, date, i === 0 ? 30 : barData[i - 1].c);
                lineData[i] = {x: barData[i].x, y: barData[i].c};
                i++;
            }
        }
    }
    function getTodaysDateStr() {  // formatted: YYYY-MM-DD
        var today = new Date();
        return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    }
    function subtractDaysFromToday(daysToSubtract) {
        Date.prototype.subtractDays = function (d) {
            this.setDate(this.getDate() - d);
            return this;
        }
        return new Date().subtractDays(daysToSubtract).toISOString().split('T')[0];
    }
    function autoDate(days_ago) {
        let sym = document.getElementById('stock_sym').value;
        let date_start = document.getElementById('date_start');
        let date_end = document.getElementById('date_end');
        let all_data = false;
        // TO-DO: fix "Today"-button's bug.
        if (days_ago != '1826') {
            date_start.value = subtractDaysFromToday(Number(days_ago));
        }
        else if (days_ago === '0') {
            date_start.value = getTodaysDateStr();
        }
        else {
            all_data = true; 
        }
        date_end.value = getTodaysDateStr();
        if (sym !== '') {
            const data = {
                stock_symbol: sym,
                from_date: all_data ? 'ALL' : date_start.value,
                to_date: date_end.value
            };
            client.sendHttpRequest('POST', 'http://127.0.0.1:8000/get_stock_data', data, function(response) {
                refreshStockData(response, sym);
            });
        } else {
            alert('Error: No stock symbol input');
        }
    }

