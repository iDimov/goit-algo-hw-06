import networkx as nx

class MetroNetwork:
    def __init__(self):
        # Створюємо неорієнтований граф
        self.G = nx.Graph()
        
    def create_metro_network(self):
        """Створення мережі метро"""
        line1 = [
            'Академмістечко', 'Житомирська', 'Святошин', 'Нивки', 'Берестейська', 'Шулявська',
            'Політехнічний інститут', 'Вокзальна', 'Університет', 'Театральна', 'Хрещатик',
            'Арсенальна', 'Дніпро', 'Гідропарк', 'Лівобережна', 'Дарниця', 'Чернігівська', 'Лісова'
        ]

        line2 = [
            'Героїв Дніпра', 'Мінська', 'Оболонь', 'Почайна', 'Тараса Шевченка', 'Контрактова площа',
            'Поштова площа', 'Майдан Незалежності', 'Площа Українських Героїв', 'Олімпійська',
            'Палац "Україна"', 'Либідська', 'Деміївська', 'Голосіївська', 'Васильківська',
            'Виставковий центр', 'Іподром', 'Теремки'
        ]

        line3 = [
            'Сирець', 'Дорогожичі', 'Лук’янівська', 'Золоті Ворота', 'Палац Спорту', 'Кловська',
            'Печерська', 'Звіринецька', 'Видубичі', 'Славутич', 'Осокорки', 'Позняки', 'Харківська',
            'Вирлиця', 'Бориспільська', 'Червоний хутір'
        ]
        
        # Додаємо ребра з вагами для кожної лінії
        self._add_line_edges(line1)
        self._add_line_edges(line2)
        self._add_line_edges(line3)
        
        # Додаємо пересадки між лініями з вагою 5 (час на пересадку)
        self.G.add_edge('Майдан Незалежності', 'Золоті Ворота', weight=5)
        self.G.add_edge('Площа Українських Героїв', 'Палац Спорту', weight=5)
        self.G.add_edge('Театральна', 'Золоті Ворота', weight=5)
    
    def _add_line_edges(self, stations):
        """Додає ребра між послідовними станціями з вагами"""
        for i in range(len(stations) - 1):
            self.G.add_edge(stations[i], stations[i + 1], weight=3)
    
    def analyze_network(self):
        """Аналіз основних характеристик мережі"""
        print("\nАналіз мережі метро:")
        print(f"Кількість станцій: {self.G.number_of_nodes()}")
        print(f"Кількість з'єднань: {self.G.number_of_edges()}")
        print("\nСтупені станцій (кількість з'єднань):")
        for node, degree in self.G.degree():
            print(f"{node}: {degree}")
    
    def dfs_path(self, start, end, path=None, visited=None):
        """Пошук шляху методом DFS"""
        if visited is None:
            visited = set()
        if path is None:
            path = []
            
        path.append(start)
        visited.add(start)
        
        if start == end:
            return path
            
        for neighbor in self.G.neighbors(start):
            if neighbor not in visited:
                new_path = self.dfs_path(neighbor, end, path[:], visited)
                if new_path:
                    return new_path
        return None
    
    def bfs_path(self, start, end):
        """Пошук шляху методом BFS"""
        if start not in self.G or end not in self.G:
            return None
            
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            vertex, path = queue.pop(0)
            for neighbor in self.G.neighbors(vertex):
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None
    
    def dijkstra_algorithm(self, start, end):
        """Власна реалізація алгоритму Дейкстри"""
        # Ініціалізація відстаней та попередніх вершин
        distances = {node: float('infinity') for node in self.G.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.G.nodes()}
        
        # Створюємо множину невідвіданих вершин
        unvisited = set(self.G.nodes())
        
        while unvisited:
            # Знаходимо вершину з найменшою відстанню серед невідвіданих
            current = min(unvisited, key=lambda node: distances[node])
            
            if current == end:  # Якщо досягли кінцевої вершини
                break
                
            # Видаляємо поточну вершину з невідвіданих
            unvisited.remove(current)
            
            # Перевіряємо всіх сусідів поточної вершини
            for neighbor in self.G.neighbors(current):
                if neighbor in unvisited:
                    # Розраховуємо нову відстань через поточну вершину
                    weight = self.G[current][neighbor]['weight']
                    new_distance = distances[current] + weight
                    
                    # Якщо знайдено коротший шлях
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # Відновлюємо шлях від кінцевої до початкової вершини
        if distances[end] == float('infinity'):
            return None
            
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        
        # Повертаємо шлях у правильному порядку
        return path[::-1]

def main():
    # Створюємо та налаштовуємо мережу
    metro = MetroNetwork()
    metro.create_metro_network()
    
    # Завдання 1: Аналіз мережі
    print("=== Завдання 1: Аналіз мережі ===")
    metro.analyze_network()
    
    # Завдання 2: Порівняння DFS та BFS
    print("\n=== Завдання 2: Порівняння DFS та BFS ===")
    start = 'Академмістечко'
    end = 'Палац Спорту'
    
    dfs_result = metro.dfs_path(start, end)
    print(f"\nШлях DFS від {start} до {end}:")
    print(" -> ".join(dfs_result) if dfs_result else "Шлях не знайдено")
    
    bfs_result = metro.bfs_path(start, end)
    print(f"\nШлях BFS від {start} до {end}:")
    print(" -> ".join(bfs_result) if bfs_result else "Шлях не знайдено")
    
    # Завдання 3: Найкоротший шлях (власна реалізація алгоритму Дейкстри)
    print("\n=== Завдання 3: Найкоротший шлях (власна реалізація Дейкстри) ===")
    shortest_path = metro.dijkstra_algorithm(start, end)
    print(f"\nНайкоротший шлях від {start} до {end}:")
    if shortest_path:
        print(" -> ".join(shortest_path))
        # Розрахуємо загальну вагу шляху
        total_weight = sum(metro.G[shortest_path[i]][shortest_path[i+1]]['weight'] 
                          for i in range(len(shortest_path)-1))
        print(f"Загальна вага шляху: {total_weight}")
    else:
        print("Шлях не знайдено")

if __name__ == "__main__":
    main()