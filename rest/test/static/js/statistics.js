export function drawStatisticsTable(total_statistics) {
  console.debug("Draw statistics table begin");
  
  // 创建容器
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Statistics Table";
  div.appendChild(title);

  // 创建表格
  const table = document.createElement('table');
  table.style.width = '100%';
  table.style.borderCollapse = 'collapse';
  table.style.marginTop = '20px';
  
  // 创建表头
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  
  // 添加表头列
  const headers = [
    'Switch ID', 'Port', 'RX Packets', 'RX Bytes', 'RX Errors',
    'TX Packets', 'TX Bytes', 'TX Errors'
  ];
  
  headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    th.style.border = '1px solid #ddd';
    th.style.padding = '8px';
    th.style.textAlign = 'left';
    th.style.backgroundColor = '#f2f2f2';
    headerRow.appendChild(th);
  });
  
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // 创建表格内容
  const tbody = document.createElement('tbody');
  
  // 遍历统计数据
  total_statistics.forEach(switchData => {
    switchData.statistics.forEach(portStats => {
      const row = document.createElement('tr');
      
      // 添加单元格数据
      const cells = [
        switchData.dpid,
        portStats.port_no,
        portStats.rx_packets,
        portStats.rx_bytes,
        portStats.rx_errors,
        portStats.tx_packets,
        portStats.tx_bytes,
        portStats.tx_errors
      ];
      
      cells.forEach(cellData => {
        const td = document.createElement('td');
        td.textContent = cellData;
        td.style.border = '1px solid #ddd';
        td.style.padding = '8px';
        row.appendChild(td);
      });
      
      tbody.appendChild(row);
    });
  });
  
  table.appendChild(tbody);
  div.appendChild(table);

  console.debug("Return drawed statistics table");
  return div;
}
