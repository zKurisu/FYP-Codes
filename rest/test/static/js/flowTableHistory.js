export function drawFlowTableHistory(flowData) {
  console.debug("Draw flow table history begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Flow Table History";
  div.appendChild(title);

  // Create table
  const table = document.createElement('table');
  table.style.width = '100%';
  table.style.borderCollapse = 'collapse';
  
  // Create table header
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  
  // Define table headers
  const headers = [
    'Switch ID',
    'Priority',
    'Match Fields',
    'Output Port',
    'Command',
    'Idle Timeout',
    'Hard Timeout'
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
  
  // Create table body
  const tbody = document.createElement('tbody');
  
  // Process each switch's flows
  Object.entries(flowData).forEach(([dpid, flows]) => {
    flows.forEach(flow => {
      const row = document.createElement('tr');
      
      // Extract output port from instructions
      let outputPort = 'N/A';
      try {
        // Simple extraction of port number from the instructions string
        const portMatch = flow.instructions.match(/port=(\d+)/);
        if (portMatch) {
          outputPort = portMatch[1];
          // Convert special port numbers to meaningful names
          if (outputPort === '4294967293') outputPort = 'CONTROLLER';
          else if (outputPort === '4294967294') outputPort = 'TABLE';
          else if (outputPort === '4294967295') outputPort = 'IN_PORT';
        }
      } catch (e) {
        console.warn("Couldn't parse instructions:", flow.instructions);
      }

      // Prepare cell data
      const cells = [
        flow.datapath_id || dpid,
        flow.priority ?? '0',
        flow.match ? flow.match.replace(/OFPMatch$|$/g, '') : 'None',
        outputPort,
        flow.command ?? 'N/A',
        flow.idle_timeout ?? '∞',
        flow.hard_timeout ?? '∞'
      ];
      
      // Create cells
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

  console.debug("Return drawn flow table history");
  return div;
}
