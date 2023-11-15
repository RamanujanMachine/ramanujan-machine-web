import React from 'react';
import './App.css';
import Form from './components/Form';

function App() {
	return (
		<div className="app-root">
			<div className="header">
				The Ramanujan Machine
				<div className="subheading">using algorithms to discover new mathematics</div>
			</div>
			<div className="body">
				<Form></Form>
				<div className="link">
					<a href="https://www.ramanujanmachine.com/">Ramanujan Machine Home</a>
				</div>
			</div>
		</div>
	);
}

export default App;
