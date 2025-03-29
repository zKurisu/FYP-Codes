export function drawFlowTableCurrent(total_flow_entities) {
  console.debug("Draw flow table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Flow Table";
  div.appendChild(title);

  // 创建表格
  const table = document.createElement('table');
  
  // 创建表头
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  
  // 添加详细表头
  const headers = [
    'Switch ID', 
    'In Port', 
    'Ethernet Destination',
    'Out Port',
    'Packet Count',
    'Byte Count'
  ];
  
  headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    headerRow.appendChild(th);
  });
  
  thead.appendChild(headerRow);
  table.appendChild(thead);
  
  // 创建表格内容
  const tbody = document.createElement('tbody');
  
  // 遍历数据
  Object.entries(total_flow_entities).forEach(([dpid, flows]) => {
    flows.forEach(flow => {
      const row = document.createElement('tr');
      
      // 添加单元格数据
      const cells = [
        dpid,
        flow.in_port || 0,
        flow.eth_dst || '00:00:00:00:00:00',
        flow.out_port || 0,
        flow.packet_count || 0,
        flow.byte_count || 0
      ];
      
      cells.forEach(cellData => {
        const td = document.createElement('td');
        td.textContent = cellData;
        row.appendChild(td);
      });
      
      tbody.appendChild(row);
    });
  });
  
  table.appendChild(tbody);
  div.appendChild(table);

  console.debug("Return drawed flow table");
  return div;
}
