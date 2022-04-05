"""
Description: 该文件包含一个 portalToSQL 类，用于将门户中特定的消息更新到 mysql
            数据库中。构造函数中含有 loginUrl, cookie, infoHref, lableName, pages, number 6个参数。
            loginUrl    登录页面的URL                    String
            cookie      登录页面后获得的cookie           Dictionary
            infoHref    需要爬取的消息对应的Href         String
            lableName   数据库中的表名                   String   或许可以删掉了
            pages       所需爬取新闻列表页的最大页数             int
            number      列表页的一个参数，区分校内新闻、校内通知等  int

            Note: 由于北邮信息门户系统的特殊性，需要手动获取cookie才能登陆。在其他部分测试过的
            学校门户网站中不需要提供cookie也可以登陆。
"""


import requests
import http.cookiejar as cookielib
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine


class portalToSQL:
    
    # 基础信息
    username = '2020212096'               # 信息门户登录用户名 ???
    userpassword = ''                         # 信息门户登录密码

    host = "localhost"
    port = 3306
    database = "data"
    user = "root"
    password = "20021214Yzz+"
    charset = 'utf8'

    '''
    Input:      loginUrl:   登录网址
                cookkie:    登录cookie
                infoUrl:    信息所在的网址
                infoHref:   信息所在的Href标识
                lableName:  预存入的数据库的表名
    Output:     None
    Function:   构造函数，初始化
    '''
    def __init__(self, loginUrl, cookie, infoHref, lableName, pages, number):
        self.loginUrl = loginUrl
        self.cookie = cookie
        self.infoHref = infoHref
        self.lableName = lableName
        self.pages = pages
        self.number = number

    
    '''
    Input:      HTTP GET请求 loginUrl 所得到的内容的字符串 str
    Output:     包含本次登录的网站信息的字典 dic (包括用户名、密码、Lt等参数)
    Function:   从 loginUrl 里获取本次登录所特有的参数，如 lt， execution 等
    '''
    ## 这里的str是个啥？？
    def getLt(self, str):
        lt=bs(str,'html.parser')

        dic={}
        for inp in lt.form.find_all('input'):
            if(inp.get('name'))!=None:
                dic[inp.get('name')]=inp.get('value')

        # dic['username']='2020212096'
        # dic['password']='Lyt38078660'

        return dic
    
    '''
    Input:      目标地址 objectUrl，实例化的 Session 对象
    Output:     含有标题、日期和文章主体的字典 result
    Function:   获得所需要爬取的页面的标题、日期和文章主体
    '''
    def getNewsDetail(self, objectUrl, session):
        result = {}
        res = session.get(objectUrl, headers=self.cookie)
        res.encoding = 'utf-8'
        soup = bs(res.text, 'html.parser')
        result['Title'] = soup.select('.text-center')[0].text
        
        date=[]
        # 学术讲座和其他通知的标签不同，故做两种处理。'singlemeta text-center'为学术讲座的格式。
        if soup.find_all(class_ = 'pmeta ptime'):
            for j in soup.find_all(class_ = 'pmeta ptime'):
                date.append(j.text)
                eachDate = ''   ## 这是为什么
            for i in date:
                eachDate = i
        else:
            for j in soup.find_all(class_ = 'singlemeta text-center'):
                date.append(j.text)
                eachDate = ''
            for i in date:
                eachDate = i
            eachDate = (eachDate.split(' ')[-1] + "    " + eachDate.split(' ')[-2])
        result['date'] = eachDate
        article = []
        image = []
        tmp = ''
        allP = soup.select('.singleinfo #vsb_content .v_news_content p')
                           
        # 插入图片                           
        allPicture = soup.select('.singleinfo #vsb_content .v_news_content p img')
        try:
            for pictures in allPicture:
                imgsUrl = 'http://my.bupt.edu.cn' + pictures.get('src')
                image.append(imgsUrl)
        except:
            pass # 解决不含img信息时的报错问题
        
        for p in allP:
            # article.append('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + p.text.strip() + '\n')
            article.append(p.text.strip() + '\n')
        for i in range(0, len(article)):
            tmp += article[i] 
        result['article'] = tmp
        
        tmp = ''
        for unitImg in range(0, len(image)):   
            if unitImg == len(image) - 1:
                tmp += image[unitImg]
            else:
                tmp += image[unitImg] + ','
        result['image'] = tmp
        return result
    
    # 将数据写入数据库
    # 连接数据库
    '''
    Input:      需要写入数据库的 DataFrame 型数据 df
    Output:     写入数据库的结果
    Function:   将 df 写入 database 数据库的 lablename 表中
    '''
    def toSqlServer(self, df):

        # connect=pymysql.connect(host=self.host,user=self.user,port=self.port,passwd=self.password,database=self.database,charset=self.charset)
        # df  为处理好的数据，to_filename为要传入的数据库表的名称
        #  构建信息。即数据库的基本信息
        # engine = create_engine(
        #     str(r'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (self.database,self.password, self.host, self.port, self.user, self.charset)))
        engine = create_engine("mysql+pymysql://root:20021214Yzz+@localhost:3306/data?charset=utf8")
        # 例如：engine = create_engine("mysql+pymysql://root:666666@localhost:3306/ajx?charset=utf8")
        #  append 增量入库，不会覆盖之前的数据，
        df.to_sql(self.lableName, con=engine, if_exists='append', index=False)

    '''
    Input:      None
    Output:     df
    Function:   将所需要爬取的信息保存到 Excel 文件和 SQL Server 数据库
    '''
    def getInformation(self):
        #模拟一个浏览器头
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    
        #实例化session
        session = requests.Session()
        session.cookies = cookielib.CookieJar()
        response=session.get(self.loginUrl, headers=header)
        # 得到含有输入的用户名、密码的字典格式
        dic = self.getLt(response.text)
        print(dic)

        # 更新post信息
        postdata={
                'username':self.username,
                'password':self.userpassword,
                'submit':'登录',
                'type':'username_password',
                'execution':dic['execution'],
                '_eventId':'submit'
                }

        #携带登陆数据，以post方式登录，
        response = session.post(self.loginUrl, data=postdata, headers=header)

        url = []
        for i in range(self.pages):
            infoUrl= "http://my.bupt.edu.cn/list.jsp?PAGENUM={}&urltype=tree.TreeTempUrl&wbtreeid={}".format(i+1, self.number)
        #用 beautifulsoup 解析 html
            # 用 GET 方式访问“校内通知”的页面
            # http://my.bupt.edu.cn/list.jsp?PAGENUM=4&urltype=tree.TreeTempUrl&wbtreeid=1221
            res = session.get(infoUrl, headers=self.cookie)
            soup = bs(res.text, 'html.parser')

            # 获取各个通知的详细URL
            urls = soup.find_all(href=re.compile(self.infoHref))
            # print(urls)
            isPrompt = False  # 让提示代码只执行一次
            for j in urls:
                if (('http://my.bupt.edu.cn/' + j.get('href')) not in url):
                    url.append('http://my.bupt.edu.cn/' + j.get('href'))
                    if url != [] and isPrompt == False:
                        print(">>> 网址爬取成功")
                        isPrompt = True

        # 获取新闻详情
        news_total = []
        for i in range(0, len(url)):
            newsary = self.getNewsDetail(url[i], session)  # 读取网址中的内容详情
            news_total.append(newsary)
        df = pd.DataFrame(news_total)
        self.toSqlServer(df)  # 将数据存入数据库
        # return df

