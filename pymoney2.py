import sys

def initialize():
    try:                                                    #檢測檔案存不存在                 
        rec = []
        with open('records.txt','a+') as fh_records:        #開啟上次存好的records.txt,如果找不到檔案就會新建一個
            fh_records.seek(0)                              #用'a+'開,所以先seek到開頭    
            if fh_records.readlines():                      #如果file裡面有東西就印Welcome (不是第一次使用)
                print('Welcome back!')
                fh_records.seek(0)                          #seek到第一行
                total = int(fh_records.readline())          #每次開都從第一行取得money
                fh_records.seek(0)
                cnt = 0
                for data in fh_records.readlines():         #data會是list              
                    if cnt!=0:                              #不讀第一行
                        rec.append(data.strip().split() )   #去掉'\n'並依空格分開,再加進rec裡
                    cnt += 1
                return total,rec
            else:                                           #如果file是空的就讓使用者輸入money (是第一次使用)
                try:
                    total = int(input("How much money do you have? ex: 1000 :"))
                    return total,rec
                except ValueError:
                    total = 0
                    print('Invalid value for money. Set to 0 by default.')
                    return total,rec
    except FileExistsError:
        print("The file doesn't exist.")
        return total,rec

def add(rec):
    global initial_money,temp_money,temp_records
    temp_money = initial_money
    temp_records = records.copy()
    add_to = input("Add an expense or income record with description and amount ,ex: breakfast -50 : ").split() #str -> list by space
    if len(add_to)==2:
        try:
            #計算money
            initial_money += int(add_to[1])
            #存入record
            rec.append(add_to)
            return rec
        except ValueError:          #add_to[1]不能轉成int時
            print('Invalid value for money.\nFail to add a record.')
            return rec
    else:
        print('The format of a record should be like this: breakfast -50.\nFail to add a record.')
        return rec

def delete(rec):
    global initial_money,temp_money,temp_records
    if rec == []:                           #沒紀錄->不能刪->直接return
        print("There's no records in file. Fail to delete a record.")
        return rec
    else:
        want_remove = input('Which record do you want to delete? ').split()
        if len(want_remove)==3:
            name = want_remove[0]
            #確保花費和欲刪除行數的輸入是可以轉成int的
            try:
                price = int(want_remove[1])
                index = int(want_remove[2])
            except ValueError:
                print('Invalid format. Fail to delete a record.')
                return rec
            #進一步確認要刪除的資料存在
            temp_money = initial_money          #存上一步的資料
            temp_records = records.copy()
            for i in range(0,len(rec)):
                if (name == rec[i][0]) and (str(price) == rec[i][1]) and (index == i+1):
                    initial_money -= price
                    rec.pop(i)
                    return rec
            #handle輸入正確,但沒有跟record的資料對到的情況
            print(f"There's no record with {' '.join(want_remove)}. Fail to delete a record.")
            return rec
        else:
            print('Invalid format. Fail to delete a record.')
            return rec

def view(total,rec):
        print("Here's your expense and income records:")
        print('Description          Amount\n==================== =======')
        for item in rec:
            print(f'{item[0]:<20} {item[1]:<6}')    # {name : <x } 靠右對齊x格
        print(f'==================== =======\nNow you have {total} dollars.')

def back(rec,temp_rec):
    global initial_money,temp_money
    initial_money = temp_money
    rec = temp_rec.copy()
    return rec

def save(total,record):
    with open('records.txt','w+') as fh_record:
        #在第一行寫入total 
        fh_record.write(f'{str(total)}\n')
        #換行後,第二行開始寫入record
        for item in record :
            fh_record.write(f"{' '.join(item)}\n")


initial_money,records = initialize()

#新功能需要
temp_money = initial_money
temp_records = records.copy()

while True:
    command = input('\nWhat do you want to do (add / view / delete / back / exit)? ')
    if command == 'add':     
        records = add(records)
    elif command == 'view':
        view(initial_money,records)
    elif command == 'delete':
        records = delete(records)
    elif command == 'back':                 #新功能(輸入back可以回到上一步(限一次))     
        records = back(records,temp_records)
    elif command == 'exit':
        save(initial_money,records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')