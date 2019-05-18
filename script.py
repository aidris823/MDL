import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print symbols

    for command in commands:
        print command
        co = command['op']
        arguments = command['args']
        if co == "push":
            stack.append([i[:] for i in stack[-1]])
        elif co == "pop":
            stack.pop()
        elif co == "line":
            add_edge(tmp, arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])
            matrix_mult(stack[-1], tmp)
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif co == "move":
            tmp = make_translate(arguments[0],arguments[1],arguments[2])
            matrix_mult(stack[-1],tmp)
            stack[-1] = [i[:] for i in tmp]
            tmp = []
        elif co == "rotate":
            tmp = new_matrix()
            theta = arguments[1] * (math.pi / 180)

            if arguments[0] == 'x':
                tmp = make_rotX(theta)
            elif arguments[0] == 'y':
                tmp = make_rotY(theta)
            elif arguments[0] == 'z':
                tmp = make_rotZ(theta)
            stack[-1] = [i[:] for i in tmp]
            tmp = []
        elif co == 'scale':
            tmp = make_scale(arguments[0], arguments[1], arguments[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [i[:] for i in tmp]
        elif co == 'box':
            add_box(tmp, arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])
            matrix_mult(stack[-1],tmp)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        elif co == 'sphere':
            add_sphere(tmp, arguments[0], arguments[1], arguments[2], arguments[3], step_3d)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif co == 'torus':
            add_torus(tmp, arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], step_3d)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif co == 'save':
            save_extension(screen, arguments[0])
        elif co == 'display':
            display(screen)
        else:
            pass
