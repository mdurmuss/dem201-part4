# Madde6 (GAME of THRONES)

Ben Datagrip kullanarak veritabanında işlemler gerçekleştiriyorum. Orada bir console açıp aşağıdaki sorguları yazarsanız cevapları görebilirsiniz.

Öncelikle her bir sorguda ihtiyacım olacak olan verileri şu sorgularla elde ettim.

```sql
SELECT t.title_id
      FROM imdb.title_basics t where primary_title = 'Game of Thrones';

-- dizinin ID'sine göre tüm bölümlerin ID'lerini bul.
CREATE TABLE result SELECT t.title_id,t.season_number,t.episode_number
      FROM imdb.title_episode t where parent_title_id = 'tt0944947';
```

Bu noktadan itibaren **result** tablosu ile title-ratings tablosunu join ile birleştirip istediğim sonuçları buldum.

- 6.A

  ```sql
  -- 6.A  21s 122ms
  SELECT r.*,ra.average_rating FROM result r join imdb.title_ratings ra on r.title_id = ra.title_id ORDER BY ra.average_rating DESC limit 5;
  ```

  ![6a](/Users/md/mustafa/dem201/homework/data2base/madde6/images/6a.png)

- 6.B

  ```sql
  -- 6.B  23s 456ms
  SELECT r.*,ra.average_rating FROM result r join imdb.title_ratings ra on r.title_id = ra.title_id ORDER BY ra.average_rating limit 5;
  ```

  ![6b](/Users/md/mustafa/dem201/homework/data2base/madde6/images/6b.png)

- 6.C

  ```sql
  -- 6.C  18s 166 ms
  SELECT r.*,ra.num_votes FROM result r join imdb.title_ratings ra on r.title_id = ra.title_id ORDER BY ra.num_votes DESC limit 5;
  ```

  ![6c](/Users/md/mustafa/dem201/homework/data2base/madde6/images/6c.png)

- 6.D

```sql
-- 6.D 17s 776ms
SELECT r.*,ra.num_votes FROM result r join imdb.title_ratings ra on r.title_id = ra.title_id ORDER BY ra.num_votes limit 5;
```

![6d](/Users/md/mustafa/dem201/homework/data2base/madde6/images/6d.png)

