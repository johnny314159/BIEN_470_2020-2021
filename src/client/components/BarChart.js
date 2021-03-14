import React, { useRef, useEffect, useState } from "react";
import { select, axisBottom, axisRight, scaleLinear, scaleBand } from 'd3';

function BarChart({ data }) {
  const svgRef = useRef();
  
  const numerical_data = data.map(x => parseFloat(x));
  const absolute_data = numerical_data.map(x => Math.abs(x));

  // check if a value is positive or negative
  const isPositive = number => number > 0;

  console.log();
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

    console.log(xScale[0]);
    const yScale = scaleLinear()
                    .domain([0, Math.ceil(Math.max(...absolute_data))])
                    .range([150, 0]);


    const xAxis = axisBottom(xScale).ticks(absolute_data.length);
    const xAxisNames = axisBottom(xScaleNames);

    svg
        .select(".x-axis")
        .style("transform", "translateY(100%)")
        .call(xAxisNames);
    
    const yAxis = axisRight(yScale);

    svg
        .select(".y-axis")
        .style("transform", "translateX(300px)")
        .call(yAxis);

    svg
        .selectAll(".bar")
        .data(absolute_data)
        .join("rect")
        .attr("class", "bar")
        .attr("fill", (value, index) => (isPositive(numerical_data[index])) ? "#57bdc3" : "#C35D57")
        .attr("x", (value, index) => xScale(index))
        .attr("y", yScale)
        .attr("width", xScale.bandwidth())
        .attr("height", value => 150 - yScale(value));

}, [data]);

  return (
      <svg ref={svgRef} >
        <g className="x-axis" />
        <g className="y-axis" />
      </svg>
  );
}

export default BarChart;
