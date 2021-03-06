#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa.durmus@albert.health]

# Module Imports
import mariadb
import csv
from tqdm import tqdm


def connect_db():
    print("Connected to MariaDB.")
    conn = mariadb.connect(
        user="root",
        password="new_password",
        host="127.0.0.1",
        port=3306,
        database="imdb")

    # Get Cursor
    cur = conn.cursor()

    return cur, conn


def title_rating():
    print("Title Rating processing...")

    # connect db
    cur, conn = connect_db()

    # open and read data.
    file = csv.reader(open("./dataset/title.ratings.tsv"), delimiter="\t")

    # create the query.
    query = "INSERT INTO title_ratings (title_id, average_rating, num_votes) VALUES (?, ?, ?)"
    data = []

    # tqdm for detecting time.
    for idx, row in tqdm(enumerate(file)):

        if idx == 0:  # continue over column names.
            continue

        tconst = row[0]
        average_rating = float(row[1])
        num_votes = int(row[2])

        data.append(tuple([tconst, average_rating, num_votes]))

        # daha hızlı veri yazmak için batch halinde gönderiyoruz.
        if idx % 10000 == 0:
            cur.executemany(query, data)
            data = []

    conn.commit()
    cur.close()


def title_episode():
    print("Title Episode processing...")

    cur, conn = connect_db()
    read_tsv = csv.reader(open("./dataset/title.episode.tsv"), delimiter="\t")

    data = []
    query = "INSERT INTO title_episode (title_id, parent_title_id, season_number, episode_number) VALUES (?, ?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:
            continue
        try:  # eğer bazı veriler boşsa veya yanlışsa o satır atlanacak.
            row1 = row[0]
            row2 = row[1]
            row3 = int(row[2])
            row4 = int(row[3])
        except:
            continue
        # veri tuple olarak eklenmeli.
        data.append(tuple([row1, row2, row3, row4]))

        if idx % 10000 == 0:
            cur.executemany(query, data)
            data = []

    conn.commit()
    cur.close()


def title_crew():
    print("Title crew processing...")

    cur, conn = connect_db()

    read_tsv = csv.reader(open("./dataset/title.crew.tsv"), delimiter="\t")

    data = []
    QUERY = "INSERT INTO title_crew (title_id, director_title_id, writers_title_id) VALUES (?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:  # sütun isimlerini atla.
            continue
        try:
            row1 = row[0]
            row2 = row[1]
            row3 = row[2]
        except:
            continue
        data.append(tuple([row1, row2, row3]))

        if idx % 10000 == 0:
            cur.executemany(QUERY, data)
            data = []

    conn.commit()
    cur.close()


def name_basics():
    print("Name Basics processing...")
    cur, conn = connect_db()
    tsv_file = open("./dataset/name.basics.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    data = []
    QUERY = "INSERT INTO name_basics (title_id, primary_name, birth_year, death_year, primary_profession, known_for_titles_id) VALUES (?, ?, ?, ?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:  # sütun isimlerini atla.
            continue
        try:
            row1 = row[0]
            row2 = row[1]
            row3 = int(row[2])
            row4 = int(row[3])
            row5 = row[4]
            row6 = row[5]
        except:
            continue
        data.append(tuple([row1, row2, row3, row4, row5, row6]))

        if idx % 10000 == 0:
            cur.executemany(QUERY, data)
            data = []

    conn.commit()
    cur.close()


def title_basics():
    print("Title basics processing...")
    cur, conn = connect_db()
    tsv_file = open("./dataset/title.basics.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    data = []
    QUERY = "INSERT INTO title_basics (title_id, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:  # sütun isimlerini atla.
            continue
        try:
            row1 = row[0]
            row2 = row[1]
            row3 = row[2]
            row4 = row[3]
            row5 = bool(int(row[4]))
            row6 = int(row[5])
            row7 = int(row[6])
            row8 = int(row[7])
            row9 = row[8]
        except:
            continue
        data.append(tuple([row1, row2, row3, row4, row5, row6, row7, row8, row9]))

        if idx % 10000 == 0:
            cur.executemany(QUERY, data)
            data = []

    conn.commit()
    cur.close()


def make_csv_limit_maximum():
    import sys
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)


def title_akas():
    print("Title_akas processing...")
    # bir for döngüsünde csv dosyasından okuyabileceğiniz max satır sayısı vardır.
    # bu verisetinde biz bunu aşıyoruz.
    # bu limiti maksimuma çekmek için bir fonksiyon yazıldı.
    make_csv_limit_maximum()

    cur, conn = connect_db()
    tsv_file = open("./dataset/title.akas.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    data = []
    QUERY = "INSERT INTO title_akas (title_id, ordering, title, region, language, types, attribute, is_original_title) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:  # sütun isimlerini atla.
            continue
        try:
            row1 = row[0]
            row2 = int(row[1])
            if len(row[2]) > 8000:
                continue
            row3 = row[2]
            row4 = row[3]
            row5 = row[4]
            row6 = row[5]
            row7 = row[6]
            row8 = bool(int(row[7]))
        except:
            continue
        data.append(tuple([row1, row2, row3, row4, row5, row6, row7, row8]))

        if idx % 50000 == 0:
            cur.executemany(QUERY, data)
            data = []

    conn.commit()
    cur.close()


def title_principals():
    print("Title Principals processing...")
    cur, conn = connect_db()
    tsv_file = open("./dataset/title.principals.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    data = []
    QUERY = "INSERT INTO title_principals (title_id, ordering, name_id, job_category, job, characters) VALUES (?, ?, ?, ?, ?, ?)"

    for idx, row in tqdm(enumerate(read_tsv)):

        if idx == 0:  # sütun isimlerini atla.
            continue
        try:
            row1 = row[0]
            row2 = int(row[1])
            row3 = row[2]
            row4 = row[3]
            row5 = row[4]
            row6 = row[5]
        except:
            continue
        data.append(tuple([row1, row2, row3, row4, row5, row6]))

        if idx % 50000 == 0:
            cur.executemany(QUERY, data)
            data = []

    conn.commit()
    cur.close()



if __name__ == '__main__':
    title_rating()
    title_episode()
    title_crew()
    name_basics()
    title_basics()
    title_akas()
    title_principals()
