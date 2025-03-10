import math
import random
from collections import deque
from mcds.find_MCDS import find_mcds, draw_graph

def generate_connected_udg(
    n: int,               # 节点数量 (必须 >=1)
    signal_range: float,  # 信号范围
    width: float = 100.0,   # 区域宽度 (默认单位正方形)
    height: float = 100.0,  # 区域高度
    max_attempts: int = 1000,  # 单个节点的最大生成尝试次数
    seed: int|None = None      # 随机种子 (可选)
) -> tuple[dict, dict]:
    """
    生成保证连通的随机 Unit Disk Graph
    返回:
        - nodes_dict: {id: (x, y)} 格式的节点位置字典
        - adjacency_dict: 邻接表字典 {id: [邻居列表]}
    注意:
        若无法生成满足条件的图，抛出 ValueError
    """
    if n < 1:
        raise ValueError("节点数量必须 >=1")
    if seed is not None:
        random.seed(seed)
    
    nodes_dict = {}
    adjacency_dict = {}
    
    # 生成第一个节点
    nodes_dict[1] = (random.uniform(0, width), random.uniform(0, height))
    adjacency_dict[1] = []
    
    # 逐步生成后续节点，确保每个新节点至少连接到一个已有节点
    for node_id in range(2, n+1):
        attempts = 0
        while attempts < max_attempts:
            # 随机生成候选位置
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            
            # 检查是否与至少一个已有节点在信号范围内
            connected = False
            for existing_id, (ex, ey) in nodes_dict.items():
                dx = x - ex
                dy = y - ey
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= signal_range:
                    connected = True
                    break
            
            if connected:
                # 添加新节点
                nodes_dict[node_id] = (x, y)
                adjacency_dict[node_id] = []
                # 更新邻接表
                for existing_id, (ex, ey) in nodes_dict.items():
                    if existing_id == node_id:
                        continue
                    dx = x - ex
                    dy = y - ey
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance <= signal_range:
                        adjacency_dict[node_id].append(existing_id)
                        adjacency_dict[existing_id].append(node_id)
                break  # 成功生成，退出循环
            
            attempts += 1
        else:
            raise ValueError(f"无法在 {max_attempts} 次尝试内生成节点 {node_id}。请增大 signal_range 或区域尺寸。")
    
    # 最终验证连通性 (可选，理论上冗余但安全)
    if not is_connected(adjacency_dict):
        raise ValueError("生成图不连通，请检查算法逻辑。")
    dpid_nodes_dict = {}
    for k in nodes_dict.keys():
        dpid = 10**15 + k
        dpid_nodes_dict[dpid] = nodes_dict[k]
    
    return dpid_nodes_dict, adjacency_dict


def is_connected(adjacency: dict) -> bool:
    """验证图是否连通"""
    if not adjacency:
        return True  # 空图视为连通
    visited = set()
    start_node = next(iter(adjacency.keys()))
    queue = deque([start_node])
    visited.add(start_node)
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited) == len(adjacency)
