def save_files(boy, girl, count):
    boy_file_name = r'D:\boy_file_' + str(count) + '.txt'
    girl_file_name = r'D:\girl_file_' + str(count) + '.txt'
    f1 = open(boy_file_name, 'w')
    f1.writelines(boy)
    f2 = open(girl_file_name, 'w')
    f2.writelines(girl)
    f1.close()
    f2.close()


def file_split(filename):
    boy = []
    girl = []
    count = 1

    f = open(filename)

    for each_line in f:
        if each_line[:6] != '======':
            '''print each_line.split(':',1)'''
            (role, line_spoke) = each_line.split(':', 1)
            if role == '小甲鱼':
                boy.append(line_spoke)
            if role == '小客服':
                girl.append(line_spoke)
        else:
            save_files(boy, girl, count)
            boy = []
            girl = []
            count += 1

    save_files(boy, girl, count)

    f.close()


file_split(r'D:\record.txt')
