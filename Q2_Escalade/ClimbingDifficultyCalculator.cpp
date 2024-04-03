// Etienne Mitchell-Bouchard, 20243430
// Martin Medina, 20235219

#include "ClimbingDifficultyCalculator.h"
#include <fstream>
#include <vector>
#include <sstream>
// #include <unordered_set>
// #include <math.h>
// #include <algorithm>
#include <iostream>
#include <iterator>
#include <cstdint>

using namespace std;

// ce fichier contient les definitions des methodes de la classe ClimbingDifficultyCalculator
// this file contains the definitions of the methods of the ClimbingDifficultyCalculator class

ClimbingDifficultyCalculator::ClimbingDifficultyCalculator()
{
}

int ClimbingDifficultyCalculator::CalculateClimbingDifficulty(std::string filename)
{
    //On parse le fichier pour obtenir notre matrice
    vector<vector<int>> matrice;
    ifstream file(filename);
    string line;
    while (getline(file, line)) {
        vector<int> v;
        string s;
        for (char c : line) {
            if (c != ',' && c != '\r')
                s.push_back(c);
            else {
                v.push_back(stoi(s));
                s = "";
            }
        }
        if (!s.empty())
            v.push_back(stoi(s));
        matrice.push_back(v);
    }

    int lines = (int) matrice.size();
    int columns = (int) matrice.at(0).size();
    //Les 2D arrays gardent en mémoire les valeurs intermédiaires (Programmation dynamique)
    int pts[lines][columns];
    bool checked[lines][columns];
    for (int i = 0; i < lines; ++i) {
        for (int j = 0; j < columns; ++j) {
            pts[i][j] = INT32_MAX;
            checked[i][j] = false;
        }
    }
    //On trouve notre source, le minimum de la 1ère ligne
    int actualX = lines - 1;
    int actualY = 0;
    int min = INT32_MAX;
    for (int j = 0; j < columns; ++j) {
        int val = matrice[actualX][j];
        pts[lines - 1][j] = val;
        if (val < min) {
            min = val;
            actualY = j;
        }
    }
    //Dijkstra
    while (actualX != 0) {
        int actual = pts[actualX][actualY];
        checked[actualX][actualY] = true;
        //Point à gauche
        if (actualY > 0) {
            if (pts[actualX][actualY - 1] > actual + matrice[actualX][actualY - 1])
                pts[actualX][actualY - 1] = actual + matrice[actualX][actualY - 1];
        }
        //Point à droite
        if (actualY < columns - 1) {
            if (pts[actualX][actualY + 1] > actual + matrice[actualX][actualY + 1])
                pts[actualX][actualY + 1] = actual + matrice[actualX][actualY + 1];
        }
        //Point en haut
        if (actualX > 0) {
            if (pts[actualX - 1][actualY] > actual + matrice[actualX - 1][actualY])
                pts[actualX - 1][actualY] = actual + matrice[actualX - 1][actualY];
        }
        //On trouve la distance la plus courte et on la sélectionne comme prochain point
        min = INT32_MAX;
        for (int i = 0; i < lines; ++i) {
            for (int j = 0; j < columns; ++j) {
                int dist = pts[i][j];
                if (dist < min && !checked[i][j]) {
                    min = dist;
                    actualX = i;
                    actualY = j;
                }
            }
        }
    }
    return pts[actualX][actualY];
}

