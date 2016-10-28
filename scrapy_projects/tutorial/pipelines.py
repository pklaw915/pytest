# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLStoreQuotesAuthorPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        conn.execute("""
                select name from quotes_author where name = %s
        """, (item['name'], ))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update quotes_author set name = %s, birthdate = %s, bio = %s where name = %s
            """, (item['name'], item['birthdate'], item['bio'], item['name']))
        else:
            conn.execute("""
                insert into quotes_author(name, birthdate, bio)
                values(%s, %s, %s)
            """, (item['name'], item['birthdate'], item['bio']))

    def _handle_error(self, failue, item, spider):
        log.err(failure)