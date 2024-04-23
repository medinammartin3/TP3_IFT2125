# Martin Medina (20235219)
# Étienne Mitchell-Bouchard (20243430)

import sys
import random

dimension = 20
cell_size = 5
wall_height = 18
wall_thickness = 2.5

strategy_choice = 1

class Strategy :
    def __init__(self):
        pass

    def Apply(self):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        print("Do Something")

# Randomized depth-first search
# Sources :
# - https://www.algosome.com/articles/maze-generation-depth-first.html
# - https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
# - https://en.wikipedia.org/wiki/Depth-first_search
# - https://en.wikipedia.org/wiki/Maze_generation_algorithm
class Algorithm1(Strategy) :
    def Apply(self):

        # 1 = Mur
        # 0 = Chemin

        # Création de la grille avec que des murs
        labyrinthe = [[1 for _ in range(dimension*2+1)]for _ in range(dimension*2+1)]

        # Point de départ
        x = 0
        y = 0
        labyrinthe[x+1][y+1] = 0

        # Initialisation de la pile
        pile = [(x, y)]
        while len(pile) > 0:
            (x, y) = pile[-1]

            # Directions possibles
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for (dx, dy) in directions:
                (nx, ny) = (x + dx, y + dy)
                if nx >= 0 and ny >= 0 and nx < dimension and ny < dimension and labyrinthe[2 * nx + 1][2 * ny + 1] == 1:
                    labyrinthe[2 * nx + 1][2 * ny + 1] = 0
                    labyrinthe[2 * x + 1 + dx][2 * y + 1 + dy] = 0
                    pile.append((nx, ny))
                    break
            else:
                pile.pop()

        # Création de l'entrée et de la sortie
        labyrinthe[1][0] = 0
        labyrinthe[-2][-1] = 0

        for i in range(len(labyrinthe)):
            print(labyrinthe[i])

        return labyrinthe


# Modified DFS
# Pour le faire plus intéréssant, on a introduit un labyrinthe avec 2 sorties
# Modification du randomized DFS afin d'avoir un code plus simple et intuitif à comprendre
# Dans cet algoritme, le labyrinthe de construit plus en "couches" et d'une façon encore plus aléatoire
class Algorithm2(Strategy) :

    def Apply(self):

        # 1 = Mur
        # 0 = Chemin

        # Création de la grille avec que des murs
        labyrinthe = [[1 for _ in range(dimension*2+1)]for _ in range(dimension*2+1)]

        # Création aléatoire de l'entrée et de la sortie
        labyrinthe[random.randint(1, 1)][0] = 0
        labyrinthe[0][random.randint(0, dimension*2)] = 0
        labyrinthe[-2][-1] = 0

        # Point de départ
        x = 0
        y = 0
        labyrinthe[x+1][y+1] = 0

        # Initialisation de la pile
        pile = [(x, y)]
        while len(pile) > 0:
            (x, y) = pile[-1]

            # Directions possibles
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for (dx, dy) in directions:
                (nx, ny) = (x + dx, y + dy)
                if nx >= 0 and ny >= 0 and nx < dimension and ny < dimension and labyrinthe[2 * nx + 1][2 * ny + 1] == 1:
                    labyrinthe[2 * nx + 1][2 * ny + 1] = 0
                    labyrinthe[2 * x + 1 + dx][2 * y + 1 + dy] = 0
                    pile.append((nx, ny))
                    break
            else:
                pile.pop()

        for i in range(len(labyrinthe)):
            print(labyrinthe[i])

        return labyrinthe



class Generator() :
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        return self.strategy.Apply()

class Creator() :
    def __init__(self):
        pass

    def PrintLabyrinth(self, fileName, content):
        file = open(fileName, "w")
        file.write("// Authors : Martin Medina and Étienne Mitchell-Bouchard\n"
                   "difference(){\n"
                   "union(){\n"
                   "// base plate\n"
                   f"cube([{cell_size*(dimension*2)},{cell_size*(dimension*2)},1], center=false);\n"
                   f"translate([{cell_size/2},{wall_thickness/2},{wall_height / 2 + 1}]){{\n"
                   f"cube([{cell_size},{wall_thickness},{wall_height}], center=true);\n"
                   "}\n")
        for i in range(len(content)-1):
            for j in range(len(content)-1):
                # Murs axe Y
                if content[i][j] == 1 and content[i][j+1] == 1:
                    file.write(f"translate([{i*cell_size+wall_thickness/2},{j*cell_size+cell_size/2},{wall_height/2+1}]){{\n"
                               "rotate([0,0,90]){\n"
                               f"cube([{cell_size},{wall_thickness},{wall_height}], center=true);\n"
                               "}\n"
                               "}\n")
                # Murs axe X
                if content[i][j] == 1 and content[i+1][j] == 1:
                    file.write(f"translate([{i*cell_size+cell_size/2},{j*cell_size+wall_thickness/2},{wall_height/2+1}]){{\n"
                               f"cube([{cell_size},{wall_thickness},{wall_height}], center=true);\n"
                               "}\n")
        # Finir les bordures externes
        file.write(f"translate([{cell_size*dimension-cell_size/2},{cell_size*(dimension*2)-wall_thickness/2},{wall_height/2+1}]){{\n"
                   f"cube([{cell_size*(dimension*2) - cell_size*2},{wall_thickness},{wall_height}], center=true);\n"
                   "}\n"
                   f"translate([{cell_size*(dimension*2)-wall_thickness/2},{cell_size*dimension},{wall_height/2+1}]){{\n"
                   "rotate([0,0,90]){\n"
                   f"cube([{cell_size*(dimension*2)},{wall_thickness},{wall_height}], center=true);\n"
                   "}\n"
                   "}\n"
                   "// logo\n"
                   f"translate([{cell_size*3}, {wall_thickness/4}, {wall_height*0.3}]){{\n"
                   "rotate([90, 0, 0]){\n"
                   f"linear_extrude(1) text(\"IFT2125 Martin/Etienne\", size={wall_height/2});\n"
                   "}}}}")
        file.close()


# main call
def main():
    global strategy_choice
    args = sys.argv[:]
    if len(args) >= 2 :
        strategy_choice = int(args[1])

    # Generator
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else :
        print("error strategy choice")
    code_labyrinthe = my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth(f"labyrinthe_algo{strategy_choice}.scad", code_labyrinthe)


if __name__ == "__main__":
    main()
