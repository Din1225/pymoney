import sys


class Record:
    """Represent a record."""
    def __init__(self, category , description, amount):
        """初始化單一record"""
        self._category = category
        self._description = description
        self._amount = str(amount)

    @property
    def category(self):
        """檢視record的類別"""
        return self._category
    @property
    def description(self):
        """檢視record的敘述"""
        return self._description
    @property
    def amount(self):
        """檢視record的收支"""
        return self._amount


class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """初始化records"""
        try:                                                    #檢測檔案存不存在 和 檔案內紀錄有沒有不合法的格式                
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
                            data = data.strip().split()         #去掉'\n'並依空格分開,再加進rec裡
                            int(data[2])                        #(用來測試有沒有不合法的格式)
                            rec.append(Record(data[0],data[1],data[2]))#每個元素都轉成Record的形式
                        cnt += 1
                    self._records,self._initial_money = rec,total
                else:                                           #如果file是空的就讓使用者輸入money (是第一次使用)
                    try:
                        total = int(input("How much money do you have? ex: 1000 :"))
                        self._records,self._initial_money = rec,total
                    except ValueError:
                        total = 0
                        print('Invalid value for money. Set to 0 by default.')
                        self._records,self._initial_money = rec,total
        except ValueError:
            print("Some records in the file are in invalid format")
            print(sys.exit())                                   #直接中斷程式  
        except FileExistsError:
            print("The file doesn't exist.")
            print(sys.exit())                                   #直接中斷程式 
	
 
    def add(self,new_record,categories):
        """增加紀錄"""
        new_record = new_record.split()                                 #str -> list by space
        if len(new_record)==3:
            new_record = Record(new_record[0],new_record[1],new_record[2])      #確認完長度正確後 把list轉成Record instance
            if categories.is_category_valid(new_record.category):
                try:
                    #計算money
                    self._initial_money += int(new_record.amount)
                    #存入record
                    self._records.append(new_record)                #list的每一項都是一個Record()的型別
                except ValueError:                                  #add_to[2]不能轉成int時
                    print('Invalid value for money.\nFail to add a record.')
            else:       #handle 要加的紀錄不在我定義的類別裡
                print('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
        else:
            print('Invalid format.\nFail to add a record.')
    	
 
    def view(self):
        """檢視紀錄"""
        print("Here's your expense and income records:")
        print('Category        Description          Amount')
        print('=============== ==================== ========')
        for item in self._records:
            print(f'{item.category :<15} {item.description:<20} {item.amount:<8}')    # {name : <x } 靠右對齊x格
        print('=============== ==================== ========')
        print(f'Now you have {self._initial_money} dollars.')
    	
 
    def delete(self,delete_record):
        """刪除紀錄"""
        if self._records == []:                           #沒紀錄->不能刪->直接return
            print("There's no records in file. Fail to delete a record.")
        else:
            delete_record = delete_record.split()
            if len(delete_record)==3:
                name = delete_record[0]
                #確保花費和欲刪除行數的輸入是可以轉成int的
                try:
                    price = int(delete_record[1])
                    index = int(delete_record[2])
                except ValueError:
                    print('Invalid format. Fail to delete a record.')
                    return
                #進一步確認要刪除的資料存在
                for i in range(0,len(self._records)):
                    if (name == self._records[i].description) and (str(price) == self._records[i].amount) and (index == i+1):
                        self._initial_money -= price
                        self._records.pop(i)
                        return
                #handle輸入正確,但沒有跟record的資料對到的情況
                print(f"There's no record with {' '.join(delete_record)}. Fail to delete a record.")
            else:
                print('Invalid format. Fail to delete a record.')
    	
 
    def find(self,non_nested_list):
        """在records中找符合子類別的紀錄並印出來"""
        #print用的
        global category             
        #在self._records每一項取類別出來判斷 找到有存在於non_nested_list的 就過濾出來
        def check_inside(record):
            """檢查record.category有沒有在子類別的list裡面"""
            if record.category in non_nested_list:
                return True
        sub_list =[]
        sub_list.extend(list(filter( lambda x: check_inside(x),self._records )))        #過濾出我要的Record 再用list裝起來

        #算錢
        total = 0
        for i in range(0,len(sub_list)):
            total += int(sub_list[i].amount)
        #把sub_list和錢印出來
        if sub_list != []:
            print(f"Here's your expense and income records under category \"{category}\":")
            print('Category        Description          Amount')
            print('=============== ==================== ========')
            for item in sub_list:
                print(f'{item.category:<15} {item.description:<20} {item.amount:<8}')    # {name : <x } 靠右對齊x格
            print('=============== ==================== ========')
            print(f'The total amount above is {total}.')
        else:
            print(f'There is no records under category "{category}".')


    def save(self):
        """存檔"""
        with open('records.txt','w+') as fh_record:
            #在第一行寫入total 
            fh_record.write(f'{str(self._initial_money)}\n')
            #換行後,第二行開始寫入record
            for item in self._records :
                fh_record.write(f"{' '.join([item.category,item.description,item.amount])}\n")
    

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """初始化分類"""
        categories = ['expense', ['food', ['meal', 'snack', 'drink'], \
            'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
        self._categories = categories
   
 
    def view(self):
        """檢視目前有的類別"""
        def view_categories(categories,level):
            """Categories.view的遞迴式"""
            for i in categories:
                if type(i) == list:             #只要遇到list就遞迴下去找,找出不是list的
                    view_categories(i,level+1)
                else:                           #如果不是list,就直接print出來(在同個list的會是同一層的)
                    print(f'{"  "*level}- {i}')
        view_categories(self._categories,0)
    	
 
    def is_category_valid(self,category):
        """判斷要新增的類別有沒有在分類中"""
        def is_valid(category,categories):
            """Categories.is_category_valid的遞迴式"""
            if type(categories) == list:
                for i in categories:
                    flag = is_valid(category,i)
                    if flag == -1:                          #接收到-1 代表這個i是單一個的 比較完發現不是
                        continue                            #就再往下一項繼續找
                    elif flag ==  True:                     #只要任何一項符合就代表找到了 就不斷回傳True到前一層
                        return True
            else:                                           #如果不是list 就比較,不對就回傳-1
                if category == categories:
                    return True 
                else:
                    return -1
            return False                                    #如果都沒找到就會跳出迴圈 跑到這裡 就回傳False
        return is_valid(category,self._categories)
    	
 
    def find_subcategories(self,target_categories):
        """傳回Flatten後的那些子類別"""
        def find_subcategories_gen(target, categories, found=False):
            """Categories.find_subcategories的generator"""
            if found == True:                       #一找到就會不斷回傳後面的子類別
                for i in categories:                #遇到list就遞迴 直到遇到單一元素再傳回  以達到flatten list的效果
                    if type(i) == list:
                        yield from find_subcategories_gen(target, i, True)
                    else:
                        yield i
            elif type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(target, child, False)
                    #除了檢查index有沒有超出範圍 還要檢查下一項有沒有超出範圍 如果沒有下一項就等於沒有子類別 and 如果下一項是list 就表示有子類別
                    if child == target and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(target, categories[index + 1], True)      #flag設成True,並呼叫下一項,這樣就會只進第一個if
            else:         
                if categories == target:            #找到第一個 就回傳一個
                    yield categories

        return [i for i in find_subcategories_gen(target_categories,self._categories)]  #把每次傳回來的 弄成list


records = Records()
categories = Categories()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':     
        record = input("Add an expense or income record with category, description, and amount (separate by spaces): ")
        records.add(record, categories)     
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? ")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')