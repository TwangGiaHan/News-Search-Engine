import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pickle

dir_path = os.path.dirname(os.path.realpath(__file__))

def label(cate):
    return {
        'business': 0,
        'entertainment': 1,
        'health': 2,
        'sport': 3,
        'style': 4
    }.get(cate, 5)


listFolder = ['business', 'entertainment', 'health', 'sport', 'style']


def count_number_of_files(cate):
    return len(next(os.walk("{}\\{}".format(dir_path, cate)))[2])

def get_all_filelists():
    file_list = []
    for cate in listFolder:
        num_of_files = count_number_of_files(cate)
        file_list.extend([os.path.join(dir_path, cate, f"{i}.txt") for i in range(num_of_files)])
    return file_list

def get_texts_for_tfidf():
    filelist = get_all_filelists()
    texts = []
    for filepath in filelist:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
            # Lấy dòng 1 (tiêu đề) và dòng 4 (nội dung), nếu đủ dòng
            title = lines[0].strip() if len(lines) > 0 else ""
            content = lines[3].strip() if len(lines) > 3 else ""
            texts.append(f"{title} {content}")
    return texts

def exportTFIDF():
    texts = get_texts_for_tfidf()
    tf_idf_vec = TfidfVectorizer().fit(texts)
    tf_idf = tf_idf_vec.transform(texts).toarray()
    # Lưu vectorizer
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(tf_idf_vec, f)
    return tf_idf, tf_idf_vec


def label_tf_idf():
    tf_idf, _ = exportTFIDF()
    lb = [[]]
    for cate in listFolder:
        num_of_files = count_number_of_files(cate)
        label_num = label(cate)
        # Y matrix
        label_matrix = np.full((1, num_of_files), label_num, dtype=int)
        lb = np.append(lb, label_matrix, axis=1)
    tf_idf = np.append(tf_idf, np.matrix.transpose(lb), axis=1)
    np.savetxt('./knn/tf_idf.csv', tf_idf, fmt='%.5f', delimiter=',')


def build_metadata():
    filelist = get_all_filelists()
    metadata = []
    for filepath in filelist:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()
            title = lines[0].strip() if len(lines) > 0 else ""
            author = lines[1].strip() if len(lines) > 1 else ""
            cate = lines[2].strip() if len(lines) > 2 else ""
            url = lines[4].strip() if len(lines) > 4 else ""
            metadata.append({
                "title": title,
                "author": author,
                "cate": cate,
                "source_url": url
            })
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def save_tfidf_matrix():
    tfidf, _ = exportTFIDF()
    np.save("tfidf_matrix.npy", tfidf)

label_tf_idf()
build_metadata()
save_tfidf_matrix()



