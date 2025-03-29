export function drawPortInfoTable(total_port_infos) {
  console.debug("Draw port info table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Port Info Table";
  div.appendChild(title);

  // 遍历每个交换机
  for (const dpid in total_port_infos) {
    // 创建交换机容器
    const apBox = document.createElement("div");
    apBox.classList.add("portInfo-ap-box");

    // 添加交换机标题
    const apHeader = document.createElement("h3");
    apHeader.textContent = `AP: ${dpid}`;
    apBox.appendChild(apHeader);

    // 创建表格
    const table = document.createElement("table");
    
    // 创建表头部分
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    
    // 添加表头单元格
    const headers = ["Interface", "MAC Address", "Port Number"];
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
    for (const info of total_port_infos[dpid]) {
      const row = document.createElement("tr");
      
      const cell1 = document.createElement("td");
      cell1.textContent = info.port_name;
      row.appendChild(cell1);
      
      const cell2 = document.createElement("td");
      cell2.textContent = info.mac;
      row.appendChild(cell2);
      
      const cell3 = document.createElement("td");
      cell3.textContent = info.port_no;
      row.appendChild(cell3);
      
      tbody.appendChild(row);
    }
    
    table.appendChild(tbody);
    apBox.appendChild(table);
    div.appendChild(apBox);
  }

  console.debug("Return drawed port info table");
  return div;
}
