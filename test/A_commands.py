
def color(value, maximum):
    '''
    :param value: value of point
    :param maximum:   max value of points in matrix
    :return:  coller of point
    '''

    if value is not 0:
        color_value = (value / maximum) * 1000

        if color_value < 500:
            color = '#%02x%02x%02x' % (0, color_value * 255 / 500, 255 - color_value * 255 / 500)
        else:
            color = '#%02x%02x%02x' % ((color_value - 500) * 255 / 500, 255 - (color_value - 500) * 255 / 500, 0)

    else:
        color = '#%02x%02x%02x' % (255, 255, 255)

    return color

def matrix_replacevalue(matrix, value, x_coordinaten, y_coordinaten):
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

def update(om_matrix, calculation_matrix):
    '''
    update simulation window.
    First it cobines the matrixen after it updates the window2
    :return:
    '''
    global multiplier
    global sim_view  # impor simulatie window in def update ():

    matrix_width = len(om_matrix[0])
    matrix_height = len(om_matrix)
    max_point = 0

    for point_cal in calculation_matrix:
        if max(point_cal) > max_point:
            max_point = max(point_cal)

    for y in range(0, matrix_height, 1):
        for x in range(0, matrix_width, 1):
            point_cal = calculation_matrix[y][x]
            if om_matrix[y][x] is 1:
                sim_view.create_rectangle(x * multiplier - multiplier * 4 / 7, y * multiplier - multiplier * 4 / 7,
                                          x * multiplier + multiplier * 4 / 7, y * multiplier + multiplier * 4 / 7,
                                          fill='black', width=0)
            else:
                sim_view.create_rectangle(x * multiplier - multiplier * 4 / 7, y * multiplier - multiplier * 4 / 7,
                                          x * multiplier + multiplier * 4 / 7, y * multiplier + multiplier * 4 / 7,
                                          fill=color(calculation_matrix[y][x], max_point), width=0)

    sim_view.create_oval(startpoint[0] * multiplier - multiplier * 2 / 3, startpoint[1] * multiplier - multiplier * 2 / 3,
                         startpoint[0] * multiplier + multiplier * 2 / 3, startpoint[1] * multiplier + multiplier * 2 / 3,
                         fill='green', width=1)
    sim_view.create_oval(endpoint[0] * multiplier - multiplier * 2 / 3, endpoint[1] * multiplier - multiplier * 2 / 3,
                         endpoint[0] * multiplier + multiplier * 2 / 3, endpoint[1] * multiplier + multiplier * 2 / 3, fill='red',
                         width=1)

def setup_visual(matrix, calculation_matrix, stepmatrix, startpoint, stop):
    '''
    opzetten van de gui tijdes het brekenen van het path
    '''
    global sim_view

    calculation_matrix1 = calculation_matrix
    calculation_matrix1 = calculation_matrix

    simulatie_window = Toplevel()  # open scherm

    # bereken vermenigvuldigings factor voor scherm
    matrix_width = len(matrix[1])
    matrix_height = len(matrix)
    both_multi = [int(simulatie_window.winfo_screenwidth() / matrix_width),
                  int(simulatie_window.winfo_screenheight() / matrix_height)]
    multiplier = min(both_multi)

    simulatie_window.geometry(
        str(matrix_width * multiplier) + 'x' + str(matrix_height * multiplier))  # set dimention of screen
    sim_view = Canvas(simulatie_window, bg="white", width=matrix_width * multiplier,
                      height=matrix_height * multiplier)  # create canvas
    sim_view.place(x=0, y=0)
    update(matrix, calculation_matrix)

    def clock():
        global stepmatrix
        global calculation_matrix1

        a_algoritme(matrix, stepmatrix, calculation_matrix1)
        simulatie_window.after(200, clock)

    # run first time
    clock()
    simulatie_window.mainloop()

def a_algoritme(om_matrix, cal_matrix, stepmatrix):
    global start
    global end
    global starts
    global paths

    find = False

    if starts == True:
        paths = [startpoint]
        starts = False

    low_path = [0, 0, 1000000000000000000]  # lowest value of path [x,y,value]

    for value in paths:
        print value
        cal_value, stepmatrix = A_algorithm.A_cost(value, startpoint, endpoint, stepmatrix, om_matrix,
                                                   cal_matrix)  # calculate cost of path
        cal_matrix = matrix_replacevalue(cal_matrix, cal_value, value[0], value[1])  # zet calculatie value in matrix

        if cal_value < low_path[2]:
            low_path[0] = value[0]
            low_path[1] = value[1]
            low_path[2] = cal_value

    paths = A_algorithm.possible_paths(low_path[0:2])

    update(om_matrix, cal_matrix)

    return stepmatrix, cal_matrix