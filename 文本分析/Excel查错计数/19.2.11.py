import requests,json
import xlrd,xlwt
import string
from aip import AipNlp

def initBaidu():
    global client
    APP_ID = '11656491'
    API_KEY = 'sMkXY7DqBcOEMy1ue4pHhQGN'
    SECRET_KEY = 'xKdxqG7svYiGkDeUG7Yx1pqzUT5PMGky'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    
def ErrorChinese(msg):
    global client
    """ 你的 APPID AK SK 
    APP_ID = '11656491'
    API_KEY = 'sMkXY7DqBcOEMy1ue4pHhQGN'
    SECRET_KEY = 'xKdxqG7svYiGkDeUG7Yx1pqzUT5PMGky'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)"""
    index_flag=170
    num_flag=0
    l=list()
    while(1):
        cell_flag=len(msg[num_flag*170:])/index_flag
        if(cell_flag>1):
            msg1=msg[170*num_flag:170*(num_flag+1)]
            a=client.ecnet(msg1)
            try:
                for i in range(len(a['item']['vec_fragment'])):
                    d=dict()
                    d['错词']=a['item']['vec_fragment'][i]['ori_frag']
                    d['位置']=a['item']['vec_fragment'][i]['begin_pos']/2+1+num_flag*170
                    l.append(d)
            except:
                pass
            num_flag+=1
            continue
        else:
            a=client.ecnet(msg[num_flag*170:])
            try:
                for i in range(len(a['item']['vec_fragment'])):
                    d=dict()
                    d['错词']=a['item']['vec_fragment'][i]['ori_frag']
                    d['位置']=a['item']['vec_fragment'][i]['begin_pos']/2+1+num_flag*170
                    l.append(d)
            except:
                pass
            break
            
    return l

def is_chinese(uchar):
    '''
    判断一个unicode是否是汉字
    '''
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False
    
def NumChinese(cell):
    def Get_Average(aver):
        if(aver==list()):
            return
        sum = 0
        for item in aver:     
          sum += item  
        return sum/len(aver)
    n=0
    a=list()
    cell=str(cell)
    '''for word in cell:
        if(is_chinese(word)==True):
            n+=1'''
    a=ErrorChinese(cell)
    e=0
    if(a!=None):
        e=len(a)
    aver=list()
    for i in a:
        aver.append(i['位置'])
    return (0,e,a,Get_Average(aver))           #中文汉字数、错字数、错字和位置


initBaidu()
x=input('请输入Excel位置：')
data=xlrd.open_workbook(x)
workbook = xlwt.Workbook(encoding = 'utf-8')
for i in range(len(data.sheets())):
    worksheet = workbook.add_sheet(str(data.sheet_names()[i]),cell_overwrite_ok=True)
    table=data.sheets()[i]
    l=table.col_values(0, start_rowx=1, end_rowx=None)   #返回由该列中所有单元格的数据组成的列表
    headers=['文本段','中文总字数','错字数','错字位置平均值']
    x=0
    for cell in headers:
        worksheet.write(0,x,cell)
        x+=1
    MaxChineseError=0
    CE=list()
    x=0
    for cell in l:
        x+=1
        worksheet.write(x,0,cell)
        try:
            NumCH=NumChinese(cell)
        except UnicodeEncodeError:
            print("编码问题自动跳过…… "+str(x))
            CE.append('')
            continue
        except:
            input("出错，摁回车跳过……")
            CE.append('')
            continue
        if(NumCH==None):
            NumCH=(0,0,0)
        if(int(NumCH[1])>=MaxChineseError):
            MaxChineseError=int(NumCH[1])
        
        worksheet.write(x,1,NumCH[0])           #中文总字数
        worksheet.write(x,2,NumCH[1])           #错字数
        worksheet.write(x,3,NumCH[3])           #错字位置平均值
        CE.append(NumCH[2])

        if(MaxChineseError!=0):
            for y in range(MaxChineseError):
                worksheet.write(0,y*2+4,'中文错别字'+str(y+1))
                worksheet.write(0,y*2+5,'位置')
        p=0
        for y in CE:
            p+=1
            if (y!=None and y!='0'):
                for q in range(len(y)):
                    worksheet.write(p,q*2+4,str(y[q]['错词']))        #中文错别字
                    worksheet.write(p,q*2+5,y[q]['位置'])             #错别字位置          
        if(x%1000==0):
            print("已完成 "+str(x))
            workbook.save('new.xls')
    workbook.save('new.xls')
    print('全部完成')
