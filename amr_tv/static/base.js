let dateRange = [];
const selectedAdjacencyMatrixCells = {};

const loadTransmissionEvents = () => {
  return $.ajax({
    url: "transmission-events/",
    data: {"date_range": JSON.stringify(dateRange)},
  });
};

const renderAdjacencyMatrix = () => {
  $.ajax({
    url: "adjacency-matrix/",
    data: {"organism_groups_list": JSON.stringify(organismGroupsArr)},
    success: (data) => {
      $("#adjacency-matrix-plot").html(data);
      $("#node-link-diagram-plot").empty();
      $(".node-detail-text-div").hide();
      $("#node-detail-table-plot").empty();
      $("#loading-spinner").hide();
    },
  });
};

const updateSelectedAdjacencyMatrixCells = (x, y, pointIndex) => {
  const xHasY = selectedAdjacencyMatrixCells[x].hasOwnProperty(y)
  const yHasX = selectedAdjacencyMatrixCells[y].hasOwnProperty(x)

  if (xHasY) {
    delete selectedAdjacencyMatrixCells[x][y];
  } else {
    selectedAdjacencyMatrixCells[x][y] = pointIndex;
  }

  if (x !== y) {
    if (yHasX) {
      delete selectedAdjacencyMatrixCells[y][x];
    } else {
      selectedAdjacencyMatrixCells[y][x] = [pointIndex[1], pointIndex[0]];
    }
  }
};

const renderNodeLinkDiagram = () => {
  $.ajax({
    url: "node-link-diagram/",
    data: {"selected_events": JSON.stringify(selectedAdjacencyMatrixCells)},
    success: (data) => {
      $("#node-link-diagram-plot").html(data);
      $(".node-detail-text-div").hide();
      $("#node-detail-table-plot").empty();
      $("#loading-spinner").hide();
    },
  });
};

$(document).ready(() => {
  $("#adjacency-matrix-create-btn").click(async () => {
    $("#loading-spinner").show();

    const startDate = $("#start-date-input").val();
    const endDate = $("#end-date-input").val();
    dateRange = [startDate, endDate];

    await loadTransmissionEvents();

    for (const organismGroup of organismGroupsArr) {
      selectedAdjacencyMatrixCells[organismGroup] = {};
    }

    renderAdjacencyMatrix();
  }).click();

  $("#adjacency-matrix-plot").on("plotly_click", (data) => {
    $("#loading-spinner").show();

    const pointIndex = data.target._hoverdata[0].pointIndex;
    const x = data.target._hoverdata[0].x;
    const y = data.target._hoverdata[0].y
    updateSelectedAdjacencyMatrixCells(x, y, pointIndex);

    $.ajax({
      url: "adjacency-matrix/highlighted/",
      data: {"selected_cells": JSON.stringify(selectedAdjacencyMatrixCells)},
      success: (data) => {
        $("#adjacency-matrix-plot").html(data);
        $("#loading-spinner").hide();
      },
    });
  });

  $("#node-link-diagram-create-btn").click(() => {
    $("#loading-spinner").show();
    renderNodeLinkDiagram();
  });

  $("#node-link-diagram-plot").on("plotly_click", (data) => {
    $("#loading-spinner").show();

    const customData = data.target._hoverdata[0].customdata;
    customData["date_range"] = dateRange;
    customData["organism_groups"] = organismGroupsArr;
    $.ajax({
      url: "node-detail-table/",
      data: {"data": JSON.stringify(customData)},
      success: (data) => {
        $("#node-detail-organism-group").text(data.organismGroup);
        $("#node-detail-amr-genotypes").text(data.amrGenotypes);
        $("#node-detail-table-plot").html(data.plotDiv);

        $("#loading-spinner").hide();
        $(".node-detail-text-div").show();
        document.getElementById('node-detail-table-plot').scrollIntoView();
      },
    });
  });
});
