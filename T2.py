from collections import deque, defaultdict

def bfs(graph, start):
    
    visited = set()                  
    queue = deque([start])           
    visit_order = []                 
    
    visited.add(start)               
    
    while queue:                    
        node = queue.popleft()       
        visit_order.append(node)     
        
        
        for neighbor in graph[node]:
            if neighbor not in visited:   
                visited.add(neighbor)
                queue.append(neighbor)    
    
    return visit_order


graph = defaultdict(list)
edges = [('A','B'), ('A','C'), ('B','D'), ('C','D'), ('C','E')]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)   


result = bfs(graph, 'A')
print("BFS starting from A:", result)