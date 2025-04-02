export function drawFlowTableCurrent(totalFlowEntities) {
  console.debug("Draw flow table begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Flow Table";
  div.appendChild(title);

  // 遍历每个交换机
  Object.entries(totalFlowEntities).forEach(([dpid, flows]) => {
    // 为每个交换机创建标题
    const dpidTitle = document.createElement('h3');
    dpidTitle.textContent = `Switch ${dpid}`;
    div.appendChild(dpidTitle);

    // 创建表格
    const table = document.createElement('table');
    
    // 创建表头
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // 添加详细表头
    const headers = [
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
    
    // 遍历当前交换机的流表
    flows.forEach(flow => {
      const row = document.createElement('tr');
      
      // 添加单元格数据
      const cells = [
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
    
    table.appendChild(tbody);
    div.appendChild(table);

    // 添加分隔线
    const separator = document.createElement('hr');
    div.appendChild(separator);
  });

  console.debug("Return drawed flow table");
  return div;
}
