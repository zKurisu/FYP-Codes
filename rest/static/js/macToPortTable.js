export function drawMacToPortTable(macToPortItems) {
  console.debug("Draw mac to port table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Mac To Port Table";
  div.appendChild(title);

  // 遍历每个 outer key (dpid)
  for (const dpid in macToPortItems) {
    // 创建 dpid Box 容器
    console.debug(`DPID: ${dpid}`)
    const dpidBox = document.createElement("div");
    dpidBox.classList.add("dpid-box");

    // 添加 dpid 标题
    const dpidHeader = document.createElement("h3");
    dpidHeader.textContent = `Datapath ID: ${dpid}`;
    dpidBox.appendChild(dpidHeader);

    // 创建表格
    const table = document.createElement("table");

    // 添加表头
    const headerRow = table.insertRow();
    const header1 = headerRow.insertCell();
    header1.textContent = "Mac";
    const header2 = headerRow.insertCell();
    header2.textContent = "Port";

    // 添加表格内容
    for (const mac in macToPortItems[dpid]) {
        const row = table.insertRow();
        const cell1 = row.insertCell();
        cell1.textContent = mac;
        const cell2 = row.insertCell();
        cell2.textContent = macToPortItems[dpid][mac];
    }

    // 将表格添加到 dpid Box 中
    dpidBox.appendChild(table);

    // 将 dpid Box 添加到容器中
    div.appendChild(dpidBox);
  }

  console.debug("Return drawed mac to port table");
  return div
}
