import os

current_directory = __file__
file_name = "7.txt"
file_path = os.path.join(current_directory + "/../", file_name)


codes = []
variables = dict()


def set_var(name, type, val=""):
    if variables.get(name, False):
        print("ERROR variable", name, "is defined already")
    else:
        variables[name] = [type, val]


def doMath(exp):
    if isinstance(exp, int):
        return exp
    elif len(exp) < 3:
        # print("len is small", exp, len(exp))
        return exp
    result = ["", "", ""]
    i = 0
    for ch in exp:
        if ch not in ["+", "-", "*", "/", "%"]:
            result[i] += ch
        else:
            i += 1
            result[i] += ch
            i += 1
        if i > 2:
            return exp
    a = result[0]
    b = result[1]
    c = result[2]

    # print("variables[a] =>", variables)
    if variables.get(a, None) is not None:
        val1 = float(variables[a][1])
    elif a.isdigit():
        val1 = int(a)
    elif "." in a:
        val1 = float(a)
    else:
        print(f"Err1: variable is {a} not defined")

    if variables.get(c, None) is not None:
        val2 = float(variables[c][1])
    elif c.isdigit():
        val2 = int(c)
    elif "." in c:
        val2 = float(c)
    else:
        print(f"Err2: variable is {c} not defined")

    # print("doMath=>", val1, b, val2)
    if b == "+":
        return val1 + val2
    elif b == "-":
        return val1 - val2
    elif b == "*":
        return val1 * val2
    elif b == "/":
        return val1 / val2
    elif b == "%":
        return val1 % val2
    else:
        print("Unknown Operation =>", b)
        exit(1)


def translate_var(exp: str):
    # print("translate_var =>", variables)
    # print("translate_var =>", exp)
    if isinstance(exp, int):
        return exp
    if isinstance(exp, float):
        return int(exp)
    if exp[0].isalnum():
        ee = doMath(exp)
    else:
        if ("'" in exp) or ('"' in exp):
            return exp[1:-1]
        return exp
    # print("translate_var after math =>", ee)
    if isinstance(ee, float):
        return int(ee)
    if isinstance(ee, int):
        return ee
    if ("'" in ee) or ('"' in ee):
        return ee[1:-1]
    if variables.get(exp, False):
        var = variables.get(exp)
        type = var[0]
        val = var[1]
        if type == "integer":
            val = int(val)
    else:
        val = ee

    return val


def resolve_cond(operand1: str, operator, operand2):
    # print('resolve_cond',operand1, operator, operand2)
    operand1 = translate_var(operand1)
    operand2 = translate_var(operand2)
    if ">=" == operator:
        return int(operand1) >= int(operand2)
    if "<=" == operator:
        return int(operand1) <= int(operand2)
    if ">" == operator:
        return int(operand1) > int(operand2)
    if "<" == operator:
        return int(operand1) < int(operand2)
    if "==" == operator:
        return int(operand1) == int(operand2)
    return True


def update_val_for_var(var, val):
    # print("update_val_for_var =>", var, val)
    val = translate_var(val)
    old_val = variables[var]
    old_val[1] = val
    # print("update_val_for_var old_val =>", old_val)
    variables.update({var: old_val})


def run_code(lines: list[list[str]], start_number=-1, show_output=True, depth=0):
    # print(start_number, show_output,sep="$$")
    var_flag = False
    is_main = start_number == -1
    # if is_main:
    #     print(lines)
    # print("start_number=>",start_number)
    for line_number, line in enumerate(lines):
        # print("line_number=>",line_number,depth)
        # print("line=>",line)
        if line_number < start_number:
            # print("ignore start_number=>",start_number)
            continue
        if line[0] == "var":
            var_flag = True
        elif line[0] == "begin":
            var_flag = False
        elif var_flag:
            set_var(line[0], line[2])
        elif line[0] == "for":
            # print("for line:", line)
            a = int(translate_var(line[3]))
            b = int(translate_var(line[5]))
            if line[4] == "to":
                c = 1
            else:
                c = -1
            for i in range(a, b + c, c):
                update_val_for_var(line[1], i)
                # print("run_code for=>",line_number , show_output,depth+1,'$$',line[1], i)
                lines, start_number = run_code(
                    lines, line_number + 1, show_output, depth + 1
                )
                # if is_main:
                #     print(i,a,b,c,lines)

        elif line[0] == "if":
            a = line.index("(")
            line.reverse()
            r_line = line.copy()
            line.reverse()
            b = len(line) - r_line.index(")")
            # print("if block:",line,a,b)
            if a + 5 == b:
                do_if = resolve_cond(line[a + 1], line[a + 2], line[a + 3])
                # print("run_code if=>",line_number + 1, do_if)
                lines, start_number = run_code(lines, line_number + 1, do_if, depth + 1)
                # if is_main:
                #     print(i,a,b,c,lines)
            else:
                print("ERROR IN IF BLOCK")
                exit(1)

        elif line[0] == "end" and len(lines[line_number]) == 1:
            lines[line_number].append(depth)
            # print("end =>",line_number,lines[line_number],lines[line_number-1],lines[line_number-2],depth)
            return lines, line_number
        elif line[0] == "end" and lines[line_number][1] == depth:
            # print("end=>",line_number,lines[line_number],lines[line_number-1],lines[line_number-2],depth)
            return lines, line_number
        elif line[0] == "end.":
            break
        elif line[0] == "readln":
            if show_output:
                print("enter input:")
                input()
        elif line[0] == "writeln":
            # print("writeln=>",start_number,line_number,lines[line_number-1],depth)
            txt = translate_var(line[2])
            if txt == ")":
                txt = ""
            if show_output:
                print(txt)
        elif line[0] == "write":
            if show_output:
                # print("write line:",line,is_main,start_number,line_number)
                pp = translate_var(line[2])
                print(pp, end="")
        elif line[1] == ":=":
            # print(line)
            p2 = "".join(line[2:])
            # print("p2=>",p2)
            update_val_for_var(line[0], doMath(p2))
        else:
            # print("no code=>", line)
            pass


line_number = 1

depth = 0
depth_type = []
code_depth = dict()
# print(variables)
order = 1
lines = []
words = []
in_qoute = False
h = ""
oh = ""
inqoute = ""
then_flag = False
with open(file_path, "r") as f:
    code = f.read()
    for ch in code:
        if (oh == "writeln" or oh == "write") and len(words) > 3:
            then_flag = True
            if len(words) > 0:
                lines.append(words.copy())
                words.clear()
            if ch == "l":
                oh += ch
            else:
                if oh != "":
                    words.append(oh)
                oh = ""
                words.append(ch)
            continue
        if ch == "\n" or ch == ";":
            if h != "":
                words.append(h)
                h = ""
            if oh != "":
                words.append(oh)
                oh = ""
            if len(words) > 0:
                lines.append(words.copy())
                words.clear()
                if then_flag:
                    lines.append(["end"])
                    then_flag = False
            continue
        if in_qoute and ch not in ["'", '"']:
            inqoute += ch
        elif ch in ["'", '"']:
            inqoute += ch
            if in_qoute:
                words.append(inqoute)
                inqoute = ""
                in_qoute = False
            else:
                in_qoute = True
        elif ch in [":", "=", ">"]:
            if oh != "":
                words.append(oh)
                oh = ""
            h += ch
        elif ch not in [":", "=", ")", "(", "+", "-", "*", "/", ";"]:
            if h != "":
                words.append(h)
                h = ""
            if ch == " ":
                if oh != "":
                    words.append(oh)
                oh = ""
            else:
                oh += ch
        else:
            if h != "":
                words.append(h)
                h = ""
            if oh != "":
                words.append(oh)
                oh = ""
            words.append(ch)

    # print("lines", lines)

    run_code(lines)

    # print(variables)
    # print(code_depth)
