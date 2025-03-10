// 渲染 MAC 到端口表
function renderMacToPortTable(macToPortItems) {
    const container = document.getElementById("tables-container");

    // 清空容器
    container.innerHTML = "";

    // 遍历每个 outer key (dpid)
    for (const dpid in macToPortItems) {
        // 创建 dpid Box 容器
        const dpidBox = document.createElement("div");
        dpidBox.classList.add("dpid-box");

        // 添加 dpid 标题
        const dpidHeader = document.createElement("h3");
        dpidHeader.textContent = `Datapath ID: ${dpid}`;
        dpidBox.appendChild(dpidHeader);

        // 创建表格
        const table = document.createElement("table");

        // 添加表头
        const headerRow = table.insertRow();
        const header1 = headerRow.insertCell();
        header1.textContent = "Mac";
        const header2 = headerRow.insertCell();
        header2.textContent = "Port";

        // 添加表格内容
        for (const mac in macToPortItems[dpid]) {
            const row = table.insertRow();
            const cell1 = row.insertCell();
            cell1.textContent = mac;
            const cell2 = row.insertCell();
            cell2.textContent = macToPortItems[dpid][mac];
        }

        // 将表格添加到 dpid Box 中
        dpidBox.appendChild(table);

        // 将 dpid Box 添加到容器中
        container.appendChild(dpidBox);
    }
}

// 从服务器获取数据
function fetchMacToPortItems() {
    fetch('/api/mac_to_port-items')
        .then(response => response.json())
        .then(data => {
            renderMacToPortTable(data);
        })
        .catch(error => console.error('Error fetching MAC to port items:', error));
}

// 每 5 秒轮询一次
setInterval(fetchMacToPortItems, 5000);

// 初始加载
fetchMacToPortItems();
