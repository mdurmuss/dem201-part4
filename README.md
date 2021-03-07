## DEM201

## Kullanım

- Öncelikle daha önceki aşamada oluşturduğumuz veritabanını docker üzerinde çalıştırmalısınız. Docker desktop üzerinde kolayca çalıştırılabilir.
- Verisetindeki 7 dosyayı **dataset**/ isimli yeni bir klasör açıp içerisine eklemelisiniz.
- Aşağıdaki komutları çalıştırdığınızda tablolarınız verisetindeki ilgili kısımlar ile doldurulmaya başlanacak.

```shell
brew install mariadb-connector-c
pip3 install -r requirements.txt
python main.py	
```

## Nasıl Çalışıyor?

**Her bir tabloya ilgili veriyi eklemek için verisetiyle aynı isimde 7 fonksiyon** oluşturuldu. Bir örnek üzerinde detaylı anlatmak daha iyi olacaktır. Kod üzerindeki yorum satırlarına dikkat edebilirsiniz.

```python
# Veritabanı bağlantısı aşağıdaki fonksiyon ile gerçekleştirildi.
# burada oluşturduğunuz veritabanı ismi ve şifrenizi değiştirmeniz gerekli.
def connect_db():
    print("Connected to MariaDB.")
    conn = mariadb.connect(
        user="root",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="imdb")

    # Get Cursor
    cur = conn.cursor()

    return cur, conn
```

```python
# title-ratings verisetinden title_ratings tablosuna veri aktaran fonksiyon
def title_rating():
    print("Title Rating processing...")

    cur, conn = connect_db()
    # veritabanına bağlantıyı sağladık. buradaki cur ve conn değişkenleri ilerde veritabanını güncellemeye ve kapatmaya yarayacak.

    # ilgili tsv dosyasını okur.
    file = csv.reader(open("./dataset/title.ratings.tsv"), delimiter="\t")

    # bu verisetinde 3 adet sütun var. Tabloyu db'de oluştururken bu sütun isimlerinin kullanılması önemli. Yoksa hata verir.
    query = "INSERT INTO title_ratings (title_id, average_rating, num_votes) VALUES (?, ?, ?)"

    # satırlar batch'ler halinde veritabanına yazılacak. bu satırları tutacağım değişkeni tanımladım.
    data = []

    # tqdm for detecting time.
    for idx, row in tqdm(enumerate(file)):

        if idx == 0:  # continue over column names.
            continue

        tconst = row[0]
        average_rating = float(row[1])
        num_votes = int(row[2])

        # ÖNEMLİ: veriler bir dizi içerisinde tuple olarak tutulmalı.
        data.append(tuple([tconst, average_rating, num_votes]))

        # daha hızlı veri yazmak için batch halinde gönderiyoruz.
        if idx % 10000 == 0:
            cur.executemany(query, data)
            data = [] # veriyi yazdıktan sonra batch boşaltılır.

            
    # tüm veri yazıldıktan sonra db güncelle ve bağlantıyı kapat.
    conn.commit()
    cur.close()

```

Burada bir örnek üzerinden anlattım. Kod içerisinde diğer fonksiyonları da görebiliriz. Main fonksiyonu içerisinde hepsi sırayla(dosya boyutuna göre sıralı) çağrılıyor ve veritabanına yazılıyor.

## Ekstra

1. Her bir satırı tek tek veritabanına göndermek oldukça vakit kaybettiriyor. Batch'ler halinde yazmak süreyi oldukça azalttı.
2. CSV dosyaları for içerisinde okunurken maksimum bir okunma satır sayısı var. Burada bu hatayı **title_akas** verisini yazarken aldım. Bu yüzden fonksiyon içerisinde bu maksimum değeri yükselten ayrı bir fonksiyon bulunmakta.

