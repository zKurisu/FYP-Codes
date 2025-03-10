function renderFlowTable(flowItems) {
    const groupedFlows = {};
    const flowTable = document.getElementById("flow-table");

    // 清空流表容器
    flowTable.innerHTML = "";  // 确保每次渲染前清空内容

    // 按 dpid 分组
    flowItems.forEach(item => {
        const dpid = item.datapath_id;
        if (!groupedFlows[dpid]) {
            groupedFlows[dpid] = [];
        }
        groupedFlows[dpid].push(item);
    });

    // 创建 dpid Box 容器
    for (const dpid in groupedFlows) {
        const dpidBox = document.createElement("div");
        dpidBox.classList.add("dpid-box");

        const dpidHeader = document.createElement("h3");
        dpidHeader.textContent = `Datapath ID: ${dpid}`;
        dpidBox.appendChild(dpidHeader);

        groupedFlows[dpid].forEach(item => {
            const flowItem = document.createElement("div");
            flowItem.classList.add("flow-item", item.command?.toLowerCase() || "default");

            // 显示必填字段
            let content = `
                <strong>Priority:</strong> ${item.priority}, <br>
                <strong>Match:</strong> ${item.match}, <br>
                <strong>Instructions:</strong> ${item.instructions}, 
            `;

            // 显示可选字段（如果存在）
            if (item.buffer_id !== null && item.buffer_id !== undefined) {
                content += `<br><strong>Buffer ID:</strong> ${item.buffer_id}, `;
            }
            if (item.command) {
                content += `<br><strong>Command:</strong> ${item.command}, `;
            }
            if (item.idle_timeout !== null && item.idle_timeout !== undefined) {
                content += `<br><strong>Idle Timeout:</strong> ${item.idle_timeout}, `;
            }
            if (item.hard_timeout !== null && item.hard_timeout !== undefined) {
                content += `<br><strong>Hard Timeout:</strong> ${item.hard_timeout}, `;
            }
            if (item.cookie !== null && item.cookie !== undefined) {
                content += `<br><strong>Cookie:</strong> ${item.cookie}, `;
            }
            if (item.flags !== null && item.flags !== undefined) {
                content += `<br><strong>Flags:</strong> ${item.flags}`;
            }

            flowItem.innerHTML = content;
            dpidBox.appendChild(flowItem);
        });

        flowTable.appendChild(dpidBox);
    }
}

function fetchFlowItems() {
    fetch('/api/flow-items')
        .then(response => response.json())
        .then(data => {
            renderFlowTable(data);
        })
        .catch(error => console.error('Error fetching flow items:', error));
}

// 每 5 秒轮询一次
setInterval(fetchFlowItems, 5000);

// 初始加载
fetchFlowItems();
