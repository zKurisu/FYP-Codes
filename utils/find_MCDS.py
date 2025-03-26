import networkx as nx
import matplotlib.pyplot as plt

def find_mcds(nodes_dict, signal_range):
    # 构建邻接表
    adj = get_adjacency(nodes_dict, signal_range)
    # 初始化颜色和集合
    color = {id: 'white' for id in nodes_dict}
    mcds = []
    
    # 初始节点选择：度数最大且ID最小
    white_nodes = [id for id in nodes_dict if color[id] == 'white']
    sorted_nodes = sorted(white_nodes, key=lambda x: (-len(adj[x]), x))
    selected = sorted_nodes[0]
    mcds.append(selected)
    color[selected] = 'black'
    for n in adj[selected]:
        if color[n] == 'white':
            color[n] = 'gray'
    
    # 迭代阶段
    while any(c == 'white' for c in color.values()):
        gray_nodes = [id for id, c in color.items() if c == 'gray']
        if not gray_nodes:
            break
        
        # 仅考虑与当前 MCDS 连通的灰色节点
        connected_gray = []
        for node in gray_nodes:
            if any(neighbor in mcds for neighbor in adj[node]):
                connected_gray.append(node)
        
        # 如果没有连通灰色节点，强制选择桥梁节点（需处理非连通图）
        # if not connected_gray:
        #     connected_gray = gray_nodes  # 假设图是连通的，此处简化处理
        
        # 排序依据：覆盖的白色邻居数 → 度数 → ID
        sorted_gray = sorted(
            connected_gray,
            key=lambda x: (-sum(1 for n in adj[x] if color[n] == 'white'), -len(adj[x]), x)
        )
        selected = sorted_gray[0]
        mcds.append(selected)
        color[selected] = 'black'
        for n in adj[selected]:
            if color[n] == 'white':
                color[n] = 'gray'
    
    return mcds, adj

def draw_graph(nodes_dict, adj, mcds=None, title="Graph"):
    G = nx.Graph()
    # 添加节点和边
    for node, pos in nodes_dict.items():
        G.add_node(node, pos=pos)
    for node, neighbors in adj.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    pos = nx.get_node_attributes(G, 'pos')
    # 绘制
    plt.figure(figsize=(10, 8))
    node_colors = ['red' if node in mcds else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=12, font_weight='bold')
    plt.title(title)
    plt.show()

def get_adjacency(nodes_dict, signal_range):
    # 构建邻接表
    adj = {id: [] for id in nodes_dict}
    ids = list(nodes_dict.keys())
    n = len(ids)
    for i in range(n):
        id1 = ids[i]
        x1, y1 = nodes_dict[id1]
        for j in range(i + 1, n):
            id2 = ids[j]
            x2, y2 = nodes_dict[id2]
            distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
            if distance <= signal_range:
                print(f"Distance is {distance}")
                adj[id1].append(id2)
                adj[id2].append(id1)
    return adj

