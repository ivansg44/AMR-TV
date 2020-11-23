$.ajax({
  url: "adjacency-matrix/",
  success: (data) => {
    $("#adjacency-matrix-spinner-container").hide();
    $("#adjacency-matrix-plot").html(data);
  }
})

$.ajax({
  url: "node-link-diagram/",
  success: (data) => {
    $("#node-link-diagram-plot").html(data);
  }
})
