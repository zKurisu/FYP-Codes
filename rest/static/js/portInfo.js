export function drawPortInfoTable(total_port_infos) {
  console.debug("Draw port info table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Port Info Table";
  div.appendChild(title);

  // 遍历每个 outer key
  for (const dpid in total_port_infos) {
      // 创建 ap Box 容器
      const apBox = document.createElement("div");
      apBox.classList.add("portInfo-ap-box");

      // 添加 ap 标题
      const apHeader = document.createElement("h3");
      apHeader.textContent = `AP: ${dpid}`;
      apBox.appendChild(apHeader);

      // 创建表格
      const table = document.createElement("table");

      // 添加表头
      const headerRow = table.insertRow();
      const header1 = headerRow.insertCell();
      header1.textContent = "Intfs";
      const header2 = headerRow.insertCell();
      header2.textContent = "Mac";
      const header3 = headerRow.insertCell();
      header3.textContent = "Port";

      // 添加表格内容
      for (const info of total_port_infos[dpid]) {
          const row = table.insertRow();
          const cell1 = row.insertCell();
          cell1.textContent = info.port_name;
          const cell2 = row.insertCell();
          cell2.textContent = info.mac;
          const cell3 = row.insertCell();
          cell3.textContent = info.port_no;
      }

      // 将表格添加到 ap Box 中
      apBox.appendChild(table);

      // 将 ap Box 添加到容器中
      div.appendChild(apBox);
  }

  console.debug("Return drawed port info table");

  return div
}
