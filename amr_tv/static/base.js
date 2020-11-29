const selectedAdjacencyMatrixCells = {
  // Stub organism group specifications
  "Enterobacter": {"Salmonella enterica": null},
  "Salmonella enterica": {"Enterobacter": null},
};

$.ajax({
  url: "transmission-events/",
  success: () => {
    $("#adjacency-matrix-spinner-container").hide();
    renderAdjacencyMatrix();
    renderNodeLinkDiagram(selectedAdjacencyMatrixCells);
  },
});

const renderAdjacencyMatrix = () => {
  $.ajax({
    url: "adjacency-matrix/",
    success: (data) => {
      $("#adjacency-matrix-plot").html(data);
    },
  });
};

const renderNodeLinkDiagram = (selectedAdjacencyMatrixCells) => {
  $.ajax({
    url: "node-link-diagram/",
    data: {"data": JSON.stringify(selectedAdjacencyMatrixCells)},
    success: (data) => {
      $("#node-link-diagram-plot").html(data);
    },
  });
};

$("#adjacency-matrix-plot").on("plotly_click", (data) => {
  const x = data.target._hoverdata[0].x;
  const y = data.target._hoverdata[0].y;
  return;
});

$("#node-link-diagram-plot").on("plotly_click", (data) => {
  const customData = data.target._hoverdata[0].customdata;
  $.ajax({
    url: "node-detail-table/",
    data: customData,
    success: (data) => {
      $("#node-detail-organism-group").text(data.organismGroup)
      $("#node-detail-amr-genotypes").text(data.amrGenotypes)
      $("#node-detail-table-plot").html(data.plotDiv);
    },
  });
});
