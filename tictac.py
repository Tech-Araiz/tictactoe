lg=[[".",".","."],[".",".","."],[".",".","."]]
count=0
go=True
def show():
    for i in lg:
        print(i)
def win_check_X():
    global go
    if lg[0][0]=="X" and lg[1][0]=="X" and lg[2][0]=="X":
        print("X wins")
        go=False   
    elif lg[0][0]=="X" and lg[0][1]=="X" and lg[0][2]=="X":
        print("X wins")
        go=False
    elif lg[0][0]=="X" and lg[1][1]=="X" and lg[2][2]=="X":
        print("X wins")
        go=False
    elif lg[1][0]=="X" and lg[1][1]=="X" and lg[1][2]=="X":
        print("X wins")
        go=False
    elif lg[2][0]=="X" and lg[2][1]=="X" and lg[2][2]=="X":
        print("X wins")
        go=False
    elif lg[2][0]=="X" and lg[1][1]=="X" and lg[0][2]=="X":
        print("X wins")
        go=False
    elif lg[0][1]=="X" and lg[1][1]=="X" and lg[2][1]=="X":
        print("X wins")
        go=False
    elif lg[0][2]=="X" and lg[1][2]=="X" and lg[2][2]=="X":
        print("X wins")
        go=False
def win_check_zero():
    global go
    if lg[0][0]=="0" and lg[1][0]=="0" and lg[2][0]=="0":
        print("0 wins")
        go=False   
    elif lg[0][0]=="0" and lg[0][1]=="0" and lg[0][2]=="0":
        print("0 wins")
        go=False
    elif lg[0][0]=="0" and lg[1][1]=="0" and lg[2][2]=="0":
        print("0 wins")
        go=False
    elif lg[1][0]=="0" and lg[1][1]=="0" and lg[1][2]=="0":
        print("0 wins")
        go=False
    elif lg[2][0]=="0" and lg[2][1]=="0" and lg[2][2]=="0":
        print("0 wins")
        go=False
    elif lg[2][0]=="0" and lg[1][1]=="0" and lg[0][2]=="0":
        print("0 wins")
        go=False
    elif lg[0][1]=="0" and lg[1][1]=="0" and lg[2][1]=="0":
        print("0 wins")
        go=False
    elif lg[0][2]=="0" and lg[1][2]=="0" and lg[2][2]=="0":
        print("0 wins")
        go=False
def win_check():
    win_check_zero()
    win_check_X()


show()

while(go):
    if count%2==0:
        print("<<<<Player 1's Turn>>>>")
    else:
        print("<<<<Player 2's Turn>>>>")
    row= int(input("input the row:"))
    col=int(input("input the col:"))
    col-=1
    row-=1
    if lg[row][col]!=".":
        print("invalid position!")
    elif col<=3 and row<=3 and count%2==0:
        lg[row][col]="0"
        count+=1
    else:
        lg[row][col]="X"
        count+=1
    show()
    if count>=8:
        go=False
        print("<<<<ENDED>>>>")
    win_check()



        