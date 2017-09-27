rdd_bible.count()
rdd_bible_cleaned.count()


x = rdd_bible_cleaned.collect()
x = rdd_bible.collect()

import numpy as np


x = numpy.array(x)
x2 = np.array(list(map(lambda v: re.sub(r'(?=03:019:024)(.*)(?=03:019:025)', '', v) , x)))

np.size(x)
np.size(x2)


numpy.size((numpy.where(x == "03019024")))

x2 = re.sub(r'(?=03:019:024)(.*)(?=03:019:025)', '', x)

(03:019:024.*)


arr = np.array(["AB", "AC", "XAB", "XAC", "AD"])
print(np.array(list(map(lambda v: re.sub(r'^A','XA', v) ,arr))))








table2.count()

rdd_bible_cleaned.subtract("03019024")


rdd_bible.regexp_replace("03:019:024")

rdd_bible_cleaned.count()
rdd_bible_cleaned.take(20)



^.*\b(03:019:024)\b.*$
  
  /^(.*?)abc/
  
  rdd_bible.count()
x = rdd_bible.subtract("god")

rdd_bible = rdd_bible.flatMap(clean_up)
rdd_bible.count()
rdd_bible

table2 = rdd_bible.filter(lambda x: "[^^](03:019:024).*[0-9]" not in x)
table2.count()

sentence = regexp_replace(trim(lower(column)), '\\*\s\W\s*\\*_', '')


rdd_bible.take(5)









rdd_ulysess_all = rdd_bible.map(lambda x: x.filter(lambda re.sub(r'([03:019:024])', ''))
                                
                                .filter("03:019:024")
                                x.take(5)
                                
                                rdd_bible.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
                                
                                
                                rdd_ulysess = rdd_ulysses.flatMap(clean_up)
                                rdd_ulysess_all = rdd_ulysess.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
                                
                                
                                rdd_ulysess.count()
                                x.count()
                                # Remove stopwords
                                rdd_ulysess_all.count()
                                rdd_stopwords.count()
                                x.take(100)
                                
                                sc.stop()
                                