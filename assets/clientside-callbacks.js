/**
 * @fileoverview This file stores callbacks that are performed clientside.
 */

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    /**
     * TODO
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

      // Remove the active class, and let the return value make it active. There
      // seems to be more to fully activating tabs than just changing classes.
      document.getElementById('main-graph-tab').classList.remove('active');

      return ['main-graph-tab', null];
    }
  }
});
