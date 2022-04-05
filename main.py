import portalToSQL as pts

loginUrl = 'http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541' # 登录页面的URL
# 由于北邮信息门户的特殊性，此处使用的是人工登录门户后获得的cookie

cookie = {'cookie':'JSESSIONID=D3DAE108CD370BFC4A6B768D9F403065'}

#notificationUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1154' # 校内通知的URL
notificationHref = 'xntz_content.jsp' # 校内通知的 href 标识
#announcementUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1305' # 公示公告的URL
announcementHref = 'content.jsp'
#newsUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1221' # 校内新闻的URL
newsHref = 'xnxw_content.jsp'
#lectureUrl = 'http://my.bupt.edu.cn/jz_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1300' # 学术讲座的URL
lectureHref = 'hy_content.jsp'

    

if __name__ == '__main__':
    
    notification = pts.portalToSQL(loginUrl, cookie,notificationHref, 'schoolArticles', 120, 1154)
    # df1 = notification.getInformation()

    announcement = pts.portalToSQL(loginUrl, cookie,announcementHref, 'schoolAnnouncements', 50, 1305)
    # df2 = announcement.getInformation()

    news = pts.portalToSQL(loginUrl, cookie,  newsHref, 'schoolNews', 165, 1221)
    # df3 = news.getInformation()

    lecture = pts.portalToSQL(loginUrl, cookie, lectureHref, 'schoolLectures', 5, 1300)
    # df4 = lecture.getInformation()
    '''
    df1.to_csv("schoolArticles.csv")  # 公示公告
    df2.to_csv("schoolAnnouncements.csv")  # 校内通知
    df3.to_csv("schoolNews.csv")  # 校内新闻
    df4.to_csv("schoolLectures.csv")  # 学术讲座
    '''
    
