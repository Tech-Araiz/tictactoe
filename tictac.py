from colorama import Fore, Back
import os
lg=[[".",".","."],[".",".","."],[".",".","."]]
count=0
go=True
def show():
    for i in lg:
        print("    "+str(i))
def win_check_X():
    global go
    if lg[0][0]=="X" and lg[1][0]=="X" and lg[2][0]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False   
    elif lg[0][0]=="X" and lg[0][1]=="X" and lg[0][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[0][0]=="X" and lg[1][1]=="X" and lg[2][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[1][0]=="X" and lg[1][1]=="X" and lg[1][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[2][0]=="X" and lg[2][1]=="X" and lg[2][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[2][0]=="X" and lg[1][1]=="X" and lg[0][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[0][1]=="X" and lg[1][1]=="X" and lg[2][1]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[0][2]=="X" and lg[1][2]=="X" and lg[2][2]=="X":
        print("\n     "+Fore.WHITE+Back.GREEN+"X wins"+ Fore.RESET + Back.RESET) 
        go=False
def win_check_zero():
    global go
    if lg[0][0]=="0" and lg[1][0]=="0" and lg[2][0]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET) 
        go=False   
    elif lg[0][0]=="0" and lg[0][1]=="0" and lg[0][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[0][0]=="0" and lg[1][1]=="0" and lg[2][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET)
        go=False
    elif lg[1][0]=="0" and lg[1][1]=="0" and lg[1][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET)
        go=False
    elif lg[2][0]=="0" and lg[2][1]=="0" and lg[2][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET) 
        go=False
    elif lg[2][0]=="0" and lg[1][1]=="0" and lg[0][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET)
        go=False
    elif lg[0][1]=="0" and lg[1][1]=="0" and lg[2][1]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET)
        go=False
    elif lg[0][2]=="0" and lg[1][2]=="0" and lg[2][2]=="0":
        print("\n     "+Fore.WHITE+Back.GREEN+"0 wins"+ Fore.RESET + Back.RESET)
        go=False
def win_check():
    win_check_zero()
    win_check_X()

os.system("cls")

while(go):
    print(Fore.CYAN + "<<<<<<TIC TAC TOE>>>>>>"+ Fore.RESET)
    show()
    if count%2==0:
        print(Fore.RED + "<<<<Player 1's Turn>>>>"+ Fore.RESET)
    else:
        print(Fore.RED + "<<<<Player 2's Turn>>>>"+ Fore.RESET)
    row= int(input(Fore.YELLOW + "input the row:" + Fore.RESET))
    col=int(input(Fore.YELLOW + "input the col:" + Fore.RESET))
    col-=1
    row-=1
    if lg[row][col]!=".":       
        os.system("cls")
        print("    " + Fore.BLACK+Back.RED+"invalid position!"+ Fore.RESET + Back.RESET)
    elif col<=3 and row<=3 and count%2==0:
        lg[row][col]="0"
        count+=1
        os.system("cls")
    else:
        lg[row][col]="X"
        count+=1
        os.system("cls")
    if count>=8:
        go=False
        print("<<<<ENDED>>>>")
    win_check()



        