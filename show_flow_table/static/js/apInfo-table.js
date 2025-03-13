function renderAPInfoTable(apInfo) {
    const container = document.getElementById("tables-container");

    // 清空容器
    container.innerHTML = "";

    // 遍历每个 outer key
    for (const apName in apInfo) {
        // 创建 ap Box 容器
        const apBox = document.createElement("div");
        apBox.classList.add("ap-box");

        // 添加 ap 标题
        const apHeader = document.createElement("h3");
        apHeader.textContent = `AP: ${apName}`;
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
        for (const info of apInfo[apName]) {
            const row = table.insertRow();
            const cell1 = row.insertCell();
            cell1.textContent = info.name;
            const cell2 = row.insertCell();
            cell2.textContent = info.mac;
            const cell3 = row.insertCell();
            cell3.textContent = info.port;
        }

        // 将表格添加到 ap Box 中
        apBox.appendChild(table);

        // 将 ap Box 添加到容器中
        container.appendChild(apBox);
    }
}

