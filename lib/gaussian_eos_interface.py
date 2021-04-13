

def cube_preprocessor(file_name):
    print('cube file processing: ' + file_name + '.cube -> ' + file_name + '.pcube')
    with open(file_name+'.cube', mode='r') as gcf, open(file_name+'.pcube', mode='w') as pf:
        lines = [s.strip() for s in gcf.readlines()]
        atom_num = int(lines[2].split()[0])
        dimension = '3'
        x_num = int(lines[3].split()[0])
        y_num = int(lines[4].split()[0])
        z_num = int(lines[5].split()[0])

        # atom line skip
        line_num = 5 + atom_num

        pf.write(dimension + ' ' + str(x_num) + ' ' + str(y_num) + ' ' + str(z_num) + '\n')

        cube = [[[''] * z_num for y in range(y_num)] for x in range(x_num)]

        # read cube (Gaussian format)
        for i in range(x_num):
            for j in range(y_num):
                z_column = []
                for z_line in range(z_num // 6 + 1):
                    z_column.extend(lines[line_num].split())
                    line_num += 1
                cube[i][j] = z_column
        # write cube (Eos format)
        for i in range(z_num):
            for j in range(y_num):
                x_column = ''
                for k in range(x_num):
                    x_column += ' ' + cube[k][j][i]
                pf.write(x_column + '\n')
    print('')
