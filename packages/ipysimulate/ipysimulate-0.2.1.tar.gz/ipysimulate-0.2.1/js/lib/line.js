var widgets = require('@jupyter-widgets/base');
var semver_range = require('../package.json').version;
var d3 = require('d3');
require('./charts.css');
require('lodash');


var LinechartModel = widgets.DOMWidgetModel.extend({

    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'LinechartModel',
        _view_name : 'LinechartView',
        _model_module : 'ipysimulate',
        _view_module : 'ipysimulate',
        _model_module_version : semver_range,
        _view_module_version : semver_range,
    }),

	initialize: function (attributes, options) {
        widgets.DOMWidgetModel.prototype
			.initialize.call(this, attributes, options);
		this.on('msg:custom', this._on_msg.bind(this));

        // Initialize data
		this.xlabel = this.get('xlabel');
		this.ylabels = this.get('ylabels');
		this.reset_data()
    },

	_on_msg: function (command, buffers) {
        if (command.what) {
            switch (command.what) {
                case 'new_data':
                    this.update(command.data);
                    break;
                case 'reset_data':
                    this.reset();
                    break;
            }
        }
    },

	update: function(new_data) {
		// Append new data
		this.data.x.push(new_data.x)
		for (const [key, value] of Object.entries(new_data.series)) {
			this.series[key].push(value)
		}
		// Send updated data to all views
		this.update_views()
	},

	reset: function() {
    	this.reset_data() // Clear data
		this.update_views()
	},

	update_views: function() {
		for (var key in this.views) { // Send cleared data to all views
			this.views[key].then(this._update_view.bind(null, this.data))
		}
	},

	_update_view: function(data, view) {
    	view.update(data)
	},

	reset_data: function () {
		this.data = {'x': [], 'series': []};
		this.series = {}
		var i;
		for (i = 0; i < this.ylabels.length; i++) {
			let label = this.ylabels[i]
			let series_entry = {'name': label, 'values': []}
			this.data.series.push(series_entry)
			this.series[label] = series_entry.values
		}
	},

});


var LinechartView = widgets.DOMWidgetView.extend({

    // Render view --------------------------------------------------------- //
    render: function() {

		// Create output area ---------------------------------------------- //

        this.container = document.createElement("div");
        this.container.className = 'ipysimulate-chart'
        this.el.appendChild(this.container);

		var width = 500;
		var height = 300;
		var margin = {top: 20, right: 30, bottom: 40, left: 40}

		var svg = d3.select(this.container).append("svg")
			.attr("style", "width: 100%; height: 100%")
			.attr("viewBox", [0, 0, width, height])
			.append("g");

		var x = d3.scaleLinear().range([margin.left, width - margin.right]);
		var y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

		// Axis ------------------------------------------------ //

		var xAxis = d3.axisBottom().scale(x);
		var yAxis = d3.axisLeft().scale(y);

		svg.append("g")
		  .attr("transform", `translate(0,${height - margin.bottom})`)
		  .attr("class","myXaxis")
		svg.append("g")
		  .attr("transform", `translate(${margin.left},0)`)
		  .attr("class","myYaxis")

		// Axis Labels
		svg.append("text")
		    .attr("class", "chart-label")
		    .attr("text-anchor", "middle")
		    .attr("x", margin.left + (width - margin.right - margin.left)/2 )
		    .attr("y", height - 5)
		    .text(this.model.xlabel);

		// Content --------------------------------------------------------- //

		// Color scale
		var color = d3.scaleOrdinal()
		  .domain(d3.range(0, this.model.data.series.length, 1))
		  .range(d3.schemeSet2);

		// Path collection (g)
		var paths = svg.append("g")
	      .attr("fill", "none")
	      .attr("stroke-width", 1.5)

		// Path objects
	    paths.selectAll("path")
		    .data(this.model.data.series)
		    .join("path")
		    .attr("stroke", (d, i) => color(i))


		// Legend --------------------------------------------------------- //

		// Add one dot in the legend for each name.
		svg.selectAll("mydots")
		  .data(this.model.data.series)
		  .enter()
		  .append("circle")
		    .attr("cx", width - margin.right - 5)
		    .attr("cy", function(d, i){ return margin.top + i*25})
		    .attr("r", 7)
		    .style("stroke", 'white')
		    .style("fill", function(d, i){ return color(i)})

		// Add one dot in the legend for each name.
		svg.selectAll("mylabels")
		  .data(this.model.data.series)
		  .enter()
		  .append("text")
		    .attr("class", "chart-label")
		    .attr("x", width - margin.right - 17)
		    .attr("y", function(d, i){ return margin.top + i*25 + 4.5})
		    .text(function(d){ return d.name})
		    .attr("text-anchor", "end")

		// References --------------------------------------------------------- //
		this.paths = paths
		this.svg = svg
		this.x = x
		this.y = y
		this.xAxis = xAxis
		this.yAxis = yAxis

	},

	update: function (data) {

    	// Create a update selection: bind to the new data
		var x = this.x
		var y = this.y

		// Line function TODO Move out of update
    	var line = d3.line()
			//.defined(d => !isNaN(d)) // TODO What does this do?
			.x((d, i) => x(data.x[i]))
			.y(d => y(d))

		// Update scale
		// TODO Update by comparing only new value
		x.domain(d3.extent(data.x));
		y.domain([d3.min(data.series, d => d3.min(d.values)),
				  d3.max(data.series, d => d3.max(d.values)) ]);

		// Update paths
		this.paths
			.selectAll("path")
		    .data(data.series)
			.attr("d", d => line(d.values));

		// Update axis
		this.svg.selectAll(".myXaxis")
			.transition()
			.duration(100)
			.call(this.xAxis);
		this.svg.selectAll(".myYaxis")
			.transition()
			.duration(100)
			.call(this.yAxis);

		},

});

module.exports = {
    LinechartModel: LinechartModel,
    LinechartView: LinechartView,
};




