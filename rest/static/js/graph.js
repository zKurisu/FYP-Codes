export function drawGraph(node_list, edge_list) {
  console.debug("Draw graph begin");
  
  // 创建容器
  const container = document.createElement('div');
  const fatherContainer = document.getElementsByClassName("content-display-box")[0];
  const fatherRect = fatherContainer.getBoundingClientRect();
  container.classList.add("topology-graph");
  container.style.width = `${fatherRect.width}px`;
  container.style.height = "800px";
  
  const title = document.createElement('h1');
  title.textContent = "Network Topology";
  title.style.textAlign = "center";
  title.style.marginBottom = "20px";
  title.style.color = "#2c3e50";
  container.appendChild(title);

  // 创建图表区域
  const graphContainer = document.createElement('div');
  graphContainer.style.width = '100%';
  graphContainer.style.height = 'calc(100% - 60px)';
  graphContainer.style.border = "1px solid #e0e0e0";
  graphContainer.style.borderRadius = "8px";
  graphContainer.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";
  container.appendChild(graphContainer);

  // 转换节点数据格式（显示最后3位）
  const ap_list = node_list.filter(node => (! node.startsWith("00")))
  const visNodes = ap_list.map(node => ({
    id: node, // 保持原始ID用于内部引用
    label: node.slice(-3), // 只显示最后3位
    color: {
      border: "#2c3e50",
      background: "#3498db",
      highlight: {
        border: "#2c3e50",
        background: "#2980b9"
      },
      hover: {
        border: "#2c3e50",
        background: "#2980b9"
      }
    },
    font: { 
      color: "#fff",
      size: 14,
      face: "Arial",
      strokeWidth: 3,
      strokeColor: "#2c3e50"
    },
    borderWidth: 2,
    shape: "circle",
    size: 24,
    shadow: {
      enabled: true,
      color: "rgba(0,0,0,0.3)",
      size: 10,
      x: 5,
      y: 5
    },
    // 添加完整ID作为悬停提示
    title: `Full ID: ${node}`
  }));

  // 转换边数据格式（所有连接都是双向的）
  const uniqueEdges = new Set();
  const visEdges = [];
  
  edge_list.forEach(edge => {
    // 标准化边标识（避免重复创建双向边）
    const sortedNodes = [edge[0], edge[1]].sort();
    const edgeKey = `${sortedNodes[0]}-${sortedNodes[1]}`;
    
    if (!uniqueEdges.has(edgeKey)) {
      visEdges.push({
        from: edge[0], // 使用原始ID
        to: edge[1],   // 使用原始ID
        arrows: {
          to: { enabled: true, scaleFactor: 0.6 },
          from: { enabled: true, scaleFactor: 0.6 }
        },
        color: {
          color: "#7f8c8d",
          highlight: "#e74c3c",
          hover: "#e74c3c"
        },
        width: 2,
        smooth: {
          type: "horizontal"
        },
        selectionWidth: 3,
        shadow: {
          enabled: true,
          color: "rgba(0,0,0,0.2)",
          size: 5,
          x: 3,
          y: 3
        }
      });
      
      uniqueEdges.add(edgeKey);
    }
  });

  // 创建网络图（其余代码保持不变...）
  const data = { nodes: visNodes, edges: visEdges };
  const options = {
    physics: {
      enabled: true,
      solver: "forceAtlas2Based",
      forceAtlas2Based: {
        gravitationalConstant: -50,
        centralGravity: 0.01,
        springLength: 200,
        springConstant: 0.08,
        damping: 0.4
      }
    },
    nodes: {
      shapeProperties: {
        interpolation: false
      }
    },
    edges: {
      arrowStrikethrough: false,
      chosen: true
    },
    interaction: {
      hover: true,
      tooltipDelay: 200,
      hideEdgesOnDrag: false,
      multiselect: true
    },
    layout: {
      improvedLayout: true
    },
    configure: {
      enabled: false
    },
    height: '100%',
    width: '100%'
  };

  if (typeof vis !== 'undefined') {
    const network = new vis.Network(graphContainer, data, options);
    
    window.addEventListener('resize', () => {
      network.redraw();
      network.fit();
    });
    
    setTimeout(() => {
      network.fit({
        animation: {
          duration: 1000,
          easingFunction: 'easeInOutQuad'
        }
      });
    }, 500);
  } else {
    console.error("Vis.js not loaded!");
    const errorMsg = document.createElement('div');
    errorMsg.textContent = "图表库加载失败，请刷新重试";
    errorMsg.style.color = "#e74c3c";
    errorMsg.style.textAlign = "center";
    errorMsg.style.padding = "20px";
    graphContainer.appendChild(errorMsg);
  }

  console.debug("Return drawed graph");
  return container;
}
