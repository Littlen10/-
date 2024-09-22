from functions import *


function = Functions()
temp = input("请输入“-n 参数”控制生成题目的个数\n或输入”-e <exercisefile>.txt -a <answerfile>.txt“批改作答:")

while (temp[1] != 'n' and temp[1] != 'e') or len(temp) <= 4:  # 检测命令是否输入正确
    print("输入命令错误")
    temp = input("请输入“-n 参数”控制生成题目的个数\n或输入”-e <exercisefile>.txt -a <answerfile>.txt“批改作答:")

if temp[0] == '-' and temp[1] == 'n':
    times = eval(temp[3:])
    while times < 1:
        temp = input("输入参数错误，参数需不小于1\n请输入“-n 参数”控制生成题目的个数")
        times = eval(temp[3:])
    num = input("请输入“-r 参数”控制题目中数值的范围")
    if num[0] == '-' and num[1] == 'r' and len(num) >= 4:  # 检测参数是否输入正确
        max_num = eval(num[3:])
    else:
        max_num = -1
    while num[0] != '-' or num[1] != 'r' or max_num < 1:  # 检测命令或参数是否输入正确
        print("输入命令或参数错误")
        num = input("请输入“-r 参数”控制题目中数值的范围")
        if num[0] == '-' and num[1] == 'r' and len(num) >= 4:
            max_num = eval(num[3:])

    exerc = open('Exercises.txt', 'w').close()
    exerc = open('Exercises.txt', 'w')
    ans = open('Answers.txt', 'w').close()
    ans = open('Answers.txt', 'w')

    function.gen_writ(exerc, ans, times, max_num)

    exerc.close()
    ans.close()

elif temp[0] == '-' and temp[1] == 'e':
    while temp.find('-a') == -1 or (temp[0] != '-' and temp[1] != 'e') or len(temp) <= 6:  # 检测命令是否输入正确
        temp = input("输入命令错误\n请输入”-e <exercisefile>.txt -a <answerfile>.txt:“")

    s_split = temp[3:]
    s_split = s_split.split(' -a ')
    address1 = s_split[0]
    address2 = s_split[1]
    exercfile = open(address1, 'r', encoding="utf-8")
    ansfile = open(address2, 'r', encoding="utf-8")
    function.check(exercfile, ansfile)
    exercfile.close()
    ansfile.close()
