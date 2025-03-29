export function drawFlowTable(total_flow_entities) {
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
  
  const idHeader = document.createElement('th');
  idHeader.textContent = 'ID';
  
  const entitiesHeader = document.createElement('th');
  entitiesHeader.textContent = 'Flow Entities';
  
  headerRow.appendChild(idHeader);
  headerRow.appendChild(entitiesHeader);
  thead.appendChild(headerRow);
  table.appendChild(thead);
  
  // 创建表格内容
  const tbody = document.createElement('tbody');
  
  // 遍历数据
  for (const [id, entities] of Object.entries(total_flow_entities)) {
    const row = document.createElement('tr');
    
    // ID 单元格
    const idCell = document.createElement('td');
    idCell.textContent = id;
    
    // Entities 单元格
    const entitiesCell = document.createElement('td');
    
    // 创建无序列表显示实体
    const list = document.createElement('ul');
    entities.forEach(entity => {
      const item = document.createElement('li');
      item.textContent = entity;
      list.appendChild(item);
    });
    
    entitiesCell.appendChild(list);
    row.appendChild(idCell);
    row.appendChild(entitiesCell);
    tbody.appendChild(row);
  }
  
  table.appendChild(tbody);
  div.appendChild(table);

  console.debug("Return drawed flow table");
  return div;
}
