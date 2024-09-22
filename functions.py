import random
import math
from fractions import Fraction


class Functions(object):
    # 运算符列表
    operators = ['+', '-', '×', '÷', 'x']

    numb = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',']

    data = []

    # 随机生成整数
    def random_number(self, max_num):
        return str(random.randint(1, 10))

    # 随机生成运算符
    def random_operator(self):
        return random.choice(Functions.operators)

    # 生成随机的后缀表达式
    def generate_expression(self, max_num):
        stack = []
        # 随机生成表达式的长度
        for i in range(random.randint(3, 10)):
            if len(stack) >= 2:
                # 随机选择两种操作：加入一个操作符或者进行一次运算
                if random.randint(0, 1) == 1:
                    # 随机选择一个运算符
                    operator = Functions.random_operator(self)
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    # 确保除数不为0
                    if operator == '÷' and operand2 == '0':
                        operand2 = Functions.gen_number(self, max_num)
                    stack += [operand1, operand2, operator]
                else:
                    # 添加一个操作数
                    # 确保相邻的操作数之间有运算符
                    if isinstance(stack[-1], str):
                        stack.append(Functions.random_operator(self))
                    stack.append(Functions.gen_number(self, max_num))
            else:
                # 第一个操作数
                stack.append(Functions.gen_number(self, max_num))
        # 确保最后一个元素不为操作符
        if isinstance(stack[-1], str):
            stack.pop()
        return stack

    # 处理后缀表达式，便于转换和计算结果
    def get_hou(self, expr):
        expression = []
        for item in expr:
            if isinstance(item, list):
                expression.append(item[2])
            else:
                expression.append(item)
        return expression

    # 预处理中缀表达式
    def first(self, expr):
        expression = ''
        for i in expr:
            if i == '/':  # 将分数的"/"号换为"，"，方便拼成分数函数
                expression += ','
            else:
                expression += i
        return expression

    # 转换×运算符，方便计算结果
    def tranc(self, expr):
        formul2 = ''
        formul1 = expr
        for i in formul1:
            if i == '×' or i == 'x':  # 将"×"号换为"*"
                j = '*'
                formul2 += j
            else:
                formul2 += i
        return formul2

    # 转换÷运算符，方便计算结果
    def tranz(self, expr):
        formul2 = ''
        formul1 = expr
        for i in formul1:
            if i == '÷':  # 将处理好的表达式的"÷"号换为"/"
                j = '/'
                formul2 += j
            else:
                formul2 += i
        return formul2

    # 计算运算结果
    def get_ans(self, expr, note=1):
        frac = "Fraction("
        if note == 1:  # 生成表达式时使用
            infix_expression = Functions.to_show_infix(self, expr)  # 后缀转中缀
            expression = infix_expression[0]
        else:  # 读取表达式时使用
            expression = expr
        # print("中缀表达式：", infix_expression)
        formul1 = Functions.tranc(self, expression)  # x换成*
        # print(formul1)
        formul1 = Functions.first(self, formul1)  # 分数的/换,
        formul2 = ''
        flag = 0
        length = len(formul1)
        for i in range(length):  # 将带分数的‘换为+
            if formul1[i] == "'":
                formul2 += '+'
                continue
            if formul1[i] not in Functions.numb and formul1[i] != "'":
                formul2 += formul1[i]
                continue
            if formul1[i] in Functions.numb and formul1[i - 1] not in Functions.numb:  # 读取到的数拼接成分数函数，并看情况加括号
                formul2 = formul2 + '(' + frac + formul1[i]
                if formul1[i + 1] not in Functions.numb and formul1[i + 1] != "'":
                    formul2 = formul2 + ')' + ')'
                elif formul1[i + 1] not in Functions.numb and formul1[i + 1] == "'":
                    formul2 += ')'
                    flag = 1
                continue
            elif formul1[i] in Functions.numb:
                formul2 = formul2 + formul1[i]
                if formul1[i + 1] not in Functions.numb and formul1[i + 1] != "'":
                    if flag == 1:
                        formul2 = formul2 + ')' + ')' + ')'
                        flag = 0
                    else:
                        formul2 = formul2 + ')' + ')'
                elif formul1[i + 1] not in Functions.numb and formul1[i + 1] == "'":
                    formul2 = formul2 + ')'
                    flag = 1
                continue
        formul2 = Functions.tranz(self, formul2)  # ÷换成/
        # print(formul2)
        ans = eval(formul2)
        return ans

    def fen_tran(self, operand):
        if operand[1] == 0:
            return str(operand[0])
        else:
            return f"({operand[1]}'{operand[0]})"

    # 处理后缀表达式，便于转换与显示
    def get_show_hou(self, expr):
        expression = []
        for item in expr:
            if isinstance(item, list):
                expression.append(Functions.fen_tran(self, item))
                # if item[1] == 0
                #     expression.append(item[0])
                # else:
                #     expression.append(item[0])
            else:
                expression.append(item)
        return expression

    # 将后缀表达式转换为中缀表达式
    def to_show_infix(self, expr):
        expression = Functions.get_show_hou(self, expr)
        stack = []
        for token in expression:
            if token in Functions.operators:
                if len(stack) >= 2:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    # 添加括号，保证运算顺序
                    stack.append(f"({operand1} {token} {operand2})")
                else:
                    operand = stack.pop()
                    if len(stack) > 0 and isinstance(stack[-1], list):
                        # 将操作数添加到前一个表达式中
                        stack[-1].append(token)
                        stack[-1].append(operand)
                    elif len(stack) > 0:
                        # 两个操作数和一个运算符组成一个表达式
                        stack.append([stack.pop(), token, operand])
                    else:
                        # 第一个操作数
                        stack.append(operand)
            else:
                # 操作数入栈
                stack.append(token)
        if len(stack) == 1 and isinstance(stack[0], list):
            # 如果只有一个表达式，则返回这个表达式
            stack = stack[0]
        return stack

    # 显示题目
    def show_zhong(self, expr):
        infix_expression = Functions.to_show_infix(self, expr)
        # print("中缀表达式：", infix_expression)
        formul = infix_expression[0]
        if formul[0] == '(' and formul[-1] == ')':  # 去掉最外层括号
            formul = formul[1:-1]
        return formul

    # 转换x÷运算符
    def trans(self, expr):
        formul2 = ''
        formul1 = expr
        for i in formul1:
            if i == '×':
                j = '*'
                formul2 += j
            elif i == '÷':
                j = '/'
                formul2 += j
            else:
                formul2 += i
        return formul2

    # 生成真分数
    def gen_fraction(self, max_num, min_num=1):
        numerator = random.randint(min_num, max_num)
        denominator = random.randint(min_num, max_num)
        fig = numerator / denominator
        while fig >= max_num:  # 检查数值是否太大
            numerator = numerator // 2
            fig = numerator / denominator
        while numerator == denominator or numerator % denominator == 0:  # 检查分子分母是否相等
            numerator = random.randint(min_num, max_num)
            denominator = random.randint(min_num, max_num)
            fig = numerator / denominator
            while fig >= max_num:
                numerator = numerator // 2
                fig = numerator / denominator
        # 转化为带分数
        if numerator > denominator:
            figure = Fraction(numerator, denominator)
            integer = numerator // denominator
            numerator = numerator % denominator
            # print(numerator,denominator,'\n')
            num = Fraction(numerator, denominator)
            return [num, integer, figure]
        else:
            num = Fraction(numerator, denominator)
            return [num, 0, num]

    # 生成一个随机数，或者是一个真分数
    def gen_number(self, max_num, min_num=1):
        if random.random() < 0.6:
            num = random.randint(min_num, max_num)
            num = Fraction(num)
            return [num, 0, num]
        else:
            return Functions.gen_fraction(self, max_num)

    def gen_writ(self, exercfile, ansfile, times, max_num):
        for i in range(times):
            flag = 0
            while flag == 0:
                # 生成随机的后缀表达式
                expression = Functions.generate_expression(self, max_num)
                while expression in Functions.data:
                    expression = Functions.generate_expression(self, max_num)
                Functions.data.append(expression)
                # 将后缀表达式转换为中缀表达式
                infix_expression = Functions.to_show_infix(self, expression)
                for item in infix_expression[0]:
                    if item in Functions.operators:
                        flag = 1
            ans = Functions.get_ans(self, expression)

            while ans < 0:  # 结果小于0，重新生成
                flag = 0
                while flag == 0:
                    # 生成随机的后缀表达式
                    expression = Functions.generate_expression(self, max_num)
                    while expression in Functions.data:
                        expression = Functions.generate_expression(self, max_num)
                    Functions.data.append(expression)
                    # 将后缀表达式转换为中缀表达式
                    infix_expression = Functions.to_show_infix(self, expression)
                    for item in infix_expression[0]:  # 生成表达式不正确，重新生成
                        if item in Functions.operators:
                            flag = 1
                ans = Functions.get_ans(self, expression)
            text = Functions.show_zhong(self, expression)
            exercfile.write("{}. ".format(i + 1))
            exercfile.write(text + '\n')
            ansfile.write("{}. ".format(i + 1))
            ans = Functions.get_ans(self, expression)
            # print(ans)
            ansfile.write(str(ans) + '\n')

        print("题目和答案已生成写入文档，分别为Exercises.txt，Answers.txt")
        return 0

    def check(self, f1, f2):
        text1 = 'Correct:'
        text2 = 'Wrong:'
        list1 = "("
        list2 = "("
        num1 = 0
        num2 = 0
        count = 0
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        for l1, l2 in zip(lines1, lines2):
            count += 1
            s1 = l1.strip()
            s2 = l2.strip()
            s1 = '(' + s1[len(str(count)) + 2:] + ')'
            s2 = s2[len(str(count)) + 2:]
            ans = str(Functions.get_ans(self, s1, 0))
            if ans == s2:
                num1 += 1
                list1 = list1 + str(count) + ', '
            else:
                num2 += 1
                list2 = list2 + str(count) + ', '
        if list1[-1] == " " and list1[-2] == ',':
            list1 = list1[:-2]
        if list2[-1] == "," and list2[-2] == ' ':
            list2 = list2[:-2]
        text1 = text1 + ' ' + str(num1) + ' ' + list1 + ")"
        text2 = text2 + ' ' + str(num2) + ' ' + list2 + ")"
        respon = open('Grade.txt', 'w').close()
        respon = open('Grade.txt', 'w')
        respon.write(text1 + '\n')
        respon.write(text2 + '\n')
        print("作答情况已导入文件Grade.txt")
        respon.close()
        return 0

