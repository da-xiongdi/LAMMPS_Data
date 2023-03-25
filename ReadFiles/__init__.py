path = "D:/document/00Study/01接触角摩擦力/计算/液滴/stage13.2/LGV-001-LL/ar-square-100-0.1575.profile"

buff_size = 1024 * 1024 * 512

with open(path, "r") as f:
    buff = f.read(buff_size)
    i = 1
    while len(buff) > 0:
        save_path = "D:/document/00Study/01接触角摩擦力/计算/液滴/stage13.2/LGV-001-LL/ar-%s-square-100-0.1575.profile" % i
        with open(save_path, "w") as fw:
            fw.write(buff)
        i += 1
        buff = f.read(buff_size)
