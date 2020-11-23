$.ajax({
  url: "adjacency-matrix/",
  success: (data) => {
    $("#adjacency-matrix-spinner-container").hide();
    $("#adjacency-matrix-plot").html(data);
  }
})
