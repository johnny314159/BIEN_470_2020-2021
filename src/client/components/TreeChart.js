import React, { useRef, useEffect } from "react";
import { select, hierarchy, tree, linkHorizontal } from "d3";
import useResizeObserver from "./useResizeObserver";


function TreeChart({ data }) {
  const svgRef = useRef();
  const wrapperRef = useRef();
  const dimensions = useResizeObserver(wrapperRef);

  // check if a string is upper case
  const isUpperCase = str => str === str.toUpperCase();


  // will be called initially and on every data change
  useEffect(() => {
    const svg = select(svgRef.current);
    if (!dimensions) return;

    const root = hierarchy(data);
    const treeLayout = tree().size([4*dimensions.height, 0.9*dimensions.width]);
    treeLayout(root);

    const linkGenerator = linkHorizontal()
                              .x(node => node.y)
                              .y(node => node.x);


      // render links
      svg
        .selectAll(".link")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("d", linkGenerator)
        .attr("fill", "none")
        .attr("stroke", "#57bdc3");

      // render nodes


      // render labels
      svg
        .selectAll(".label")
        .data(root.descendants())
        .join(enter => enter.append("text").attr("opacity", 1))
        .attr("class", "label")
        .attr("x", node => node.y)
        .attr("y", node => node.x)
        .attr("dy", "0.32em")
        .attr("text-anchor", node => node.children ? 'end': 'start')
        .attr("font-size", 12)
        .text(node => isUpperCase(node.data.name) ? '' : node.data.name)



    // I basically need to resize it and I'm good? for now
    // and also fix the marks it leaves when you actively resize it...


}, [data, dimensions]);

  return (
    <div ref={wrapperRef} style={{ marginBottom: "2rem", marginLeft: "4rem" }}>
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default TreeChart;
