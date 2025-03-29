export function drawFlowTable(total_flow_entities) {
  console.debug("Draw flow table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Flow Table";
  div.appendChild(title);

  console.debug("Return drawed flow table");
  return div
}
