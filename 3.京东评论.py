import requests
from lxml import etree
import json
import pymysql
import time

class JD_spider(object):

    def __init__(self,):
        self.url = ''
        self.html = ''
        self.comment_url = 'https://sclub.jd.com/comment/productPageComments.action'


    def get_comment(self,i):
        """
        取评论
        :return: [[id,username,score]],[]]或[{'id':123,'username':'zzdw','score':5,}];
        """
        self.params = {
            'productId': 100000287113,  # 商品id，先写死 苹果手机
            'score': 0,
            'sortType': 5,
            'page': i,
            'pageSize': 10,
            # 'callback': 'fetchJSON_comment98vv15262',
            # 'isShadowSku': 0,
            # 'fold': 1,
        }
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'cookie': '__jdu=342774265; mt_xid=V2_52007VwEXUVteV1kYTSkODGMEFldVUE5SHRsQQAA0ABBODQpXUwNITg5WZwEQUQ1dAFsvShhcDHsDEU5eWUNaGUIYVQ5nAiJQbVtiWR5PEVkAVwAVUls%3D; shshshfpa=215f53d2-634c-f0ec-70ac-6e7d425179e2-1545296893; unpl=V2_ZzNtbUdXFxN2CEZTLhtUVmIARVVKUBcVIg1PB3JMW1U3AxYNclRCFXwURldnGloUZwMZXkdcQxRFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJAxNaS1ZFF3ILQlR4KWwGZzMSXHJVRhZzDkNXfB1sNWAzIm1EX0ATdwF2VUsYbEczXxVUQVFFHDgKQ1d9H1kGYAciXHJU; pin=%E6%9C%A8%E6%A7%BF-%E5%90%91%E5%8D%97; _tp=FwBFNe%2Fh1l1dIwiYsR35hVV6fZJ6Op46H%2BhDwTpWetfiYUsY6%2F5mxQTKqeEfAOPh; _pst=%E6%9C%A8%E6%A7%BF-%E5%90%91%E5%8D%97; unick=%E6%9C%A8%E6%A7%BF-%E5%90%91%E5%8D%97; pinId=6vfDAeeY2hrOeyRhFUKZPw; PCSYCityID=412; user-key=87bc2599-66e0-42ea-ac7e-4f691948b927; cn=0; ipLoc-djd=1-72-4137-0; areaId=1; __jda=122270672.342774265.1545296775.1545914273.1545964023.8; __jdc=122270672; __jdv=122270672|baidu|-|organic|not set|1545964023311; TrackID=1RuZ-F4cuItBPqoShKYnAhGhjt6mISReZLqPErQkGUpIewy-QsseBHRWpZCG3bWX9AHRxwn8ylhUa-mH29KRM0A; ceshi3.com=000; 3AB9D23F7A4B3C9B=GTV7W3JEROFSPYYJGDW2SVRAB6744BFQPD3G7CQKMQIV4UEVC4CXJEZ4GDD6HIC5EZAZNPXF5SBY2CV2FLUH2KMEIA; shshshfp=018a9bf58edcea2fe1971733c53e419b; _gcl_au=1.1.2082545328.1545964430; shshshfpb=cPLjtL6WiKEY9t3pZWoluXA%3D%3D; thor=E86E20F3FE258477823C5FAA491FAEEBA39F88C7A837958F290D3BDC72CD7901ADBA15277F6F04408BFB18AAF6599CFA254FA05D32360B833F0E486FA0D49DE9F30DC1D30E1E61A2EAFC5BE4F22A52D4BC3A2A729D225B9D726D47B3DB9907F140438908D14F5D91728C3AC9DC3AFAEC3F9AEC2FB06A76EB0194770612761143; JSESSIONID=9A380D7FFA7894718AE8038A9AACAC06.s1',
            'referer': 'https://item.jd.com/100000287113.html',
        }
        comment_resp = requests.get(url=self.comment_url, params=self.params, headers=self.headers, )
        comment_str = comment_resp.text
        # load是本地文件
        comment_dict = json.loads(comment_str)
        # 评论
        comments = comment_dict["comments"]

        result_list = []
        for comment in comments:
            id = comment['id']
            # print('id:', id)
            name = comment["nickname"]
            # print('用户名：', name)
            content = comment['content']
            # print('评论：', content)
            c_time = comment['creationTime']
            # print('时间：', c_time)
            score = comment['score']
            # print(score)
            color = comment['productColor']
            # print('颜色：', color)
            size = comment['productSize']
            # print('版本：', size)
            result_list.append({
                'id': id,
                'content': content,
                'creationTime': c_time,
                'score': score,
                'color': color,
                'size_q': size,
            })

        # return result_list
        # print(result_list)
        for list in result_list:
            print(list)
            self.save_db(list)

    def save_db(self,list):
        """

        :param list: [{'id':2323,'content':'物美价廉',},{}]
        :return: affected_rows: {int} 成功写入的行数
        """
        db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='123456',
                     db='jd',
                     charset='utf8mb4')
        # with db.cursor() as cursor:
        #     sql = 'CREATE TABLE if not EXISTS jd(id int, content varchar(200), c_time varchar(20), score varchar(20), color char(20), size_q varchar(20))'
        #     cursor.execute(sql)

        with db.cursor() as cursor:
            sql_v = """insert into jd(id,content,c_time,score,color,size_q) values (%(id)s, %(content)s,%(creationTime)s,%(score)s,%(color)s,%(size_q)s);"""
            cursor.execute(sql_v, args=list)
            db.commit()
            # 关闭数据库连接
            db.close()

    def run(self):
        for i in range(0,10):
            self.get_comment(i)



if __name__ == '__main__':
    jdspider = JD_spider()
    jdspider.run()