#-*- coding:utf-8 -*-
import requests,json
import xlrd,xlwt
import string
from aip import AipNlp
from aip import AipImageCensor

def initBaidu():
    global client
    APP_ID = '11656491'
    API_KEY = 'sMkXY7DqBcOEMy1ue4pHhQGN'
    SECRET_KEY = 'xKdxqG7svYiGkDeUG7Yx1pqzUT5PMGky'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

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

def ErrorChinese(msg):
    global client
    """ 你的 APPID AK SK 
    APP_ID = '11656491'
    API_KEY = 'sMkXY7DqBcOEMy1ue4pHhQGN'
    SECRET_KEY = 'xKdxqG7svYiGkDeUG7Yx1pqzUT5PMGky'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)"""
    try:
        a=client.ecnet(msg)
        #print(a)
        l=list()
        for i in range(len(a['item']['vec_fragment'])):
            d=dict()
            d['错词']=a['item']['vec_fragment'][i]['ori_frag']
            d['位置']=a['item']['vec_fragment'][i]['begin_pos']
            l.append(d)
    except:
        l=None
    return (l)

def OldErrorChinese(msg_str):
    '''
    pip install request
    url = 'http://api.CuoBieZi.net/spellcheck/json_check/json_phrase'
    字段一："content", 填写需要检查的文字内容
    字段二："mode", 固定值，填写："advanced"  预留参数，固定值
    字段三："biz_type", 固定值，填写："show"  预留参数，固定值
    返回 json 格式的结果：
    {"Cases":[{"Error":"中国人民共和国","Tips":"中华人民共和国","Sentence":"中国人民共和国下半年上世纪将在微信账户钱包帐户的“九宫格”中开设快速的笑着保险入口，","ErrInfo":"","Pos":4}]}
    json 结果说明：
    Error 是错误词
    Tips 是正确词语
    Sentence 是错误词与所在的句子
    Pos 是错误词在文章中的位置
    其他是测试字段，未来会取消
    '''
    l=list()
    payload = {
        "content" : msg_str,
        "mode": "advanced",
        "username" : "tester",
        "biz_type": "show"
    }
    url = 'http://api.CuoBieZi.net/spellcheck/json_check/json_phrase'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    returned_json_dic=response.json()
    try:
        for i in range(len(returned_json_dic['Cases'])):
            d=dict()
            d['错词']=returned_json_dic['Cases'][i]['Error']#错字
            #d['正确词语']=returned_json_dic['Cases'][i]['Tips'] #正确词语
            d['位置']=returned_json_dic['Cases'][i]['Pos'] #在句子中的位置
            l.append(d)
            #print(returned_json_dic['Cases'][i]['Sentence'])#所在句子
        return(l)
    except:
        1

def is_chinese(uchar):
    '''
    判断一个unicode是否是汉字
    '''
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False
    
def is_chinese_punctuation(uchar):
    '''
    判断一个unicode是否是中文标点
    '''
    p='！？｡＂＃＄％＆＇（）＊＋，，。！@#￥%……&*（）——－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏'
    if uchar in p:
        return True
    else:
        return False
    
def NumChinese(cell):
    '''
    汉字和标点数，查错    
    l=list()
    n=0
    np=0
    e=0
    for i in range(len(data.sheets())):
        table = data.sheets()[i]
        nrows = table.nrows             #获取该sheet中的有效行数
        ncols = table.ncols             #获取列表的有效列数
        for rowx in range(nrows):
            for colx in range(ncols):
                if(table.cell_type(rowx,colx)==1):    #判断单元格中的数据类型
                    a=ErrorChinese(table.cell_value(rowx,colx))
                    if(a!=None):
                        e+=len(a)
                        l.append(a)
                        l.append((i,rowx,colx))
                    for c in table.cell_value(rowx,colx):
                        if(is_chinese(c)==True):
                            n+=1
                        if(is_chinese_punctuation(c)==True):
                            np+=1
    return (n,np,l,e)'''
    n=0
    a=None
    cell=str(cell)
    for word in cell:
        if(is_chinese(word)==True):
            n+=1
    if(n!=0):
        a=ErrorChinese(cell)
    e=0
    if(a!=None):
        e=len(a)
    return (n,e,a)           #中文汉字数、错字数、错字和位置

def CheckEnglish(word):
    f=open('words.txt')
    d=dict()
    for word_n in f:
        if(word_n.strip() not in d):
            d[word_n.strip()]=0
    if word in d:
        return True
    else:
        return False
            
def NumEnglish(cell):
    cell=str(cell)
    n=0
    np=0
    location=0
    l=list()
    t=[0,l]
    if (cell.strip() ==''):
        return
    word=list()
    for letter in cell:
        if ((letter in string.punctuation) or is_chinese_punctuation(letter) ):
            np+=1                       #总标点数        
        if letter in string.ascii_letters:
            n+=1                        #字母个数
            letter=letter.lower()
            word+=[letter]
        else:
            word=''.join(word)
            if(word!=''):
                location+=1
                if not CheckEnglish(word):
                    t[0]+=1             #错词个数
                    d=dict()
                    d['wor']=word
                    d['loc']=location
                    t[1].append(d)      #错词和位置(第几个单词)
            word=list()
                
    return [location,np,t[0],t[1],n] #英文单词数、总标点、英文错词数、错词和位置、字母个数

def DNNml(text):
    '''
    DNN语言模型，检测句子通顺程度。数值越低，句子越通顺。
    '''
    global client
    try:
        d=client.dnnlm(text)
        return d['ppl']
    except:
        return str('无')

def sentiment(text):
    '''
    情感倾向分析.对包含主观观点信息的文本进行情感极性类别（积极、消极、中性）的判断，
    并给出相应的置信度。
    {
    "text":"苹果是一家伟大的公司",
    "items":[
        {
            "sentiment":2,    //表示情感极性分类结果
            "confidence":0.40, //表示分类的置信度
            "positive_prob":0.73, //表示属于积极类别的概率
            "negative_prob":0.27  //表示属于消极类别的概率
        }
            ]
    }
    '''
    global client
    try:
        d=client.sentimentClassify(text)
        l=[d['items'][0]['positive_prob'],d['items'][0]['negative_prob']]
    except:
        l=[1,1]
    return l

#def English(data):
    '''
    英文单词和英文标点数，查错
    a=[0,0,0,'']
    for i in range(len(data.sheets())):
        table = data.sheets()[i]
        nrows = table.nrows             #获取该sheet中的有效行数
        ncols = table.ncols             #获取列表的有效列数
        for rowx in range(nrows):
            for colx in range(ncols):
                if(table.cell_type(rowx,colx)==1):    #判断单元格中的数据类型
                    cell_v=NumEnglish(table.cell_value(rowx,colx))
                    a[0]+=cell_v[0]
                    a[1]+=cell_v[1]
                    a[2]+=cell_v[2]
                    a[3]
    return a'''
def textSpam():
    global client1
    

initBaidu()
initspam()
x=input('请输入Excel位置：')
data=xlrd.open_workbook(x)
workbook = xlwt.Workbook(encoding = 'utf-8')
for i in range(len(data.sheets())):
    worksheet = workbook.add_sheet(str(data.sheet_names()[i]),cell_overwrite_ok=True)
    table=data.sheets()[i]
    l=table.col_values(0, start_rowx=1, end_rowx=None)   #返回由该列中所有单元格的数据组成的列表
    headers=['文本段','中文总字数','总标点数','汉字错字数','英文错词数','总英文单词数','英文字母数','DNN','积极情感概率','消极情感概率','文本审核(0表示非违禁，1表示违禁，2表示建议人工复审)']
    x=0
    for cell in headers:
        worksheet.write(0,x,cell)
        x+=1
    MaxChineseError=0
    MaxEnglishError=0
    CE=list()
    EE=list()
    x=1
    for cell in l:
        worksheet.write(x,0,cell)
        t=NumChinese(cell)
        e=NumEnglish(cell)
        dnn=DNNml(cell)
        se=sentiment(cell)
        b=textspam(cell)
        if(t==None):
            t=['0','0','0']
        if(e==None):
            e=['0','0','0','0','0']
        if(int(t[1])>=MaxChineseError):
            MaxChineseError=int(t[1])
        if(int(e[2])>=MaxEnglishError):
            MaxEnglishError=int(e[2])
        worksheet.write(x,1,t[0])           #中文总字数
        worksheet.write(x,2,e[1])           #总标点数
        worksheet.write(x,3,t[1])           #汉字错字数
        worksheet.write(x,4,e[2])           #英文错词数
        worksheet.write(x,5,e[0])           #总英文单词数
        worksheet.write(x,6,e[4])           #英文字母数
        worksheet.write(x,7,dnn)            #DNN
        worksheet.write(x,8,se[0])          #积极情感概率
        worksheet.write(x,9,se[1])          #消极情感概率
        worksheet.write(x,10,b)             #文本审核
        CE.append(t[2])
        EE.append(e[3])
        x+=1
        if(x%100==0):
            print('已完成'+str(x)+'个,已保存')
            workbook.save('new.xls')
    workbook.save('new.xls')
'''
    l_a=0
    if(MaxChineseError!=0):
        for y in range(MaxChineseError):
            worksheet.write(0,y*2+10,'中文错别字'+str(y+1))
            worksheet.write(0,y*2+11,'位置')
            l_a+=2
    if(MaxEnglishError!=0):
        for y in range(MaxEnglishError):
            worksheet.write(0,y*2+10+l_a,'英文错词'+str(y+1))
            worksheet.write(0,y*2+11+l_a,'位置')
    
    p=0
    for y in CE:
        p+=1
        if (y!=None and y!='0'):
            for q in range(len(y)):
                worksheet.write(p,q*2+10,str(y[q]['错词']))        #中文错别字
                worksheet.write(p,q*2+11,y[q]['位置'])        #错别字位置         
    p=0
    for y in EE:
        p+=1
        if (y!=None and y!='0'):
            for q in range(len(y)):
                worksheet.write(p,q*2+10+l_a,str(y[q]['wor']))              #英文错词
                worksheet.write(p,q*2+11+l_a,y[q]['loc'])              #错词位置         
       
        #worksheet.write(x,7,str(t[2]))      #中文错别字及位置
        #worksheet.write(x,8,str(e[3]))      #英文错词及位置
'''        
   
    
'''print('
中文字数：%d
中文标点数：%d
错词数：%d
''%(t[0],t[1],t[3]))
for i in range(0,len(t[2]),2):
    print('所在工作表：'+ str(t[2][i+1][0]+1))
    print('所在单元格： 行：'+ str(t[2][i+1][1]+1)+
          '             列：'+ str(t[2][i+1][2]+1))
    print(str(t[2][i])+'\n')'''
