import React, { useEffect } from 'react';
import * as d3 from 'd3';

type CoordinatePair = {
    x: number,
    y: string
};

const ScatterPlot = ({ id, data }:{id:string, data: CoordinatePair[]}) =>  {
    
    useEffect(() => {
        if (data && data.length > 0) {
            const filteredData = data.filter(point => !isNaN(parseFloat(point.y)))
            for(let datum of filteredData){
                console.debug(id, datum.x, datum.y, parseFloat(datum.y), isNaN(parseFloat(datum.y)));
            }
            // select and clear DOM container
            const svg = d3.select(`#${id}`);
            svg.selectAll('*').remove();   

            var v_margin = 20, h_margin = 20,
            width = 580 - h_margin,
            height = 400 - v_margin;
            svg.style("overflow", "visible")
            .style("background", "#ffffff");
            svg.append("g").attr("width", width + 5*h_margin)
            svg.append("g").attr("height", height + 5*v_margin)
            .attr("transform", `translate(${h_margin}, ${v_margin})`);
            
            const [minX, maxX] = d3.extent(filteredData, (d) => {return d.x;});
            console.debug(`x min ${minX} x max ${maxX}`);

            const xScale = d3
            .scaleLinear()
            .domain([minX!, maxX!])
            .range([0, width - h_margin]);
        
            const [minY, maxY] = d3.extent(filteredData, (d) => parseFloat(d.y));
            console.debug(`y min ${minY} y max ${maxY}`);
        
            const yScale = d3
            .scaleLinear()
            .domain([minY!, maxY!])
            .range([height -v_margin, 0]);
            
            // x axis
            const xAxis = svg.append("g")
                .call(d3.axisTop(xScale));
            xAxis.attr("transform",`translate(${h_margin},${v_margin})`);
              
            // y axis
            const yAxis = svg.append("g")
                .call(d3.axisLeft(yScale));
            yAxis.attr("transform",`translate(${h_margin},${v_margin})`);

            const line = d3
            .line<CoordinatePair>()
            .x((d) => xScale(d.x))
            .y((d) => yScale(parseFloat(d.y))).curve(d3.curveBasis);

            svg.append('g')
            .selectAll("dot")
            .data(filteredData)
            .enter()
            .append("circle")
              .attr("cx", function (d) { return xScale(d.x); } )
              .attr("cy", function (d) { return yScale(parseFloat(d.y)); } )
              .attr("r", 1.5)
              .attr("transform", `translate(${h_margin}, ${v_margin})`)
              .style("fill", "var(--accent)");

              svg
            .data([filteredData])
            .append('path')
            .attr('d', line)
            .attr("transform", `translate(${h_margin}, ${v_margin})`)
            .attr("fill", "none")
            .attr("stroke-dasharray", "2 2")
            .attr("stroke-opacity", "0.6")
            .attr("stroke-width", "2")
            .attr("stroke", "var(--muted)");

        }
    }, [data]);

return <svg width={560} height={360} id={id} >
    <g></g>
</svg>;
};

export default ScatterPlot;