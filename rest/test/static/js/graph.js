export function drawGraph(node_list, edge_list) {
  console.debug("Draw graph begin");
  
  // 创建容器
  const container = document.createElement('div');
  container.style.width = '800px';
  container.style.height = '600px';
  container.style.border = '1px solid #ccc';
  
  const title = document.createElement('h1');
  title.textContent = "Graph";
  container.appendChild(title);

  // 创建图表区域
  const graphContainer = document.createElement('div');
  graphContainer.style.width = '100%';
  graphContainer.style.height = 'calc(100% - 40px)';
  container.appendChild(graphContainer);

  // 转换节点数据格式
  const visNodes = node_list.map((node, index) => ({
    id: node,
    label: node,
    color: index === 0 ? "#FF5733" : "#2ECC71",
  }));

  // 转换边数据格式（适配Python的元组结构）
  const visEdges = edge_list.map(edge => ({
    from: edge[0],  // 第一个元素是src
    to: edge[1],    // 第二个元素是dst
    arrows: "to",
  }));

  // 创建网络图
  const data = { nodes: visNodes, edges: visEdges };
  const options = {
    physics: { enabled: true },
    height: '100%',
    width: '100%'
  };

  // 确保vis已全局可用
  if (typeof vis !== 'undefined') {
    new vis.Network(graphContainer, data, options);
  } else {
    console.error("Vis.js not loaded!");
    const errorMsg = document.createElement('div');
    errorMsg.textContent = "图表库加载失败";
    graphContainer.appendChild(errorMsg);
  }

  console.debug("Return drawed graph");
  return container;
}
