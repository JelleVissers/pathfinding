from path import open
from path import set

def main():
    matrixfile  = open.import_file()
    matrix  = open.get_matrix(matrixfile)
    set.printmatrix(matrix)
    print"\n"
    print open.get_startpoint(matrixfile)
    print open.get_endpoint(matrixfile)

if __name__ == '__main__':
    main()