import xlrd,xlwt
from aip import AipImageCensor

def initspam():
    global client1
    APP_ID='14422159'
    API_KEY='psxn324sUoqFaNMjyob3FaqN'
    SECRET_KEY = 'jakFwZEk63dTPr52ibznaBXoI0To2GEs'
    client1=AipImageCensor(APP_ID, API_KEY, SECRET_KEY)

def textspam(cell):
    try:
        a=client1.antiSpam(cell)
        b=a['result']['spam']
    except:
        b=''
    return b
    
initspam()
x=input('请输入Excel位置：')
data=xlrd.open_workbook(x)
workbook = xlwt.Workbook(encoding = 'utf-8')
for i in range(len(data.sheets())):
    worksheet = workbook.add_sheet(str(data.sheet_names()[i]),cell_overwrite_ok=True)
    table=data.sheets()[i]
    l=table.col_values(0, start_rowx=1, end_rowx=None)   #返回由该列中所有单元格的数据组成的列表
    headers=['文本段','文本审核(0表示非违禁，1表示违禁，2表示建议人工复审)']
    x=0
    for cell in headers:
        worksheet.write(0,x,cell)
        x+=1
    x=1
    for cell in l:
        worksheet.write(x,0,cell)
        b=textspam(cell)
        worksheet.write(x,1,b)             #文本审核
        x+=1
        if(x%100==0):
            print('已完成'+str(x)+'个,已保存')
            workbook.save('new.xls')
    workbook.save('new.xls')
