$.ajax({
  url: "transmission-events/",
  success: () => {
    $("#adjacency-matrix-spinner-container").hide();
    render_adjacency_matrix();
    render_node_link_diagram();
  },
});

const render_adjacency_matrix = () => {
  $.ajax({
    url: "adjacency-matrix/",
    success: (data) => {
      $("#adjacency-matrix-plot").html(data);
    },
  });
};

const render_node_link_diagram = () => {
  $.ajax({
    url: "node-link-diagram/",
    data: {
      // Stub organism group specifications
      "Enterobacter": ["Salmonella enterica"],
      "Salmonella enterica": ["Enterobacter"],
    },
    success: (data) => {
      $("#node-link-diagram-plot").html(data);
    },
  });
};

$("#node-link-diagram-plot").on("plotly_click", function(data) {
  const customData = data.target._hoverdata[0].customdata;
  return;
});
