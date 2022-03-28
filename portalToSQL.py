import portalToSQL as pts

loginUrl = 'http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541' # 登录页面的URL  试试看 原本的失效了
# 由于北邮信息门户的特殊性，此处使用的是人工登录门户后获得的cookie
cookie = {'cookie':'JSESSIONID=7BED8F109245DB55BF1F921C59C946E4'}
notificationUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1154' # 校内通知的URL
notificationHref = 'xntz_content.jsp' # 校内通知的 href 标识
announcementUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1305' # 公示公告的URL
announcementHref = 'content.jsp'
newsUrl = 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1221' # 校内新闻的URL
newsHref = 'xnxw_content.jsp'
lectureUrl = 'http://my.bupt.edu.cn/jz_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1300' # 学术讲座的URL
lectureHref = 'hy_content.jsp'

    

if __name__ == '__main__':
    
    notification = pts.portalToSQL(loginUrl, cookie, notificationUrl, notificationHref, 'schoolArticles')
    notification.getInformation()
    
    announcement = pts.portalToSQL(loginUrl, cookie, announcementUrl, announcementHref, 'schoolAnnouncements')
    announcement.getInformation()
    
    
    news = pts.portalToSQL(loginUrl, cookie, newsUrl, newsHref, 'schoolNews')
    news.getInformation()

    lecture = pts.portalToSQL(loginUrl, cookie, lectureUrl, lectureHref, 'schoolLectures')
    lecture.getInformation()

    
