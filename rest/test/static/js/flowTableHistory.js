export function drawFlowTableHistory(flowData) {
  console.debug("Draw flow table history begin");
  const div = document.createElement('div');
  const title = document.createElement('h1');
  title.textContent = "Flow Table History";
  div.appendChild(title);

  // Process each switch's flows separately
  Object.entries(flowData).forEach(([dpid, flows]) => {
    // Create heading for each switch
    const dpidTitle = document.createElement('h3');
    dpidTitle.textContent = `Switch ${dpid}`;
    div.appendChild(dpidTitle);

    // Create table for current switch
    const table = document.createElement('table');
    
    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    
    // Define table headers (removed 'Switch ID' since it's in the title)
    const headers = [
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
      headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create table body
    const tbody = document.createElement('tbody');
    
    // Process flows for current switch
    flows.forEach(flow => {
      const row = document.createElement('tr');
      
      // Extract output port from instructions
      let outputPort = 'N/A';
      try {
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

      // Prepare cell data (removed datapath_id since it's in the title)
      const cells = [
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
        row.appendChild(td);
      });
      
      tbody.appendChild(row);
    });
    
    table.appendChild(tbody);
    div.appendChild(table);

    // Add separator between switches
    const separator = document.createElement('hr');
    div.appendChild(separator);
  });

  console.debug("Return drawn flow table history");
  return div;
}
