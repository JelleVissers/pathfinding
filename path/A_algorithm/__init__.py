import math

def possible_paths(coordinaten):
    '''
    search for possible paths
    :param coordinaten: coordinaten of searche point
    :return: list of posible coordinaten [[X0,Y0][X1,Y1]]
    '''

    possible_coordinaten =[]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]-1, coordinaten[1]+1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]  , coordinaten[1]+1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]+1, coordinaten[1]+1]]

    possible_coordinaten = possible_coordinaten + [[coordinaten[0]-1, coordinaten[1]+0]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]+1, coordinaten[1]+0]]

    possible_coordinaten = possible_coordinaten + [[coordinaten[0]-1, coordinaten[1]-1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]  , coordinaten[1]-1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0]+1, coordinaten[1]-1]]

    return possible_coordinaten

def filter_path(coordinaten,calculation_matrix,omgeving_matrix):
    '''
    filter out possible coordinaten and looks of there is already a value calculated
    :param coordinaten: list of all coordinatne
    :param calculation_matrix:  matrix of calculated points
    :param omgeving_matrix:  matrix of envirement
    :return: list of posible coordinatne [[X0,Y0],[X1,Y1]]
    '''

    possible_coordinaten = []

    for point in coordinaten:
        if calculation_matrix[point[1]][point[0]] is not 0 and omgeving_matrix[point[1]][point[0]] is not 1:
            possible_coordinaten =possible_coordinaten + [point]
    return possible_coordinaten

def matrix_replacevalue(matrix,value,x_coordinaten,y_coordinaten):
    '''
    verander waarde 0 naar 1 op gegeven positie in matrix
    '''
    yteller = 0
    test_matrix = []
    for y in matrix:
        xteller = 0
        x_line = []
        for x in y:
            if xteller == x_coordinaten and yteller == y_coordinaten:
                x_line = x_line + [value]
            else:
                x_line = x_line + [matrix[yteller][xteller]]
            xteller = xteller + 1
        yteller = yteller + 1

        test_matrix = test_matrix + [x_line]
    return test_matrix

def A_cost(nodecoordinaten,startpoint,endpoint,step_matrix,omgeving_matrix,cal_matrix):
    '''
    calculate the cost of the node with a algoritme
    :param startpoint: coordinaten startpoint  [x,y]
    :param endpoint: coordinaten of endpoint   [x,y]
    :param endpoint: stepmatrix nummer of steps
    :param nodecoordinaten: coodinaten of node [x,y]
    :return: cost of node
    '''

    possible_step = possible_paths(nodecoordinaten)
    possible_step_filter = filter_path(possible_step,cal_matrix,omgeving_matrix)
    step = 1
    found = False

    for point in possible_step_filter:                             # zoek aanliggende node met minste stappen
        step_point = step_matrix[point[1]][point[0]]
        if step_point == 0:
            if nodecoordinaten == startpoint:
                if step_point < step:
                    step = step_point+1
                    found = True
        else:
            if step_point < step:
                step = step_point+1
                found = True

        step_matrix = matrix_replacevalue(step_matrix, step, point[0], point[1])

    x_dif = nodecoordinaten[0]-endpoint[0]                  # calculate distance x direction between node and end
    y_dif = nodecoordinaten[1]-endpoint[1]                  # calculate distance y direction between node and end

    h = math.sqrt(math.pow(x_dif,2)+math.pow(y_dif,2))

    if found:
        print'goed'
        cost = step + h  # calculate total cost
        return cost,step_matrix

    else:
        print 'fout'
        cost = h  # calculate total cost
        return cost, step_matrix


