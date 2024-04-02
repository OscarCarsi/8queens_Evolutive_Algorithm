#Importa el modulo random para generar los aleatorios que se necesitaran
import random as random;
import matplotlib.pyplot as plt

#se hace la generación de un tablero con las reinas en posiciones aleatorias

def create_board(size_board):
    # Se crea el tablero 8 x 8 con 0 en todas las posiciones
    board = [[0]*size_board for _ in range(size_board)]
    # Se declara un set para guardar las posiciones ocupadas y que no se repitan
    occupied_positions = set()
    #Se recorre el tablero
    for _ in range(size_board):
        # Se toman posiciones aleatorias en fila y columna para colocar las reinas
        row, col = random.randint(0, size_board - 1), random.randint(0, size_board - 1)
        # Se verifica que la posición no este ocupada
        while (row, col) in occupied_positions:
            # Si la posición esta ocupada se toman nuevas posiciones
            row, col = random.randint(0, size_board - 1), random.randint(0, size_board - 1)
        # Se agrega la posición al set de posiciones ocupadas y se coloca la reina en el tablero
        occupied_positions.add((row, col))
        board[row][col] = 1

    return board

#Se hace la generación de los tableros definidos, en esta caso 100 tableros, con el tamaño de 8x8
def create_boards (size_board, num_boards):
    boards = []
    for _ in range(num_boards):
        board = create_board(size_board)
        boards.append(board)
    return boards
#Se seleccionan 5 tableros aleatorios para iniciar la selección de los padres
def select_random_boards(boards):
    return random.sample(boards, 5)

def calculate_fitness(selected_board):
    conflicts = 0
    # Obtiene el tamaño del tablero
    size_board = len(selected_board)
    
    # Recorre las filas
    for row in selected_board:
        #Suma las filas para obtener el numero de reinas en la fila
        num_queens = sum(row)
        #Calcula los conflictos en la fila mediante la función de aptitud de n x (n-1) / 2
        conflicts += num_queens * (num_queens - 1) // 2

    # Recorre las columnas
    for col in range(size_board):
        #Suma las columnas para obtener el numero de reinas en la columna
        num_queens = sum(selected_board[row][col] for row in range(size_board))
        #Calcula los conflictos en la columna mediante la función de aptitud de n x (n-1) / 2
        conflicts += num_queens * (num_queens - 1) // 2

    # Se identifican las diagonales
    for diff in range(-size_board + 1, size_board):
        # obtiene la diagonal que va dede la esquina superior izquierda a la inferior derecha
        diag1 = [selected_board[i][i - diff] for i in range(size_board) if 0 <= i - diff < size_board]
        # obtiene la diagonal que va dede la esquina superior derecha a la inferior izquierda
        diag2 = [selected_board[i][size_board - 1 - i - diff] for i in range(size_board) if 0 <= size_board - 1 - i - diff < size_board]
        #Suma las reinas de cada diagonal
        num_queens1 = sum(diag1)
        num_queens2 = sum(diag2)
        #Calcula los conflictos en las diagonales mediante la función de aptitud de n x (n-1) / 2
        conflicts += num_queens1 * (num_queens1 - 1) // 2
        conflicts += num_queens2 * (num_queens2 - 1) // 2

    return conflicts

def select_best_boards(boards):
    #Obtiene la aptitud de cada tablero
    fitness_boards = [(calculate_fitness(board), board) for board in boards]
    #Se combinan los tableros con su aptitud correspondiente
    boards_with_fitness = list(zip(fitness_boards, boards))
    #Se ordenan los tableros por aptitud de menor a mayor
    boards_with_fitness.sort(key=lambda x: x[0])
    # Se obtienen los padres que son los dos primeros tableros con menos choques
    parents = [board[1] for board in boards_with_fitness[:2]]  # Solo devuelve los tableros
    # Regreso los padres
    return parents

def replace(population, final_board):
    # Calcula la aptitud del tablero final
    final_fitness = calculate_fitness(final_board)

    # Calcula la aptitud de todos los tableros en la población
    fitnesses = [calculate_fitness(board) for board in population]

    # Encuentra el índice del tablero con el mayor número de choques
    worst_board_index = fitnesses.index(max(fitnesses))

    # Obtiene la aptitud del peor tablero
    worst_board_fitness = fitnesses[worst_board_index]

    # Si el tablero final es mejor que el peor tablero en la población, reemplaza el peor tablero
    if final_fitness < worst_board_fitness:
        population[worst_board_index] = final_board

    return population

def get_queens(board):
    queens = set()
    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element == 1:
                queens.add((i, j))
    return queens

#seleccionamos al azar n reinas de cada tablero (según se necesiten)
def select_random_queens(queens, num_queens):
    queens_list = list(queens)
    return set(random.sample(queens_list, num_queens))

def mutate(board, size_board):
    # Obtiene las reinas del tablero
    queens = get_queens(board)
    # Obtiene las posiciones ocupadas
    occupied_positions = set(queens)
    # Selecciona una reina al azar
    selected_queen = select_random_queens(queens, num_queens=1).pop()
    # Se toman posiciones aleatorias en fila y columna para colocar las reinas
    row, col = random.randint(0, size_board - 1), random.randint(0, size_board - 1)
    # Se verifica que la posición no este ocupada
    while (row, col) in occupied_positions:
        # Si la posición esta ocupada se toman nuevas posiciones
        row, col = random.randint(0, size_board - 1), random.randint(0, size_board - 1)
    # Se quita la reina de su posición original 
    board[selected_queen[0]][selected_queen[1]] = 0
    # Se coloca la reina en la nueva posición
    board[row][col] = 1
    return board
        


#combinamos las reinas seleccionadas al azar, en un nuevo tablero
def crossover(board1, board2):
    queens_board1 = get_queens(board1)
    selected_queens1 = select_random_queens(queens_board1, num_queens=4)

    queens_board2 = get_queens(board2)
    selected_queens2 = select_random_queens(queens_board2, num_queens=4)

    # Combinamos las reinas de los dos tableros padres
    combined_queens = selected_queens1.union(selected_queens2)

    # checamos si alguna coordenada se repite de ser asi no es compatible la cruza
    if len(combined_queens) < len(selected_queens1) + len(selected_queens2):
        print("Crossover is incompatible! The following coordinates are repeated:")
        repeated_coordinates = selected_queens1.intersection(selected_queens2)
        print(repeated_coordinates)
        return None

        # Create a new 8x8 board
    new_board = [[0] * 8 for _ in range(8)]

    # Place the queens on the new board
    for coord in combined_queens:
        new_board[coord[0]][coord[1]] = 1

    return new_board


def print_board_with_queens(coordinates):
        for row in coordinates:
            print(' '.join(str(cell) for cell in row))

def main():
    size_board = 8
    num_boards = 100
    mutate_prob = 0.8
    max_evaluations = 10000
    evaluations = 0
    best_fitnesses = []  # Lista para rastrear la aptitud del mejor tabñero
    boards = create_boards(size_board, num_boards) # Se crean los tableros
    while evaluations < max_evaluations: # Se realizan las evaluaciones
        for i, board in enumerate(boards): #Se recorren los tableros
            conflicts = calculate_fitness(board) #Se calculan los conflictos
            print(f"Tablero {i+1}:")
            print_board_with_queens(board) #Se imprime el tablero
            print(f"Conflictos: {conflicts}")
            best_fitness = min(calculate_fitness(board) for board in boards) #Se obtiene el mejor tablero
            best_fitnesses.append(best_fitness) #Se agrega a la lista de mejores aptitudes
            evaluations += 1
            if conflicts == 0: #Si no hay conflictos se imprime el tablero y se termina el programa
                print(f"Solución encontrada en el tablero {i+1}:")
                print_board_with_queens(board)
                print(f"Evaluaciones: {evaluations}")

                # Grafica la convergencia
                plt.plot(best_fitnesses)
                plt.title('Convergencia')
                plt.xlabel('Evaluaciones')
                plt.ylabel('Choques')
                plt.show()

                return
        descendants = [] # Se crea una lista para los descendientes
        while len(descendants) < 10: # Se generan 10 descendientes
            # Selecciona 5 tableros aleatorios
            selectBoards = select_random_boards(boards)
            # Selecciona los dos mejores tableros
            bestBoards = select_best_boards(selectBoards)
            # Cruza los dos mejores tableros
            crossoverresult = crossover(bestBoards[0], bestBoards[1])
            # Si la cruza es compatible
            if crossoverresult is not None:
                # Si el valor aleatorio es menor a la probabilidad de mutación, se muta el tablero
                if random.random() < mutate_prob:
                    final_board = mutate(crossoverresult, size_board)
                else:
                    # Si no se muta el tablero, se asigna el tablero resultante de la cruza
                    final_board = crossoverresult
                # Se agrega el tablero a la lista de descendientes
                descendants.append(final_board)

        # Reemplaza los tableros menos aptos en la población con los nuevos descendientes
        for descendant in descendants:
            boards = replace(boards, descendant)

    print("No se encontró una solución después de 10,000 evaluaciones.")
    # Grafica la convergencia
    plt.plot(best_fitnesses)
    plt.title('Convergencia')
    plt.xlabel('Evaluaciones')
    plt.ylabel('Choques')
    plt.show()

if __name__ == "__main__":
    main()