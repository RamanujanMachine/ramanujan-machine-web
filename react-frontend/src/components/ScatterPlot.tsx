import React, { useEffect } from 'react';
import * as d3 from 'd3';
import { CoordinatePair } from '../lib/types';

const svg_width = 860,
	svg_height = 400;

const ScatterPlot = ({ id, data }: { id: string; data?: CoordinatePair[] }) => {
	useEffect(() => {
		if (data && data.length > 0) {

			try {
				const filteredData = data.filter((point) => !isNaN(parseFloat(point.y)));

				// select and clear DOM container
				const svg = d3.select(`#${id}`);
				svg.selectAll('*').remove();

				var margin = 20,
					width = svg_width,
					height = svg_height;
				svg.style('overflow', 'visible').style('background', '#ffffff');
				var plot = svg
					.append('g')
					.attr('width', width - margin)
					.attr('height', height - margin);

				const [minX, maxX] = d3.extent(filteredData, (d) => {
					return d.x;
				});

				const xScale = d3
					.scaleLinear()
					.domain([minX!, maxX!])
					.range([0, width - margin]);

				const [minY, maxY] = d3.extent(filteredData, (d) => parseFloat(d.y));

				const yScale = d3
					.scaleLinear()
					.domain([minY!, maxY!])
					.range([height - margin, 0]);

				// x axis
				const xAxis = svg.append('g').call(d3.axisBottom(xScale));
				xAxis.attr('transform', `translate(0,${height - margin})`);

				// y axis
				const yAxis = svg.append('g').call(d3.axisLeft(yScale));
				yAxis.attr('transform', `translate(0,0)`);

				plot
					.selectAll('dot')
					.data(filteredData)
					.enter()
					.append('circle')
					.attr('cx', function (d) {
						return xScale(d.x);
					})
					.attr('cy', function (d) {
						return yScale(parseFloat(d.y));
					})
					.attr('r', 1.5)
					.style('fill', 'var(--accent)');
			} catch(e) { 
				console.log('Failed to render d3 chart', e);
			}
		}
	}, [data]);

	return data && data.length > 0 ? (
		<svg width={svg_width} height={svg_height} id={id}>
			<g></g>
		</svg>
	) : (
		<div className="chart-spinner-container">
			<div className="chart-spinner"></div>
		</div>
	);
};

export default ScatterPlot;
