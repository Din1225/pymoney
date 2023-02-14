#輸入部分額外加了簡單的防呆機制(可以防止部分不符合輸入格式的情況)
while True:
    try:
        money = int(input("How much money do you have? ex: 1000 :"))
        break
    except:
        print("Please input a 'zero or positive integer'. Ex: 1000.")

while True:
    try:
        record = input("Add an expense or income record with description and amount ,ex: breakfast -50 : ")
        change = record.split()
        if(len(change) != 2 ):       #確保使用者輸入的只有兩個字串
            print("Please input correctly. Ex: breakfast -50.")
            continue
        change_int = int(change[1])
        break
    except:
        print("Please input correctly. Ex: breakfast -50.")

now = money + change_int
print(f"Now you have {now} dollars.")

