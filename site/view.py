import json

from core.sql_core import db
from core.view_core import BaseView, redirect


class HomeView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['home'] = True
        kwargs['test'] = {1: {'q': {'h': 'Hello'}}}
        return super().get(request, *args, **kwargs)


class CommentView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['comment'] = True
        kwargs['regions'] = db.get_data_by_sql('SELECT * FROM regions')
        kwargs['cities'] = db.get_data_by_sql('SELECT * FROM cities WHERE region=%s', (kwargs['regions'][0]['id'],))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {'success': False}

        if db.set_data_by_sql('''INSERT INTO comments( last_name, first_name, middle_name, region, city, phone, email, text_comment)
                              VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''',
                              (
                                      request['POST'].get('last_name', ''),
                                      request['POST'].get('first_name', ''),
                                      request['POST'].get('middle_name', ''),
                                      request['POST'].get('region', 1),
                                      request['POST'].get('city', 1),
                                      request['POST'].get('phone', ''),
                                      request['POST'].get('email', ''),
                                      request['POST'].get('text_comment', ''),
                              )):
            data['success'] = True

        return json.dumps(data)


class ViewView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['view'] = True
        kwargs['comments'] = db.get_data_by_sql(
            '''SELECT comments.id, last_name, first_name,middle_name, regions.name AS region,
               cities.name AS city, phone, email, text_comment
               FROM comments
               INNER JOIN cities ON comments.city=cities.id
               INNER JOIN regions ON comments.region=regions.id
               ''')
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if 'comment_id' in request['DELETE']:
            try:
                if db.set_data_by_sql('DELETE FROM comments WHERE id=%s', (request['DELETE'].get('comment_id'),)):
                    return 'OK'
            except KeyError:
                pass


class StatCityView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['region_stat'] = True
        kwargs['region'] = db.get_data_by_sql('SELECT name FROM regions WHERE id=%s', (kwargs['region_id'],))
        kwargs['cities'] = db.get_data_by_sql('''
                                                 SELECT cities.id, cities.name , COUNT(*) AS comments_count
                                                 FROM comments, (SELECT id, name FROM cities WHERE region=%s)cities
                                                 WHERE region=%s AND city=cities.id GROUP BY cities.id;
                                              ''', (kwargs['region_id'], kwargs['region_id'],))
        return super().get(request, *args, **kwargs)


class StatView(BaseView):
    def get(self, request, *args, **kwargs):
        kwargs['stat'] = True
        kwargs['regions'] = db.get_data_by_sql('''SELECT regions.id, name, comments_count
                                                  FROM regions,
                                                      (SELECT region, COUNT(region) AS comments_count
                                                     FROM comments
                                                     GROUP BY region
                                                    )regs
                                                  WHERE id=region AND comments_count>5
                                               ''')
        return super().get(request, *args, **kwargs)


class GetRegion(BaseView):
    def post(self, request, *args, **kwargs):
        data = db.get_data_by_sql(
            'SELECT cities.id, name FROM cities, (SELECT id FROM regions WHERE name="%s")region WHERE region=region.id',
            (request['POST'].get('region_name'),))
        return json.dumps(data)
