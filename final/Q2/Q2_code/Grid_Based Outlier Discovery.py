# implement the algorithm without using relevant third-party packages
import csv
import math
import pandas as pd


def get_two_columns(data):
    # initializes the list
    pause_data = data.iloc[:, 0].tolist()
    play_data = data.iloc[:, 1].tolist()

    data = {'pause_data': pause_data, 'play_data': play_data}

    return data


def get_span(db):
    '''
    helper function to find the max span on the data
    :param db: two columns
    :return: max span
    '''
    span_pause = max(db['pause_data'])-min(db['pause_data'])
    span_play = max(db['play_data'])-min(db['play_data'])
    return max([span_pause,span_play])


def create_cell(l,db,d):
    '''
    create a x by x matrix where the number of cells in each dimension
    are equal to the span divided by l.
    :param l: the length of one cell
    :param db: two columns
    :param d: the distance
    :return:
    '''
    span = get_span(db)
    cells = int(math.ceil(span/l))

    # each cell represents the points in a l by l space
    cell_matrix = []
    # create a color matrix that maps the color of the cells in the cell matrix,
    # 0 is white or undecided, 1 is red, and 2 is pink, 3 is uncertain and need to check distance.
    # Outlier cells are denoted as -1. Empty cells are -2.
    color_matrix = []

    # goes through the entire database and puts each point into a cell
    # simultaniously creates a color matrix that is used to label the cells, used to tell if a cell is an outlier cell
    for i in range(1, cells+1):
        cell_row = []
        cell_color_row = []
        for j in range(1, cells+1):
            cell = []
            for k in range(0,len(db['pause_data'])):
                if(db['pause_data'][k] >= l*i-l and db['pause_data'][k] < l*i
                        and db['play_data'][k] >= l*j-l and db['play_data'][k] < l*j):
                    cell.append(k)
            cell_row.append(cell)
            cell_color_row.append(0)
        cell_matrix.append(cell_row)
        color_matrix.append(cell_color_row) # at first, all the cell color is 0:white

    return cell_matrix, color_matrix


def check_cell(cell_matrix, color_matrix, m):
    '''
    this matrix is used to record the number points in a given cell.
    Step1_1: if the # of objects of one cell more than M, all the objects in this cell should not be outlier,
    should be put red(1)
    Step1_2: for the Layer-1 neighbors of red cell, all the objects should not be outliers,
    should be put pink(2)
    Step1_3: empty cells should be put -2.
    :param cell_matrix: cell matrix after construction
    :param color_matrix: initialize as 0
    :param m: the threshold
    :return: change the color for the cell
    '''
    count_matrix = []

    # Step1: check to see if a cell has points greater than m,
    # if there are M objects inside, all the objects in this cell are not outlier(1)
    # if there are no objects inside, we define as the empty cell(-2)
    for i in range(0, len(cell_matrix)):
        count_row = []
        for j in range(0, len(cell_matrix)):
            if(len(cell_matrix[i][j]) == 0):
                color_matrix[i][j] = -2 # empty cells
            if(len(cell_matrix[i][j]) > m):
                color_matrix[i][j] = 1 # red cells
            count_row.append(len(cell_matrix[i][j]))
        count_matrix.append(count_row)

    # Step1_2.
    # denote the cells in the l1 layer to cells that are red as pink
    for i in range(0, len(cell_matrix)):
        for j in range(0, len(cell_matrix)):
            if(color_matrix[i][j] == 1):
                # check to see if the l1 cells are in range and than change color to pink
                if (i > 0 and i < len(cell_matrix)):
                    x = 0
                elif (i > 0):
                    x = -1
                else:
                    x = 1

                if (j > 0 and j < len(cell_matrix)):
                    y = 0
                elif (j > 0):
                    y = -1
                else:
                    y = 1

                if (x == 0 and y == 0):
                    color_matrix[i - 1][j] = 2
                    color_matrix[i + 1][j] = 2
                    color_matrix[i][j - 1] = 2
                    color_matrix[i][j + 1] = 2
                    color_matrix[i - 1][j - 1] = 2
                    color_matrix[i + 1][j - 1] = 2
                    color_matrix[i - 1][j + 1] = 2
                    color_matrix[i + 1][j + 1] = 2
                elif(x == 0 and y == -1):
                    color_matrix[i - 1][j - 1] = 2
                    color_matrix[i + 1][j - 1] = 2
                    color_matrix[i - 1][j] = 2
                    color_matrix[i + 1][j] = 2
                    color_matrix[i][j - 1] = 2
                elif(x == 0 and y == 1):
                    color_matrix[i - 1][j + 1] = 2
                    color_matrix[i + 1][j + 1] = 2
                    color_matrix[i][j + 1] = 2
                    color_matrix[i - 1][j] = 2
                    color_matrix[i + 1][j] = 2
                elif(x == -1 and y == 0):
                    color_matrix[i - 1][j] = 2
                    color_matrix[i - 1][j + 1] = 2
                    color_matrix[i - 1][j - 1] = 2
                    color_matrix[i][j - 1] = 2
                    color_matrix[i][j + 1] = 2
                elif(x == -1 and y == -1):
                    color_matrix[i - 1][j] = 2
                    color_matrix[i - 1][j - 1] = 2
                    color_matrix[i][j - 1] = 2
                elif(x == -1 and y == 1):
                    color_matrix[i - 1][j] = 2
                    color_matrix[i - 1][j + 1] = 2
                    color_matrix[i][j + 1] = 2
                elif (x == 1 and y == 0):
                    color_matrix[i + 1][j] = 2
                    color_matrix[i][j - 1] = 2
                    color_matrix[i][j + 1] = 2
                    color_matrix[i + 1][j - 1] = 2
                    color_matrix[i + 1][j + 1] = 2
                elif(x == 1 and y == -1):
                    color_matrix[i + 1][j] = 2
                    color_matrix[i][j - 1] = 2
                    color_matrix[i + 1][j - 1] = 2
                elif(x == 1 and y == 1):
                    color_matrix[i + 1][j] = 2
                    color_matrix[i][j + 1] = 2
                    color_matrix[i + 1][j + 1] = 2

    return cell_matrix, color_matrix, count_matrix


def check_layer1(cell_matrix, color_matrix,m, count_matrix):
    '''
    Step2: for those cell are not red, if there are M objects in cell and Layer-1 neighbors totally,
    all the objects in this cell are not outlier.
    :param cell_matrix:
    :param color_matrix:
    :param m:
    :param count_matrix:
    :return:
    '''
    # check all the white cells and check their first layer, if count first layer > m than color it pink
    for i in range(0, len(cell_matrix)):
        for j in range(0, len(cell_matrix)):
            if (color_matrix[i][j] == 0):
                if (i > 0 and i < len(cell_matrix)-1):
                    x = 0
                elif (i > 0):
                    x = -1
                else:
                    x = 1

                if (j > 0 and j < len(cell_matrix)-1):
                    y = 0
                elif (j > 0):
                    y = -1
                else:
                    y = 1

                if (x == 0 and y == 0):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 1])
                elif (x == 0 and y == -1):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                elif (x == 0 and y == 1):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                elif (x == -1 and y == 0):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                elif (x == -1 and y == -1):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                elif (x == -1 and y == 1):
                    count_matrix[i][j] += len(cell_matrix[i - 1][j])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                elif (x == 1 and y == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 1])
                elif (x == 1 and y == -1):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                    count_matrix[i][j] += len(cell_matrix[i][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 1])
                elif (x == 1 and y == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j])
                    count_matrix[i][j] += len(cell_matrix[i][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 1])

                if (count_matrix[i][j] > m):
                    color_matrix[i][j] = 2

    return cell_matrix, color_matrix, count_matrix


def check_distance(x,y,db,d):
    if(x == y):
        return False
    distance = math.sqrt((db['pause_data'][x]-db['pause_data'][y])**2 + (db['play_data'][x] -  db['play_data'][y]) **2)
    return (distance <= d)


def check_layer2(cell_matrix, color_matrix,m, count_matrix, db, d):
    # check all the white cells and check their second layer. If count second layer <= m than all those points in the cell are outliers
    outliers = []

    # Goes through the cell matrix and checks for cells that are still labeled as white
    for i in range(0, len(cell_matrix)):
        for j in range(0, len(cell_matrix)):
            if (color_matrix[i][j] == 0):
                # checks to see if the current cell is close to the edges of the cell matrix
                x_up = 0
                x_down = 0
                y_up = 0
                y_down = 0

                if(i > 0):
                    x_down = 1
                if(i > 1):
                    x_down = 2
                if(i > 2):
                    x_down = 3
                if(i < len(cell_matrix)-1):
                    x_up = 1
                if(i < len(cell_matrix)-2):
                    x_up = 2
                if(i < len(cell_matrix)-3):
                    x_up = 3

                if (j > 0):
                    y_down = 1
                if (j > 1):
                    y_down = 2
                if (j > 2):
                    y_down = 3
                if (j < len(cell_matrix) - 1):
                    y_up = 1
                if (j < len(cell_matrix) - 2):
                    y_up = 2
                if (j < len(cell_matrix) - 3):
                    y_up = 3

                # based on the results of the cell position, the algorithm checks x and y, up and down condition to make sure we don't check for a cell outside the matrix range
                if(x_up == 3 and x_down == 3 and y_up == 3 and y_down == 3):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])


                if (x_up == 3 and x_down == 3 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 3 and x_down == 3 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 3 and x_down == 3 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 3 and x_down == 3 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                if (x_up == 3 and x_down == 3 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                if (x_up == 3 and x_down == 3 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])


                if (y_up == 3 and y_down == 3 and x_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (y_up == 3 and y_down == 3 and x_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (y_up == 3 and y_down == 3 and x_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (y_up == 3 and y_down == 3 and x_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                if (y_up == 3 and y_down == 3 and x_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                if (y_up == 3 and y_down == 3 and x_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])


                if( x_down == 2 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                if (x_down == 2 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                if (x_down == 2 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                if (x_down == 1 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                if (x_down == 1 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                if (x_down == 1 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                if (x_down == 0 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                if (x_down == 0 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                if (x_down == 0 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])

                if (x_down == 2 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                if (x_down == 2 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                if (x_down == 2 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                if (x_down == 1 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                if (x_down == 1 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                if (x_down == 1 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])

                if (x_down == 0 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                if (x_down == 0 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                if (x_down == 0 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 3][j])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 3][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])

                if (x_up == 2 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 2 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 2 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 1 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 1 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 1 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 0 and y_up == 2):
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 0 and y_up == 1):
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])
                if (x_up == 0 and y_up == 0):
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 3])

                if (x_up == 2 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                if (x_up == 2 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                if (x_up == 2 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 2][j])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                if (x_up == 1 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                if (x_up == 1 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                if (x_up == 1 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i + 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                if (x_up == 0 and y_down == 2):
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 2])
                if (x_up == 0 and y_down == 1):
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j - 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j - 1])
                if (x_up == 0 and y_down == 0):
                    count_matrix[i][j] += len(cell_matrix[i][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 1][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 2][j + 3])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 1])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 2])
                    count_matrix[i][j] += len(cell_matrix[i - 3][j + 3])

            # if the number of points with in D distance is less than M, than that entire cell is an outlier cell
            if (count_matrix[i][j] < m):
                color_matrix[i][j] = -1

    # if count second layer > m, check every point inside the cells min distance to every other point. if points with distance <= d are greater than m, point is not an outlier
    for i in range(0, len(cell_matrix)):
        for j in range(0, len(cell_matrix)):
            if (color_matrix[i][j] == 0):
                for k in range(0, len(cell_matrix[i][j])):
                    d_count = 0
                    for t in range(0, len(db['pause_data'])):
                        if(check_distance(cell_matrix[i][j][k], t,db, d)):
                            d_count += 1
                    if(d_count <= m):
                        outliers.append(cell_matrix[i][j][k])

    for i in range(0, len(cell_matrix)):
        for j in range(0, len(cell_matrix)):
            if (color_matrix[i][j] == -1):
                for k in range(0, len(cell_matrix[i][j])):
                    outliers.append(cell_matrix[i][j][k])

    return cell_matrix, color_matrix, count_matrix, outliers


if __name__ == "__main__":
    # loading the data and choose two columns
    data_Q2 = pd.read_csv('two_columns.csv', header=None)
    db = get_two_columns(data_Q2)
    # set values for D and M
    # D_all = [0.1, 0.5, 1.0]
    # M_all = [50, 100]
    D = 2
    M= 1500
    l = D / (2 * math.sqrt(len(db)))
    # creates a cell matrix and maps every point in the database to a cell
    cell_matrix, color_matrix = create_cell(l,db,D)

    # checks each cell to see if they are red, colors the l1 of all red cells pink
    # empty cells are labeled as -2
    cell_matrix, color_matrix, count_matrix = check_cell(cell_matrix,color_matrix,M)

    # checks all white cells to see if they are pink
    cell_matrix, color_matrix, count_matrix = check_layer1(cell_matrix,color_matrix,M, count_matrix)

    # checks all white cells to see if they are outliers
    # if a cell isn't an outlier, individually test each point to see if its an outlier
    cell_matrix, color_matrix, count_matrix, outliers = check_layer2(cell_matrix, color_matrix,M, count_matrix, db, D)
    # print('In D and M:', D, M)
    print (outliers)
    print (len(outliers))