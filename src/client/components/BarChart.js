import React, { useRef, useEffect, useState } from "react";
import { select, axisBottom, axisRight, scaleLinear, scaleBand, min, max } from 'd3';

function BarChart({ data }) {
  const svgRef = useRef();
  
  const numerical_data = data.map(x => parseFloat(x));
  const absolute_data = numerical_data.map(x => Math.abs(x));

  // check if a value is positive or negative
  const isPositive = number => number > 0;

  // will be called initially and on every data change
  useEffect(() => {
    const svg = select(svgRef.current);
    const xScale = scaleBand()
                    .domain(absolute_data.map((value, index) => index))
                    .range([0, 300])
                    .padding(0.5);
    
    const xScaleNames = scaleBand()
                    .domain(["Before", "PhyloPGM", "After"])
                    .range([0, 300])
                    .padding(0.5);



    function findHeight() {
        // The goal of this function is to adapt the range of the bar height scale to that of the axis
        // It basically does the same math as scaleLinear below
        const domain = max([1.1*max(numerical_data), 0]) - min([1.1*min(numerical_data), 0]);
        const range = 250;
        console.log(domain);
        return range/domain;
        

    }

    // Instead of *1.1, should I do floor or ceiling?
    const yScale = scaleLinear()
                    .domain([min([1.1*min(numerical_data), 0]), max([1.1*max(numerical_data), 0])])
                    .range([250, 0]);


    // zero represents the y-location (from the top, in pixels) of the 0 on the y-axis
    const zero = yScale(0);

    //const xAxis = axisBottom(xScale).ticks(absolute_data.length);
    const xAxisNames = axisBottom(xScaleNames);


    const yAxis = axisRight(yScale);

    svg
        .select(".y-axis")
        .style("transform", "translateX(100%)")
        .call(yAxis);

    svg
        .selectAll(".bar")
        .data(numerical_data)
        .join("rect")
        .attr("class", "bar")
        .attr("fill", (value, index) => (isPositive(numerical_data[index])) ? "#C35D57" : "#57bdc3")
        .attr("x", (value, index) => xScale(index))
        .attr("y", value => isPositive(value) ? zero - Math.abs(value)*findHeight() : zero) //
        .attr("width", xScale.bandwidth())
        .attr("height", (value) => Math.abs(value)*findHeight()); //

    svg
        .select(".x-axis")
        .style("transform", "translateY(" + zero + "px)")
        .call(xAxisNames)
        .raise();





}, [data]);

  return (
      <svg ref={svgRef} className="bar-chart" >
        <g className="x-axis" />
        <g className="y-axis" />
      </svg>
  );
}

export default BarChart;
