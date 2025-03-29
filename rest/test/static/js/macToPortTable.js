export function drawMacToPortTable(total_mac_to_port) {
  console.debug("Draw mac to port table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Mac To Port Table";
  div.appendChild(title);

  console.debug("Return drawed mac to port table");
  return div
}
