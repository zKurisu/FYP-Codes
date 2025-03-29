export function drawMacToPortTable(macToPortItems) {
  console.debug("Draw mac to port table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Mac To Port Table";
  div.appendChild(title);

  // 遍历每个 outer key (dpid)
  for (const dpid in macToPortItems) {
    // 创建 dpid Box 容器
    console.debug(`DPID: ${dpid}`);
    const dpidBox = document.createElement("div");
    dpidBox.classList.add("dpid-box");

    // 添加 dpid 标题
    const dpidHeader = document.createElement("h3");
    dpidHeader.textContent = `Datapath ID: ${dpid}`;
    dpidBox.appendChild(dpidHeader);

    // 创建表格
    const table = document.createElement("table");
    
    // 创建表头部分
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    
    // 添加表头单元格
    const headers = ["MAC Address", "Port Number"];
    headers.forEach(headerText => {
      const th = document.createElement("th");
      th.textContent = headerText;
      headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // 创建表格内容
    const tbody = document.createElement("tbody");
    
    // 添加表格内容
    for (const mac in macToPortItems[dpid]) {
      const row = document.createElement("tr");
      
      const cell1 = document.createElement("td");
      cell1.textContent = mac;
      row.appendChild(cell1);
      
      const cell2 = document.createElement("td");
      cell2.textContent = macToPortItems[dpid][mac];
      row.appendChild(cell2);
      
      tbody.appendChild(row);
    }
    
    table.appendChild(tbody);
    dpidBox.appendChild(table);
    div.appendChild(dpidBox);
  }

  console.debug("Return drawed mac to port table");
  return div;
}
