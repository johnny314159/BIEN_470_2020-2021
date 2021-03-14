import React from "react";

function AboutData({ data }) {

  return (
      <div>
         <h1>How do I interpret these results?</h1>
         <br/>
         There are a lot of numbers flying around in PhyloPGM, so here's what they mean, and why they're important to your prediction.
         <h3>The initial likelihood ratio on the human sequence was {data[0].toFixed(3)}.</h3>
         <h3>By introducing the prediction scores from orthologous sequences, PhyloPGM added {data[1].toFixed(3)} (with α=0.1), for 
            a combined final score of {data[2].toFixed(3)}.
          </h3>
          Although the likelihood ratios are not the same as the prediction scores output by the machine learning algorithm, they are proportional.
          A <b>positive</b> likelihood ratio indicates a "true" label; the input sequence is predicted to be an RNA-binding site.
          A <b>negative</b> likelihood ratio indicates a "false" label; the input sequence is not predicted to be an RNA-binding site.

          <h1>About the data visualization</h1>
          On both charts, red represents negative values and blue represents positive values.
          <br/> <br/> 
          The bar chart displays the likelihood ratio of the root (human sequence), the sum of the branches' likelihood ratios multiplied by α, and the sum of the two.
          If the middle bar is the same colour as the left bar, the orthologous sequences reinforced the original label. 
          If it is a different colour, the orthologous sequences then propose more uncertainty in the original label, or in extreme cases, might even flip it entirely.
          <br/> <br/> 
          The tree chart displays the individual likelihood ratios of all extant and ancestral species that have been identified as orthologous sequences.
          The <b>opacity of the branch</b> is proportional to the magnitude of the ratio.
          The <b>size of the nodes</b> is proportional to the original prediction score of its respective sequence; a red hollow node indicates the lack of a prediction score on that species.
          <b> Dashed branches</b> indicate a likelihood ratio of 0, which happens when the branch essentially adds no value to the model. 
      </div>
  );
}

export default AboutData;
