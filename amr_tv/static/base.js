const selectedAdjacencyMatrixCells = {};

$.ajax({
  url: "transmission-events/",
  success: (data) => {
    $("#adjacency-matrix-spinner-container").hide();

    for (const organismGroup of data.organismGroupsList) {
      selectedAdjacencyMatrixCells[organismGroup] = {};
    }

    renderAdjacencyMatrix(data.organismGroupsList);
  },
});

const renderAdjacencyMatrix = (organismGroupsList) => {
  $.ajax({
    url: "adjacency-matrix/",
    data: {"data": JSON.stringify(organismGroupsList)},
    success: (data) => {
      $("#adjacency-matrix-plot").html(data);
    },
  });
};

$("#node-link-diagram-create-btn").click(() => {
  renderNodeLinkDiagram(selectedAdjacencyMatrixCells);
});

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
  const y = data.target._hoverdata[0].y
  const xHasY = selectedAdjacencyMatrixCells[x].hasOwnProperty(y)
  const yHasX = selectedAdjacencyMatrixCells[y].hasOwnProperty(x)

  if (xHasY) {
    delete selectedAdjacencyMatrixCells[x][y];
  } else {
    selectedAdjacencyMatrixCells[x][y] = null;
  }

  if (x !== y) {
    if (yHasX) {
      delete selectedAdjacencyMatrixCells[y][x];
    } else {
      selectedAdjacencyMatrixCells[y][x] = null;
    }
  }
});

$("#node-link-diagram-plot").on("plotly_click", (data) => {
  const customData = data.target._hoverdata[0].customdata;
  $.ajax({
    url: "node-detail-table/",
    data: customData,
    success: (data) => {
      $("#node-detail-organism-group").text(data.organismGroup);
      $("#node-detail-amr-genotypes").text(data.amrGenotypes);
      $("#node-detail-table-plot").html(data.plotDiv);
    },
  });
});
