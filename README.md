## DEM201

**Not:**
- Verisetlerini MySQL'e kayıt eden uygulamanızı bir Github repository'si haline getirmeli. 
- linkini ödevle birlikte paylaşmalısınız. 
- Hazırladığınız repo bir README dosyası içermelidir ve herhangi bir IDE'ye ihtiyaç duymadan kodun nasıl çalıştırılabileceğini detaylıca anlatmalıdır.
- Lütfen olabildiğiniz kadar ayrıntılı şekilde (gerektiğini düşündüğünüz yerlerde fazladan ayrıntı vererek) detaylı bir README hazırlamaya çalışın.
<hr>

### Aşamalar
1. Docker üzerinde bir MariaDB oluşturuldu.

2. Her bir veriseti için ayrı tablolar oluşturuldu.

   - title_principals
   - title_akas
   - title_basics
   - name_basics
   - title_crew
   - title_episode
   - title_ratings
   
3. **Her bir tabloya ilgili veriyi eklemek için verisetiyle aynı isimde 7 fonksiyon** oluşturuldu. Bir örnek üzerinde detaylı anlatmak daha iyi olacaktır. Kod üzerindeki yorum satırlarına dikkat edebilirsiniz.

   ```python
   # Veritabanı bağlantısı aşağıdaki fonksiyon ile gerçekleştirildi.
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

   Burada bir örnek üzerinden anlattım. Kod içerisinde diğer fonksiyonları da görebiliriz. Main fonksiyonu içerisinde hepsi sırayla(dosya boyutuna göre bir sıralama yaptım.) çağrılıyor ve veritabanına yazılıyor.

4. CSV dosyaları for içerisinde okunurken maksimum bir okunma satır sayısı var. Burada bu hatayı **title_akas** verisini yazarken aldım. Bu yüzden fonksiyon içerisinde bu maksimum değeri yükselten ayrı bir fonksiyon bulunmakta.

