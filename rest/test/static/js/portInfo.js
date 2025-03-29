export function drawPortInfoTable(total_port_infos) {
  console.debug("Draw port info table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Port Info Table";
  div.appendChild(title);

  console.debug("Return drawed port info table");
  return div
}
