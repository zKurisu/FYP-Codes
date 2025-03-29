export function drawGraph(nodes, edges) {
  console.debug("Draw graph begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Graph";
  div.appendChild(title);

  console.debug("Return drawed graph");
  return div
}
