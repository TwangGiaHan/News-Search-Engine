import nltk, unicodedata, json, os, re
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
dir_path = os.path.dirname(os.path.realpath(__file__))

nltk.download('stopwords')
nltk.download('wordnet')
def has_cyrillic(word):
    return bool(re.search('[а-яА-Я]', word))

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalize(content):
    # Clean digits
    text = ''.join([i for i in content if not i.isdigit()])

    # Clean punctuation and symbols
    text = re.sub("[!@#$+%*:()'-.,]", ' ', text)

    # filter out all Cyrillic letters
    text = [word for word in text.split() if not has_cyrillic(word)]
    text = [word for word in text if word not in stopwords.words('english')]
    text = to_lowercase(text)
    text = lemmatize_verbs(text)
    text = ' '.join(t for t in text)

    return text

with open('cnn.json', encoding="utf8") as json_data:
    articles = json.load(json_data)
    print(len(articles), "Articles loaded succesfully")
    statistic = {}
    for article in articles:
        title = article['title']
        author = article['author']
        cate = article['cate']
        content = article['content']
        source_url = article['source_url']
        if cate != None:
            newpath = dir_path + '\\tf-idf\\' + cate

            # keep track of what cate and number of txt files have been gone through
            if cate not in statistic:
                count = 0
                statistic[cate] = 0
            else:
                statistic[cate] += 1
            count = statistic[cate]

            # Create new cate folder when one not exists
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            file_name = str(count)+'.txt'
            complete_path = os.path.join(newpath, file_name)
            # f = open(complete_path, 'w', encoding="utf-8")
            # f.write('{}\n{}\n{}\n'.format(normalize(title), cate, normalize(content)))
            with open(complete_path, 'w', encoding="utf-8") as f:
                f.write('{}\n{}\n{}\n{}\n{}\n'.format(
                    normalize(title),
                    author,
                    cate,
                    normalize(content),
                    source_url
                ))
            f.close()