from search import Problem, Node, depth_first_tree_search
from sys import stdin
from collections import deque

block_coord = [
    ############  L  ############
    [
        [
            [0, 0],
            [1, 0],
            [2, 0], [2, 1]
        ],
        [
            [0, 0], [0, 1], [0, 2],
            [1, 0]
        ],
        [
                           [0, 2],
            [1,0], [1, 1], [1, 2]
        ],
        [
            [0, 0], [0, 1],
                    [1, 1],
                    [2, 1]
        ],
        [
                    [0, 1],
                    [1, 1],
            [2, 0], [2, 1]
        ],
        [
            [0, 0], [0, 1], [0, 2],
                            [1, 2]
        ],
        [
            [0, 0],
            [1, 0], [1, 1], [1, 2]
        ],
        [
            [0, 0], [0, 1],
            [1, 0],
            [2, 0]
        ]
    ],
    ############  T  ############
    [
        [
            [0, 0],
            [1, 0], [1, 1],
            [2, 0]
        ],
        [
            [0, 0], [0, 1], [0, 2],
                    [1, 1]
        ],
        [
                    [0, 1],
            [1, 0], [1, 1], [1, 2]
        ],
        [
                    [0, 1],
            [1, 0], [1, 1],
                    [2, 1]
        ],
    ],
    ############  I  ############
    [
        [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0]
        ],
        [
        [0, 0], [0, 1], [0, 2], [0, 3]
        ]
    ],
    ############  S   ############
    [
        [
                    [0, 1], [0, 2],
            [1, 0], [1, 1]
        ],
        [
            [0, 0],
            [1, 0], [1, 1],
                    [2, 1]
        ],
        [
            [0, 0], [0, 1],
                    [1, 1], [1, 2]
        ],
        [
                    [0, 1],
            [1, 0], [1, 1],
            [2, 0]
        ]
    ]
]

blocks = [
    ############  L  ############
    [
        [
            [1, 0],
            [1, 0],
            [1, 1]
        ],
        [
            [1, 1, 1],
            [1, 0, 0]
        ],
        [
            [0, 0, 1],
            [1, 1, 1]
        ],
        [
            [1, 1],
            [0, 1],
            [0, 1]
        ],
        [
            [0, 1],
            [0, 1],
            [1, 1]
        ],
        [
            [1, 1, 1],
            [0, 0, 1]
        ],
        [
            [1, 0, 0],
            [1, 1, 1]
        ],
        [
            [1, 1],
            [1, 0],
            [1, 0]
        ]
    ],
    ############  T  ############
    [
        [
            [1, 0],
            [1, 1],
            [1, 0]
        ],
        [
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [0, 1]
        ],
    ],
    ############  I  ############
    [
        [
            [1],
            [1],
            [1],
            [1]
        ],
        [
        [1, 1, 1, 1]
    ],
    ],
    ############  S   ############
    [
        [
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [1, 0],
            [1, 1],
            [0, 1]
        ],
        [
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
        [0, 1],
        [1, 1],
        [1, 0]
    ]
    ]
]

blockID = ['L', 'T', 'I', 'S']
id_set = set(blockID)

# Variáveis globais para armazenar dados constantes do problema.
# Rows, cols e regions não mudam durante a execução do programa, por isso são definidas aqui.
# Evita estar sempre a passar ao se criar uma nova instância do Board.

num_of_rows = 0
num_of_cols = 0
regions = []
regions_set = []
num_of_regions = 0
coords_to_region = {}
adjacent_regions = {}
adjacent_coords = {} # Maps coords to their adjacent coords
coords_to_corner = {} # Maps coords to their corner coords

class Board:
    __slots__ = ('board', 'conections', 'filled_regions')

    """Representação interna de um tabuleiro do Puzzle Nuruomino."""
    def __init__(self, board, connections=None, filled_regions=None):
        self.board = board
        self.conections = connections or self.calculate_connections()
        self.filled_regions = filled_regions or set()
    
    def adjacent_regions(self, region: int) -> list:
        """
        Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento.
        Usar apenas no estado inicial, em que apenas temos números como valores.
        """
        global regions, coords_to_region
        adjacentRegions = set()
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for coord in regions[region]:
            for dx, dy in d:
                neighbor = (coord[0] + dx, coord[1] + dy)
                if neighbor in coords_to_region:
                    neighbor_value = self.get_value(neighbor)
                    if neighbor_value != str(region + 1):
                        adjacentRegions.add(int(neighbor_value) - 1)
        return list(adjacentRegions)
    
    def calculate_connections(self) -> dict:
        """Calcula as ligações entre as regiões do tabuleiro."""
        global regions, adjacent_regions
        connections = {}
        for i in range(len(regions)):
            connections[i] = self.adjacent_regions(i)
            adjacent_regions[i] = connections[i]
        return connections
    
    def adjacent_positions(self, row: int, col: int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        coord = (row, col)
        if not self.is_in_board(coord):
            return []

        regionCoordsSet = regions_set[coords_to_region[coord]]
        adjacents = set()
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

        for coord in regionCoordsSet:
            for dx, dy in directions:
                neighbor = (coord[0] + dx, coord[1] + dy)
                if (self.is_in_board(neighbor) and
                    neighbor not in regionCoordsSet):
                    adjacents.add(neighbor)

        return list(adjacents)

    def adjacent_values(self, row: int, col: int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        values = set()
        for coord in self.adjacent_positions(row, col):
            values.add(self.get_value(coord))
        return list(values)
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        global num_of_rows, num_of_cols, regions, coords_to_region, num_of_regions
        board = []
        
        for line in stdin:
            line = line.split()
            if not line:
                break
            board.append(line)
            for col, value in enumerate(line):
                region_id = int(value) - 1
                while len(regions) <= region_id:
                    regions.append([])
                    regions_set.append(set())
                regions[region_id].append((num_of_rows, col))
                regions_set[region_id].add((num_of_rows, col))
                coords_to_region[(num_of_rows, col)] = region_id
            num_of_rows += 1
        
        # Pre-calculate
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (i, j) not in adjacent_coords:
                    # Adjacent coordinates
                    adjacent_coords[(i, j)] = set()
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        neighbor = (i + dx, j + dy)
                        if neighbor in coords_to_region:
                            adjacent_coords[(i, j)].add(neighbor)
                    
                    # Corners
                    left, right, up, down = j - 1, j + 1, i - 1, i + 1
                    corners = [
                        [(up, left), (up, j), (i, left)],
                        [(up, right), (up, j), (i, right)],
                        [(down, left), (i, left), (down, j)],
                        [(down, right), (i, right), (down, j)]
                    ]
                    coords_to_corner[(i, j)] = []
                    for corner in corners:
                        if (corner[0] in coords_to_region):
                            coords_to_corner[(i, j)].append(corner)
        
        num_of_cols = len(board[0]) if board else 0
        num_of_regions = len(regions)
        return Board(board)

    def print_instance(self):
        global num_of_rows, num_of_cols
        for i, line in enumerate(self.board):
            for j, value in enumerate(line):
                print(value, end='')
                if j < num_of_cols - 1:
                    print('\t', end='')
            if i < num_of_rows - 1:
                print()
            
    
    def is_in_board(self, coord) -> bool:
        return coord in coords_to_region
    
    def get_value(self, coord):
        return self.board[coord[0]][coord[1]]
    

class NuruominoState:
    __slots__ = ('board', 'prohibited', 'hash_cache', 'id', 'all_actions')

    state_id = 0

    def __init__(self, board: Board, prohibited: set = None, allActions = None, firstInitial: bool = True):
        self.board = board
        self.prohibited = prohibited or set()
        self.hash_cache = None
        self.id = Nuruomino.state_id
        Nuruomino.state_id += 1
        self.all_actions = self.calculate_all_actions() if firstInitial else allActions or []
    
    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    
    def is_prohibited(self, coord):
        """Verifica se a coordenada está na lista de proibidos."""
        return coord in self.prohibited
    
    def num_of_unfilled_regions(self):
        """Devolve o número de regiões que ainda não foram preenchidas."""
        return len(self.all_actions)

    def __hash__(self):
        if self.hash_cache is None:
            self.hash_cache = hash((tuple(tuple(row) for row in self.board.board), frozenset(self.prohibited)))
        return self.hash_cache

    def get_least_actions(self):
        """
        Retorna a lista de ações com o menor número de ações possíveis.
        E altera a lista de ações para que apenas as outras ação seja mantida.
        """
        if not self.all_actions:
            return []
        smallest_length = len(self.all_actions[0])
        smallest_actions = self.all_actions[0]
        smallest_index = 0
        for i, actions in enumerate(self.all_actions):
            if len(actions) < smallest_length:
                smallest_length = len(actions)
                smallest_actions = actions
                smallest_index = i
        del self.all_actions[smallest_index]
        return smallest_actions

    def calculate_all_actions(self):
        global regions
        allActions = []
        regionNum = 0
        for region in regions:
            blockTypeID = 0
            regionActions = []
            for i, blockType in enumerate(blocks):
                for j, block in enumerate(blockType):
                    vector = block[0]
                    zeroShift = 0
                    for value in vector:
                        if value == 1: break
                        zeroShift += 1
                    for coord in region:
                        topLeft = (coord[0], coord[1] - zeroShift)
                        if self.isvalid(region, topLeft, (i, j)):
                            regionActions.append((regionNum, blockID[blockTypeID], block, topLeft, (i, j)))
                blockTypeID += 1
            allActions.append(regionActions)
            regionNum += 1
        return allActions
    
    def isvalid(self, region, topLeft, b) -> bool:
        """
        Verifica se o bloco pode ser colocado na posiçao especificada.
        Recebe o estado atual, o bloco a colocar, a região onde se pretende
        colocar o bloco, o tipo do bloco e a coordenada superior esquerda onde
        se pretende colocar o bloco.
        Retorna True se o bloco pode ser colocado, False caso contrário.
        """
        # Verifica se o bloco cabe na região
        i, j = b
        b = block_coord[i][j]
        blockCoord = set()
        for i, j in b:
            coord = (topLeft[0] + i, topLeft[1] + j)
            if coord not in region or coord in self.prohibited:
                return False
            blockCoord.add(coord)

        # Verificar se o bloco nao está isolado na região
        for coord in blockCoord:
            for adj_coord in adjacent_coords[coord]:
                if adj_coord in coords_to_region and adj_coord not in region:
                    return True
        
        return False
    

class Nuruomino(Problem):
    __slots__ = ('boardState', 'initial')

    state_id = 0
    
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.boardState = board
        self.initial = NuruominoState(board)

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        if not state.all_actions:
            return []
        
        # Verificar se as regioes ainda estao ligadas
        queue = deque([0])
        seen = set([0])
        while queue:
            region = queue.popleft()
            for neighbor in state.board.conections[region]:
                if neighbor not in seen:
                    queue.append(neighbor)
                    seen.add(neighbor)

        global num_of_regions
        if len(seen) != num_of_regions:
            return []

        smallestActions = state.get_least_actions()
        return smallestActions
    
    def isvalid(self, state: NuruominoState, regionNum, blockType, topLeft, b) -> bool:
        """
        Verifica se o bloco pode ser colocado na posiçao especificada.
        Recebe o estado atual, o bloco a colocar, a região onde se pretende
        colocar o bloco, o tipo do bloco e a coordenada superior esquerda onde
        se pretende colocar o bloco.
        Retorna True se o bloco pode ser colocado, False caso contrário.
        """
        global regions_set, coords_to_region
        region_set = regions_set[regionNum]
        # Verifica se o bloco cabe na região
        i, j = b
        block = block_coord[i][j]
        r, c = topLeft
        blockCoord = {(r + i, c + j) for (i, j) in block}

        for coord in blockCoord:
            if coord not in region_set or coord in state.prohibited:
                return False
        
        # Verificar se o bloco nao faz 2x2 ou toca em adjacentes iguais ou está isolado na região
        isolated = True
        for x, y in blockCoord:
            for corner in coords_to_corner[(x, y)]:
                if ((corner[0] in blockCoord or state.board.get_value(corner[0]) in id_set) and
                    (corner[1] in blockCoord or state.board.get_value(corner[1]) in id_set) and
                    (corner[2] in blockCoord or state.board.get_value(corner[2]) in id_set)):
                    return False
                
            for adj_coord in adjacent_coords[(x, y)]:
                if adj_coord not in coords_to_region: continue
                
                if adj_coord not in blockCoord and state.board.get_value(adj_coord) == blockType:
                    return False
                if isolated == True and adj_coord not in region_set and adj_coord not in state.prohibited:
                    isolated = False
                
        return not isolated
    
    def result(self, state: NuruominoState, action: tuple) -> NuruominoState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # action = (regionNum, blockType, block, topLeft)
        regionNum, blockType, block, topLeft, _ = action
        newBoard = [row.copy() for row in state.board.board]
        newConnections = {}
        newProhibited = state.prohibited.copy()
        length = len(block)
        length2 = len(block[0])
        new_region_conections = set()
        global coords_to_region
        blockCoord = set()
        for i in range(length):
            for j in range(length2):
                if block[i][j] == 1:
                    x, y = topLeft[0] + i, topLeft[1] + j
                    newBoard[x][y] = blockType
                    blockCoord.add((x, y))
                    for neighbor in adjacent_coords[(x, y)]:
                        if neighbor in coords_to_region:
                            r = coords_to_region[neighbor]
                            if r not in new_region_conections and r != regionNum and (r not in state.board.filled_regions or state.board.get_value(neighbor) in id_set):
                                new_region_conections.add(r)
                elif block[i][j] == 0:
                    if blockType == 'S' or blockType == 'T':
                        newProhibited.add((topLeft[0] + i, topLeft[1] + j))
                    elif blockType == 'L':
                        if sum(1 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)] 
                               if 0 <= i + dx < length and 0 <= j + dy < length2 
                               and block[i + dx][j + dy] == 1) == 3:
                            newProhibited.add((topLeft[0] + i, topLeft[1] + j))

        # Procurar por celulas proibidas adicionais:
        # 1. Aquelas da regiao que não estão no bloco
        for coord in regions[regionNum]:
            if coord not in newProhibited and coord not in blockCoord:
                newProhibited.add(coord)

        # Conexoes que desaparecem
        to_remove = set()
        for conn in state.board.conections[regionNum]:
            if conn not in new_region_conections:
                to_remove.add(conn)

        # Atualiza as conexões da região
        for key, value in state.board.conections.items():
            if key == regionNum:
                newConnections[key] = list(new_region_conections)
            elif key in to_remove:
                newConnections[key] = [v for v in value if v != regionNum]
            else:
                newConnections[key] = value.copy()

        # Marca a região como preenchida
        filled_regions = state.board.filled_regions.copy()
        filled_regions.add(regionNum)

        # Update das actions das regioes adjacentes
        global adjacent_regions
        newActions = state.all_actions.copy()
        newNuruominoState = NuruominoState(Board(newBoard, newConnections, filled_regions), newProhibited, newActions, False)
        for i, regional_actions in enumerate(newActions):
            if regional_actions[0][0] in adjacent_regions[regionNum]:
                new = [action for action in regional_actions if self.isvalid(newNuruominoState, action[0], action[1], action[3], action[4])]
                newNuruominoState.all_actions[i] = new
     
        return newNuruominoState

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        if state.num_of_unfilled_regions() != 0:
            return False
        
        seen = set([0])
        queue = deque([0])
        count = 0
        while queue:
            region = queue.popleft()
            count += 1
            for neighbor in state.board.conections[region]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        return count == num_of_regions

    def h(self, node: Node):	
        """Função heuristica utilizada para a procura A*."""
        return -1 * node.state.num_of_unfilled_regions()

board = Board.parse_instance()
problem = Nuruomino(board)
solution = depth_first_tree_search(problem)
solution.state.board.print_instance()
