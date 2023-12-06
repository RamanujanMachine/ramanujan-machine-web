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

interface ChartProps {
	results: number[];
	toggleDisplay: () => void;
}

Chart.register(CategoryScale, Legend, LinearScale, LineElement, PointElement);
function Charts({ results = [], toggleDisplay }: ChartProps) {
	const computePairs = () => {
		return {
			labels: results,
			datasets: [
				{
					label: 'dataset name',
					data: results,
					borderColor: '#f9ae33',
					backgroundColor: '#f9ae33',
					pointRadius: 0
				}
			]
		};
	};
	return (
		<div className="chart-container">
			<Line datasetIdKey="id" data={computePairs()} options={chartOptions} />
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
