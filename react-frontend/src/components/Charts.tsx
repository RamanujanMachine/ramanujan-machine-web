import axios from 'axios';
import React from 'react';
import { CategoryScale, Chart, Legend, LinearScale, LineElement, PointElement } from 'chart.js';
import { Line } from 'react-chartjs-2';

const chartOptions = {
	responsive: true,
	plugins: {
		legend: {
			position: 'top' as const
		},
		title: {
			display: true,
			text: 'Line Chart'
		}
	}
};

const range = (start: number, end: number, step: number, length: number = (end - start) / step) =>
	Array.from({ length }, (_, i) => start + i * step);

interface ChartProps {
	results: any;
	toggleDisplay: () => void;
}

const labels: { [key: string]: string } = {
	log_reduced_denominator: 'log of denominator',
	log_error: 'log of error',
	delta: 'error delta'
};

Chart.register(CategoryScale, Legend, LinearScale, LineElement, PointElement);

function Charts({ results = {}, toggleDisplay }: ChartProps) {
	const computePairs = (dataset: string) => { 
		checkResult();
		return {
			labels: range(0, 5000, 100),
			datasets: [
				{
					label: labels[dataset],
					data: JSON.parse(results[dataset]),
					borderColor: '#f9ae33',
					backgroundColor: '#f9ae33',
					pointRadius: 0
				}
			]
		};
	};
	const checkResult = function() {
	axios.post('http://localhost:8000/verify', {expression: results.expression})
			.then((response) => {
				if (response.status != 200) {
					console.warn(response.data.error);
				}
			})
			.catch((error) => console.log(error));
		}
	return (
		<div className="chart-container">
			<p>This is the value of the Polynomial Continued Fraction:<br/><br/>{JSON.parse(results.limit)}</p>
			<p>It seems to converge to:<br/><br/>{JSON.parse(results.converges_to)}</p>
			<i>
				<sub>
					Note: the limit is estimated to high confidence using a PSLQ algorithm, but this is not a
					proof.
				</sub>
			</i>
			<p>The rate of convergence for this Polynomial Continued Fraction (in digits per step): </p>
			<Line datasetIdKey="id" data={computePairs('log_error')} options={chartOptions} />
			<p>
				Delta is a measure of the irrationality of a number (read more about it{' '}
				<a href="https://www.ramanujanmachine.com/the-mathematics-of-polynomial-continued-fractions/irrationality-testing/">
					here
				</a>
				). The given Polynomial Continued Fraction produces the following finite-depth estimations
				for Delta:
			</p>
			<Line datasetIdKey="id" data={computePairs('delta')} options={chartOptions} />
			<button
				onClick={() => {
					toggleDisplay();
				}}>
				Modify
			</button>
		</div>
	);
}

export default Charts;
