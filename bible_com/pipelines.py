# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs

from bible_com.items import Book, Verse


BOOKS_ORDER = [
    'gen',
    'exo',
    'lev',
    'num',
    'deu',
    'jos',
    'jdg',
    'rut',
    '1sa',
    '2sa',
    '1ki',
    '2ki',
    '1ch',
    '2ch',
    'ezr',
    'neh',
    'est',
    'job',
    'psa',
    'pro',
    'ecc',
    'sng',
    'isa',
    'jer',
    'lam',
    'ezk',
    'dan',
    'hos',
    'jol',
    'amo',
    'oba',
    'jon',
    'mic',
    'nam',
    'hab',
    'zep',
    'hag',
    'zec',
    'mal',
    'mat',
    'mrk',
    'luk',
    'jhn',
    'act',
    'rom',
    '1co',
    '2co',
    'gal',
    'eph',
    'php',
    'col',
    '1th',
    '2th',
    '1ti',
    '2ti',
    'tit',
    'phm',
    'heb',
    'jas',
    '1pe',
    '2pe',
    '1jn',
    '2jn',
    '3jn',
    'jud',
    'rev',
]


class VersePipeline(object):

    def __init__(self):
        self.translations = {}

    def process_item(self, item, *args):
        tran = item['translation']
        if tran in self.translations:
            translation_data = self.translations[tran]
        else:
            translation_data = {
                'books': {},
                'verses': [],
            }
            self.translations[tran] = translation_data

        translation_data = self.translations[item['translation']]
        if isinstance(item, Verse):
            verse = u'{} {}:{} {}\n'.format(
                item['book'], item['chapter'], item['verse'], item['text'],
            )
            translation_data['verses'].append({
                'verse': verse,
                'index': (
                    BOOKS_ORDER.index(item['book']) * 10**6 +
                    item['chapter'] * 1000 +
                    item['verse']
                ),
            })
        elif isinstance(item, Book):
            translation_data['books'][item['shortname']] = item['fullname']

    def close_spider(self, spider):
        for translation, translation_data in self.translations.items():
            filepath = u'trans/{}.bible'.format(translation)
            with codecs.open(filepath.encode('utf8'), 'w', 'utf-8') as f:
                f.write(translation + '\n')
                f.write('# BOOKS LIST\n')
                f.writelines([
                    u'{} {}\n'.format(shortname, fullname)
                    for shortname, fullname in
                    sorted(
                        translation_data['books'].items(),
                        key=lambda book: BOOKS_ORDER.index(book[0]),
                    )
                ])
                f.write('# TEXT\n')
                lines = [
                    verse['verse'] for verse in
                    sorted(
                        translation_data['verses'],
                        key=lambda verse: verse['index'],
                    )
                ]
                f.writelines(lines)
