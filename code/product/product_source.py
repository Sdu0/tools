# -*- coding: utf-8 -*-
import re
import time
from mysql import query, query_one, save


def get_html():
    with open("/home/sdu/Project/tools/code/product/product_source.html", "r") as f:
        return f.read()


def save_database():
    html_source = get_html()
    items = re.findall(re.compile(
        r'_a" class="level(.+?)" treenode_a="" onclick="" target="_blank" style="" title="(.*?)">'), html_source)

    for index, item in enumerate(items):
        level = item[0]
        name = item[1]
        if not query(sql=u'SELECT id FROM product WHERE name=%s and level=%s', list1=(name, level, )):
            if level == u'1':
                save(sql=u'INSERT INTO `product`(`name`, `level`) VALUES(%s, %s)', list1=(
                    name, level))
            else:
                parent_id = query(sql=u'SELECT id FROM product WHERE level=%s ORDER BY id DESC LIMIT 0, 1', list1=(
                    int(level) - 1, ))[0].get('id')
                save(sql=u'INSERT INTO `product`(`name`, `level`, `parent_id`) VALUES(%s, %s, %s)', list1=(
                    name, level, parent_id))

        time.sleep(1)


def main():
    tree = []

    level_1 = []
    for one in query(sql=u'SELECT id, name FROM product WHERE level=1'):
        level_1_id = one.get('id')
        level_1_name = one.get('name')

        level_2 = []
        for two in query(sql=u'SELECT id, name FROM product WHERE level=2 and parent_id = %s', list1=(level_1_id,)):
            level_2_id = two.get('id')
            level_2_name = two.get('name')

            level_3 = []
            for three in query(sql=u'SELECT id, name FROM product WHERE level=3 and parent_id = %s', list1=(level_2_id,)):
                level_3_id = three.get('id')
                level_3_name = three.get('name')

                level_4 = []
                for four in query(sql=u'SELECT id, name FROM product WHERE level=4 and parent_id = %s', list1=(level_3_id,)):
                    level_4_id = four.get('id')
                    level_4_name = four.get('name')

                    level_5 = []
                    for five in query(sql=u'SELECT id, name FROM product WHERE level=5 and parent_id = %s', list1=(level_4_id,)):
                        level_5_id = five.get('id')
                        level_5_name = five.get('name')
                    
                        level_6 = []
                        for six in query(sql=u'SELECT id, name FROM product WHERE level=6 and parent_id = %s', list1=(level_5_id,)):
                            level_6_id = six.get('id')
                            level_6_name = six.get('name')
                        
                            level_7 = []
                            for seven in query(sql=u'SELECT id, name FROM product WHERE level=7 and parent_id = %s', list1=(level_6_id,)):
                                level_7_id = seven.get('id')
                                level_7_name = seven.get('name')

                            level_6.append({
                                "text": level_6_name,
                                'nodes':level_7})
                        level_5.append({
                            "text": level_5_name,
                            'nodes':level_6})
                    level_4.append({
                        "text": level_4_name,
                        'nodes':level_5})
                level_3.append({
                    "text": level_3_name,
                    'nodes':level_4})
            level_2.append({
                "text": level_2_name,
                'nodes':level_3})
        level_1.append({
            "text": level_1_name,
            'nodes':level_2
            })
    tree.append({
        "text": level_1_name,
        'nodes':level_1
        })
    print tree


if __name__ == '__main__':
    main()
