import React, { useEffect } from 'react';
import * as d3 from 'd3';
import { CoordinatePair } from '../lib/types';

const WIDTH = 580;
const HEIGHT = 400;

const ScatterPlot = ({ id, data }:{id:string, data: CoordinatePair[]}) =>  {
    
    const fit = function(x:number): number{
        const ix = data.findIndex((entry) => entry.x == x);
        if(ix-1 >=0){
            return ((parseFloat(data[ix].y) + parseFloat(data[ix-1].y))/2.0);
        } else return NaN;
    }

    useEffect(() => {
        if (data && data.length > 0) {
            const filteredData = data.filter(point => !isNaN(parseFloat(point.y)) && isFinite(parseFloat(point.y)));
            // select and clear DOM container
            const svg = d3.select(`#${id}`);
            svg.selectAll('*').remove();   

            var width = WIDTH,
                height = HEIGHT;
            svg.style("overflow", "visible")
                .style("background", "#ffffff");
            svg.append("g").attr("width", width).attr("height", height)
                .attr("transform", `translate(0, 0)`);
            
            const [minX, maxX] = d3.extent(filteredData, (d) => {return d.x;});
            console.debug(`x min ${minX} x max ${maxX}`);

            const xScale = d3
                .scaleLinear()
                .domain([minX!, maxX!])
                .range([0, width]);
        
            const [minY, maxY] = d3.extent(filteredData, (d) => parseFloat(d.y));
            console.debug(`y min ${minY} y max ${maxY}`);
        
            const yScale = d3
                .scaleLinear()
                .domain([minY!, maxY!])
                .range([height, 0]);
            
            // x axis
            const xAxis = svg.append("g")
                .call(d3.axisBottom(xScale));
            xAxis.attr("transform",`translate(${0},${height})`);
              
            // y axis
            const yAxis = svg.append("g")
                .call(d3.axisLeft(yScale));
            yAxis.attr("transform",`translate(${0},${0})`);

            const line = d3
                .line<CoordinatePair>()
                .x((d) => xScale((d.x + d.x-1)/2))
                .y((d) => yScale(fit(d.x)))
                .defined((d) => !isNaN(fit(d.x)))
                .curve(d3.curveBasis);

            svg.append('g')
                .selectAll("dot")
                .data(filteredData)
                .enter()
                .append("circle")
                .attr("cx", function (d) { return xScale(d.x); } )
                .attr("cy", function (d) { return yScale(parseFloat(d.y)); } )
                .attr("r", 1.5)
                .attr("transform", `translate(0, 0)`)
                .style("fill", "var(--accent)");

            svg
                .data([filteredData])
                .append('path')
                .attr('d', line)
                .attr("transform", `translate(0, 0)`)
                .attr("fill", "none")
                .attr("stroke-dasharray", "3 3")
                .attr("stroke-opacity", "0.5")
                .attr("stroke-width", "1")
                .attr("stroke", "var(--muted)");

        }
    }, [data]);

    return <svg width={WIDTH} height={HEIGHT} id={id} >
        <g></g>
    </svg>;
};

export default ScatterPlot;