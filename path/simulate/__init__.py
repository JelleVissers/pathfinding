import pygame, sys
import math
from path import set
from pygame.locals import *
import tkMessageBox


def matrix_replacevalue(matrix, value, x_coordinaten, y_coordinaten):
    '''
    verander waarde 0 naar 1 op gegeven positie in matrix
    '''
    widht = len(matrix[0])
    height = len(matrix)
    test_matrix = []

    for y in range(0, height, 1):
        X_line = []
        for x in range(0, widht, 1):
            if x == x_coordinaten and y == y_coordinaten:
                X_line = X_line + [value]
            else:
                X_line = X_line + [matrix[y][x]]
        test_matrix = test_matrix + [X_line]

    return test_matrix


def color_cal(value, min, max):
    '''
    berekend de kleuren aan de hand van de huidige waarde van het punt en de maximale waarde van de matrix
    :param value:   Huidige waarde van punt
    :param max:     Maximale waarde in matrix
    :return: coler value
    '''
    # print min,max,value

    if value is not 0:
        color_value = ((value - min) / (max - min)) * 1000
        if color_value < 500:
            color = (0, color_value * 255 / 500, 255 - color_value * 255 / 500)
        else:
            color = ((color_value - 500) * 255 / 500, 255 - (color_value - 500) * 255 / 500, 0)
    else:
        color = (255, 255, 255)

    return color


def possible_coordinaten(coordinaten):
    '''
    search for possible paths
    :param coordinaten: coordinaten of searche point
    :return: list of posible coordinaten [[X0,Y0][X1,Y1]]
    '''

    possible_coordinaten = []
    possible_coordinaten = possible_coordinaten + [[coordinaten[0] + 1, coordinaten[1] + 1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0], coordinaten[1] + 1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0] - 1, coordinaten[1] + 1]]

    possible_coordinaten = possible_coordinaten + [[coordinaten[0] + 1, coordinaten[1]]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0], coordinaten[1]]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0] - 1, coordinaten[1]]]

    possible_coordinaten = possible_coordinaten + [[coordinaten[0] + 1, coordinaten[1] - 1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0], coordinaten[1] - 1]]
    possible_coordinaten = possible_coordinaten + [[coordinaten[0] - 1, coordinaten[1] - 1]]

    return possible_coordinaten


def filter_coordinaten(coordinaten, omgevingsmatrix, calculatiematrix):
    '''
    Mogelijke coordinaten dat er
    :param coordinaten:
    :param omgevingsmatrix:
    :param calculatiematrix:
    :return: possebility [false,true]
    '''

    point_calculatie = calculatiematrix[coordinaten[1]][coordinaten[0]]
    point_omgeving = omgevingsmatrix[coordinaten[1]][coordinaten[0]]

    possible = False

    if point_calculatie == 0 and point_omgeving == 0: possible = True
    if coordinaten[0] < 0 or coordinaten[0] > len(omgevingsmatrix[0]): possible = False
    if coordinaten[1] < 0 or coordinaten[1] > len(omgevingsmatrix): possible = False

    return possible


def filtering_coordinaten(coordinatenlist, omgevingsmatrix, calculatiematrix):
    coordinaten = []

    for coordinaat in coordinatenlist:
        if filter_coordinaten(coordinaat, omgevingsmatrix, calculatiematrix):
            coordinaten = coordinaten + [coordinaat]
    return coordinaten


def return_lowest_step(coordinaten, stepmatrix, start):
    '''
    calculate lose number of steps to go to point
    :param coordinaten: coordinates of node
    :param stepmatrix: mastrix with number of steps
    :return: stepmatrix, lowest possseble number of steps.
    '''
    pos_cor_list = possible_coordinaten(coordinaten)
    lowest_step = 10000000000000
    lowest_cor = None

    for pos_cor in pos_cor_list:
        if stepmatrix[pos_cor[1]][pos_cor[0]] == 0:
            if pos_cor == start:
                lowest_step = 1
        else:
            if stepmatrix[pos_cor[1]][pos_cor[0]] < lowest_step:
                lowest_step = stepmatrix[pos_cor[1]][pos_cor[0]] + 1

    stepmatrix = matrix_replacevalue(stepmatrix, lowest_step, coordinaten[0], coordinaten[1])

    return stepmatrix


def dijkstra(coordinaten, stepmatrix, calculatiematrix, end):
    g = stepmatrix[coordinaten[1]][coordinaten[0]]

    calculatiematrix = matrix_replacevalue(calculatiematrix, g, coordinaten[0], coordinaten[1])

    return calculatiematrix, g


def update_screen(DISPLAY, factor, omg_matrix, cal_matrix, step_matrix, start, stop):
    DISPLAY.fill((255, 255, 255))  # leeg scherm

    # afmetingen van de matrix binnen halen
    matrix_width = len(omg_matrix[0])
    matrix_height = len(omg_matrix)

    cal_max = 0
    cal_min = 100000000

    # bereken maximale waarde step_matrix
    for lines_y in cal_matrix:
        for x in lines_y:
            if x is not 0:
                if x < cal_min: cal_min = x

            if x is not 100000000:
                if x > cal_max: cal_max = x

    for y in range(0, matrix_height, 1):
        for x in range(0, matrix_width, 1):
            if omg_matrix[y][x] == 1:
                pygame.draw.rect(DISPLAY, (0, 0, 0), (x * factor - factor / 2, y * factor - factor / 2, factor, factor))
            else:
                pygame.draw.rect(DISPLAY, color_cal(cal_matrix[y][x], cal_min, cal_max),
                                 (x * factor - factor / 2, y * factor - factor / 2, factor, factor))

    # draw start point
    pygame.draw.circle(DISPLAY, (0, 0, 0), (start[0] * factor, start[1] * factor), int(factor * 1.2))
    pygame.draw.circle(DISPLAY, (0, 255, 0), (start[0] * factor, start[1] * factor), int(factor))

    # draw stop point
    pygame.draw.circle(DISPLAY, (0, 0, 0), (stop[0] * factor, stop[1] * factor), int(factor * 1.2))
    pygame.draw.circle(DISPLAY, (255, 0, 0), (stop[0] * factor, stop[1] * factor), int(factor))


def find_lowestvalue(matrix, start):
    lowest_value = 1000000000000
    coordinaten = None

    width = len(matrix[0])
    height = len(matrix)

    for y in range(0, height, 1):
        for x in range(0, width, 1):
            if matrix[y][x] is not 0:
                if matrix[y][x] < lowest_value:
                    lowest_value = matrix[y][x]
                    coordinaten = [x, y]

    if coordinaten == None:
        # print "first run"
        coordinaten = start

    return coordinaten


def other_coordinaten(calcultionmatrix, omgevingsmatrix, start):
    low_high_coordinaten = []  # [[x0,y0,value],[x1,y1,value]]

    # make list with lowest values from low to high
    for y in range(0, len(calcultionmatrix), 1):
        for x in range(0, len(calcultionmatrix[0]), 1):
            copie_coordinaten = []
            found = False
            value = calcultionmatrix[y][x]
            if value is not 0:
                if len(low_high_coordinaten) == 0:
                    low_high_coordinaten = low_high_coordinaten + [[x, y, value]]
                else:
                    for coordinaten in low_high_coordinaten:
                        if coordinaten[2] < value or found == True:
                            copie_coordinaten = copie_coordinaten + [coordinaten]
                        else:
                            copie_coordinaten = copie_coordinaten + [[x, y, value]] + [coordinaten]
                            found = True
                    low_high_coordinaten = copie_coordinaten

    remove_value_list = []

    # print "possebilitys-1: " + str(len(low_high_coordinaten))

    for coordinaten in low_high_coordinaten:
        remove_value_list = remove_value_list + [[coordinaten[0], coordinaten[1]]]
    low_high_coordinaten = remove_value_list

    # print "possebilitys-2 : " + str(len(low_high_coordinaten))

    x = 0
    for coordinaten in low_high_coordinaten:
        pos_cor = possible_coordinaten(coordinaten)
        pos_cor_list = filtering_coordinaten(pos_cor, omgevingsmatrix, calcultionmatrix)

        if len(pos_cor_list) is not 0:
            return pos_cor_list


def printmatrix(matrix):
    for line in matrix:
        print line


def calculate(omgevingsmatrix, calcultionmatrix, stepmatrix, start, stop):
    '''
    :param omgevingsmatrix: matrix reprensentatie omgeving
    :param calcultionmatrix:  matrix met berkende waarde
    :param stepmatrix:  maatrix met aantal stappen van strart tot node
    :param start: coordinaten startpunt
    :param stop: coordinaten eindpunt
    :return: omgevingsmatrix,calculationmatrix,stepmatrix
    '''

    firts_coordinaten = find_lowestvalue(calcultionmatrix, start)
    # print "first coordinend: "+str(firts_coordinaten)

    non_fil_coor_list = possible_coordinaten(firts_coordinaten)
    filter_coord_list = filtering_coordinaten(non_fil_coor_list, omgevingsmatrix, calcultionmatrix)

    # print "number of possible coordinaten : "+ str(len(filter_coord_list))

    if len(filter_coord_list) == 0:
        filter_coord_list = other_coordinaten(calcultionmatrix, omgevingsmatrix, start)

    # print filter_coord_list
    for coordinaat in filter_coord_list:
        stepmatrix = return_lowest_step(coordinaat, stepmatrix, start)
        calcultionmatrix, value = dijkstra(coordinaat, stepmatrix, calcultionmatrix, stop)

    return omgevingsmatrix, calcultionmatrix, stepmatrix


def simulate(omgevingsmatrix, start, stop, updatesize=1):
    '''
    berkend en visuwaliseert path doormiddel van het A* algorithme
    :param omgevingsmatrix: matrix van de omgeving
    :param start: coordinaten van startpunt [x,y]
    :param stop:  coordinaten van eindpunt [x,y]
    :return:
    '''

    calculation_matrix = set.creat_matrix(len(omgevingsmatrix[0]),
                                          len(omgevingsmatrix))  # maak matrix aan voor het opslaan van de gegevens
    step_matrix = set.creat_matrix(len(omgevingsmatrix[0]),
                                   len(omgevingsmatrix))  # maak matrix aan voor het opslaan van de gegeven

    pygame.init()

    # berekenen van de germenigingsvuldigingsfactor voor de breedte en hoogte van het scherm
    screen_info = pygame.display.Info()
    ver_widt = int(math.floor(screen_info.current_w / len(omgevingsmatrix[0])))
    ver_height = int(math.floor(screen_info.current_h / len(omgevingsmatrix)))

    if ver_widt < ver_height:
        ver_factor = ver_widt
    else:
        ver_factor = ver_height

    DISPLAY = pygame.display.set_mode((len(omgevingsmatrix[0]) * ver_factor, len(omgevingsmatrix) * ver_factor),FULLSCREEN | DOUBLEBUF, 8)
    pygame.event.set_allowed([QUIT, K_ESCAPE, K_TAB])

    pygame.display.set_caption("simulate simple search algorithm")
    DISPLAY.fill((255, 255, 255))
    frameteller = 0
    found = False

    while True:
        try:
            # print frameteller
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.display.set_mode((len(omgevingsmatrix[0]) * ver_factor, len(omgevingsmatrix) * ver_factor))
            if keys[K_TAB]:
                pygame.display.set_mode((len(omgevingsmatrix[0]) * ver_factor, len(omgevingsmatrix) * ver_factor),
                                        FULLSCREEN | DOUBLEBUF, 32)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            for x in range(0, updatesize, 1):
                if found == False:
                    frameteller = frameteller + 1
                    omgevingsmatrix, calculation_matrix, step_matrix = calculate(omgevingsmatrix, calculation_matrix,
                                                                                 step_matrix, start, stop)
                    if calculation_matrix[stop[1]][stop[0]] is not 0:
                        found = True
                        pygame.display.set_mode(
                            (len(omgevingsmatrix[0]) * ver_factor, len(omgevingsmatrix) * ver_factor))
                        update_screen(DISPLAY, ver_factor, omgevingsmatrix, calculation_matrix, step_matrix, start,
                                      stop)
                        printmatrix(calculation_matrix)
                        tkMessageBox._show("Found", "Endpoint found after " + str(frameteller) + " iteration")
        except:
            pygame.display.set_mode((len(omgevingsmatrix[0]) * ver_factor, len(omgevingsmatrix) * ver_factor))
            tkMessageBox.showerror("File error", " not pisseble to simulate")
            pygame.quit()

        update_screen(DISPLAY, ver_factor, omgevingsmatrix, calculation_matrix, step_matrix, start, stop)
        pygame.display.update()
