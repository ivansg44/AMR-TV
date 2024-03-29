/**
 * @fileoverview This file stores callbacks that are performed clientside.
 */

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    /**
     * Switch to main graph, and scroll to corresponding node, after
     * user clicks node in zoomed-out main graph.
     * @param {Object} clickData Plotly object containing info on last node
     *     clicked in zoomed-out main graph.
     * @return {Array.<?string>} The id of the main graph tab, which is made
     *     active, and a null value, which is used to reset the last node
     *     clicked.
     */
    scrollToNode: (clickData) => {
      const mainGraph = document.getElementById('main-graph');
      const mainGraphPoints = mainGraph.getElementsByClassName('point');
      const clickedPoint = clickData['points'][0]['pointIndex'];

      // We need to add the active class to the main graph tab, otherwise
      // ``scrollIntoView`` does not work.
      document.getElementById('main-graph-tab').classList.add('active');

      const scrollIntoViewOptions = {'block': 'center', 'inline': 'center'}
      mainGraphPoints[clickedPoint].scrollIntoView(scrollIntoViewOptions);

      // We need to also scroll the axes. It is a bit convoluted, because
      // scrolling the axes will scroll the main graph some more.
      // First some important divs
      const mainGraphCol = document.getElementById('main-graph-col')
      const mainGraphXAxisCol = document.getElementById('main-graph-x-axis-col')
      const mainGraphYAxisCol = document.getElementById('main-graph-y-axis-col')
      // Get scroll left and top vals for main graph after we scrolled clicked
      // node into view.
      const mainGraphScrollLeft = mainGraphCol.scrollLeft
      const mainGraphScrollTop = mainGraphCol.scrollTop
      // Reset main graph scroll position to current axis positions
      mainGraphCol.scrollLeft = mainGraphXAxisCol.scrollLeft
      mainGraphCol.scrollTop = mainGraphYAxisCol.scrollTop
      // Now scroll everything to where it should be
      mainGraphCol.scrollLeft = mainGraphScrollLeft
      mainGraphCol.scrollTop = mainGraphScrollTop
      mainGraphXAxisCol.scrollLeft = mainGraphScrollLeft
      mainGraphYAxisCol.scrollTop = mainGraphScrollTop

      // Remove the active class, and let the return value make it active. There
      // seems to be more to fully activating tabs than just changing classes.
      document.getElementById('main-graph-tab').classList.remove('active');

      return ['main-graph-tab', null];
    },
    /**
     * Add event handlers to the main graph axes figs, to sync scrolling b/w
     * the main graph and its axes.
     * @param _ Main graph fig was updated.
     * @return {boolean} Hidden browser var; only used b/c we need an output.
     */
    addMainVizScrollHandlers: (_) => {
      const mainGraphColEl = document.getElementById('main-graph-col');
      const mainGraphXAxisColEl =
          document.getElementById('main-graph-x-axis-col');
      const mainGraphYAxisColEl =
          document.getElementById('main-graph-y-axis-col');
      mainGraphXAxisColEl.addEventListener(
          'scroll',
          ()=> {
            const scrollLeft = mainGraphXAxisColEl.scrollLeft;
            const scrollTop = mainGraphYAxisColEl.scrollTop;
            mainGraphColEl.scroll(scrollLeft, scrollTop);
          }
      );
      mainGraphYAxisColEl.addEventListener(
          'scroll',
          ()=> {
            const scrollLeft = mainGraphXAxisColEl.scrollLeft;
            const scrollTop = mainGraphYAxisColEl.scrollTop;
            mainGraphColEl.scroll(scrollLeft, scrollTop);
          }
      );
      return true;
    }
  }
});
