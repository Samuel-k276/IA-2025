# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 84:
# 110246 João Matreno
# 110274 Samuel Gomes

from search import Problem, Node, astar_search, depth_limited_search
from sys import stdin
from collections import deque, defaultdict
from copy import deepcopy


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

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""
    def __init__(self, board, rows: int, cols: int, regions: list, firstInitial: bool = True, unfilledRegions: list = None):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.regions = regions
        self.numOfRegions = len(regions) - 1
        self.unfilledRegions = sorted(regions[1:], key=lambda x: -1 * len(x)) if firstInitial else unfilledRegions or []
    
    def pop_smallest_region(self):
        """Remove e devolve a região com menos coordenadas."""
        if not self.unfilledRegions:
            return None
        region = self.unfilledRegions.pop()
        return region


    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        regionCoord = self.regions[region][0]
        adjacentRegions = []
        adjacentCoords = self.adjacent_positions(regionCoord[0], regionCoord[1])
        regionCounter = 1
        for region in self.regions:
            if region is None:
                continue
            for adjacentCoord in adjacentCoords:
                if adjacentCoord in region:
                    adjacentRegions.append(regionCounter)
                    break
            regionCounter += 1
        adjacentRegions.sort()
        return adjacentRegions
    
    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        coord = (row, col)
        if not self.is_in_board(coord):
            return -1
        
        for region in self.regions:
            if region is not None and coord in region:
                regionCoords = region
                break
        adjacents = []
        
        for coord in regionCoords:
            checking = []
            checking.append((coord[0] - 1, coord[1] - 1))
            checking.append((coord[0] - 1, coord[1]))
            checking.append((coord[0] - 1, coord[1] + 1))
            checking.append((coord[0], coord[1] - 1))
            checking.append((coord[0], coord[1] + 1))
            checking.append((coord[0] + 1, coord[1] - 1))
            checking.append((coord[0] + 1, coord[1]))
            checking.append((coord[0] + 1, coord[1] + 1))
            for checkingCoord in checking:
                if (self.is_in_board(checkingCoord) and
                    checkingCoord not in adjacents and
                    checkingCoord not in regionCoords):
                    adjacents.append(checkingCoord)
        adjacents.sort()
        return adjacents

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        values = []
        for coord in self.adjacent_positions(row, col):
            values.append(self.get_value(coord))
        return values
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = []
        line = stdin.readline().split()
        cols = len(line)
        col = 0
        rows = 0
        regions = []
        while True:
            if not line:
                break
            rows += 1
            for value in line:
                col += 1
                while len(regions) <= int(value):
                    regions.append(None)
                if not regions[int(value)]:
                    regions[int(value)] = []
                regions[int(value)].append((rows, col))
            col = 0
            board.append(line)
            line = stdin.readline().split()
        return Board(board, rows, cols, regions)  

    def print_instance(self):
        for i, line in enumerate(self.board):
            for j, value in enumerate(line):
                print(value, end='')
                if j < len(line) - 1:
                    print('\t', end='')
            if i < len(self.board) - 1:
                print()
            
    
    def is_in_board(self, coord) -> bool:
        if 0 < coord[0] and coord[0] <= self.rows and 0 < coord[1] and coord[1] <= self.cols:
            return True
        return False
    
    def get_value(self, coord):
        if self.is_in_board(coord):
            return self.board[coord[0] - 1 ][coord[1] - 1]
        return -1

class NuruominoState:
    state_id = 0

    def __init__(self, board: Board, prohibited: set = None, connections: list = None):
        self.board = board
        self.prohibited = prohibited or set()
        self.hash_cache = None
        self.connections = connections or self.get_connections(board)
        self.id = Nuruomino.state_id
        Nuruomino.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    
    def is_prohibited(self, coord):
        """Verifica se a coordenada está na lista de proibidos."""
        return coord in self.prohibited
    
    def num_of_unfilled_regions(self):
        """Devolve o número de regiões que ainda não foram preenchidas."""
        return len(self.board.unfilledRegions)
    
    def get_connections(self, board: Board):
        """
        Cria uma lista de dicionários que para cada index correspondente a um região, 
        e o seu dicionnário contém as coordenadas dessa região em contacto com outras regiões
        e as respetivas coordenadas na regiao de destino.
        """
        connections = [defaultdict(list)]
        for i in range(1, board.numOfRegions + 1):
            connections.append(defaultdict(list))
            for coord in board.regions[i]:
                d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for dx, dy in d:
                    adj_coord = (coord[0] + dx, coord[1] + dy)
                    if board.is_in_board(adj_coord) and board.get_value(adj_coord) != i:
                        connections[i][coord].append(adj_coord)
        return connections

    def __hash__(self):
        if self.hash_cache is None:
            self.hash_cache = hash((tuple(tuple(row) for row in self.board.board), frozenset(self.prohibited)))
        return self.hash_cache

    

class Nuruomino(Problem):
    state_id = 0
    
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.boardState = board
        self.noPieceRegions = board.numOfRegions
        self.initial = NuruominoState(board)

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        region = state.board.pop_smallest_region()
        regionActions = []
        blockTypeID = 0
        for blockType in blocks:
            for block in blockType:
                vector = block[0]
                zeroShift = 0
                for value in vector:
                    if value == 1: break
                    zeroShift += 1
                for coord in region:
                    topLeft = (coord[0], coord[1] - zeroShift)
                    if self.isvalid(state, block, region, blockID[blockTypeID], topLeft):
                        regionActions.append((blockID[blockTypeID], block, topLeft))
            blockTypeID += 1
        return regionActions
    
    def isvalid(self, state: NuruominoState, block, region, blockType, topLeft) -> bool:
        """
        Verifica se o bloco pode ser colocado na posiçao especificada.
        Recebe o estado atual, o bloco a colocar, a região onde se pretende
        colocar o bloco, o tipo do bloco e a coordenada superior esquerda onde
        se pretende colocar o bloco.
        Retorna True se o bloco pode ser colocado, False caso contrário.
        """
        # region: list -> set
        region_set = set(region)
        region_num = int(state.board.get_value(region[0]))
        # Verifica se o bloco cabe na região ou está isolado
        isolated = True
        blockCoord = [(topLeft[0] + i, topLeft[1] + j) for i in range(len(block)) for j in range(len(block[i])) if block[i][j] == 1]
        for coord in blockCoord:
            if coord not in region_set or state.is_prohibited(coord):
                return False
            if coord in state.connections[region_num]:
                isolated = False
        
        if isolated: return False
            
        # Verificar se o bloco nao faz 2x2 ou toca em adjacentes iguais
        d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for coord in blockCoord:
            for dx, dy in d:
                adj_coord = (coord[0] + dx, coord[1] + dy)
                if not state.board.is_in_board(adj_coord): continue
                
                if state.board.get_value(adj_coord) == blockType and adj_coord not in blockCoord:
                    return False
                if adj_coord not in region_set:
                    isolated = False
            
            corners = [
                [(coord[0] - 1, coord[1] - 1), (coord[0] - 1, coord[1]), (coord[0], coord[1] - 1)],
                [(coord[0] - 1, coord[1]), (coord[0] - 1, coord[1] + 1), (coord[0], coord[1] + 1)],
                [(coord[0], coord[1] - 1), (coord[0] + 1, coord[1] - 1), (coord[0] + 1, coord[1])],
                [(coord[0], coord[1] + 1), (coord[0] + 1, coord[1]), (coord[0] + 1, coord[1] + 1)]
            ]

            for corner in corners:
                if all(state.board.is_in_board(c) and (c in blockCoord or str(state.board.get_value(c)).isalpha()) for c in corner):
                    return False
        
        return not isolated
    
    def result(self, state: NuruominoState, action: tuple) -> NuruominoState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # action = (blockType, block, topLeft)
        blockType, block, topLeft = action
        newBoard = [row.copy() for row in state.board.board]
        newProhibited = state.prohibited.copy()
        newConnections = [{key: value.copy() for key, value in dic.items()} for dic in state.connections]
        L_elbow_found = False
        for i in range(len(block)):
            for j in range(len(block[i])):
                if block[i][j] == 1:
                    newBoard[topLeft[0] + i - 1][topLeft[1] + j - 1] = blockType
                elif block[i][j] == 0:
                    if blockType == 'S' or blockType == 'T':
                        newProhibited.add((topLeft[0] + i, topLeft[1] + j))
                    elif blockType == 'L' and not L_elbow_found:
                        # Check if a 0 is surrounded by 3 1s
                        d = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]
                        if sum(1 for dx, dy in d 
                               if 0 <= i + dx < len(block) and 0 <= j + dy < len(block[i]) 
                               and block[i + dx][j + dy] == 1) == 3:
                            newProhibited.add((topLeft[0] + i, topLeft[1] + j))
                            L_elbow_found = True

        return NuruominoState(Board(newBoard, state.board.rows, state.board.cols, state.board.regions, False, state.board.unfilledRegions.copy()), newProhibited, newConnections)

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        if state.num_of_unfilled_regions() != 0:
            return False
        
        seen = set()
        queue = deque()
        for coord in state.board.regions[1]:
            if str(state.board.get_value(coord)).isalpha():
                queue.append(coord)
                seen.add(coord)
                break
        
        # Verifica se todas as regiões estão conectadas
        count = 0
        rows, cols = state.board.rows, state.board.cols
        while queue:
            x, y = queue.popleft()
            count += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (1 <= nx <= rows and 1 <= ny <= cols and str(state.board.get_value((nx, ny))).isalpha() and (nx, ny) not in seen):
                    seen.add((nx, ny))
                    queue.append((nx, ny))

        return count == state.board.numOfRegions * 4

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass
    
board = Board.parse_instance()
problem = Nuruomino(board)

solution = depth_limited_search(problem, problem.noPieceRegions)
solution.state.board.print_instance()
