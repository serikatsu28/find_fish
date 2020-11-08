from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# APIキーとシークレットの指定
key = '4b33730081d57ce75cb990cff164af9e'
secret = '025688e8ef0bb045'
wait_time = 1

# キーワードとディレクトリ名を指定
def main():
    go_download(検索ワード, ディレクトリ名)

# Flickr APIで写真を検索
def go_download(keyword, dir):
    # 画像の保存パスを決定
    savedir = './image/' + dir
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    # APIを使ってダウンロード
    flickr = FlickrAPI(key, secret, format='parsed-json')
    flickr_search = flickr.photos.search(
      text = keyword,     # 検索ワード
      per_page = 500,     # 取得件数
      media = 'photos',   # 写真を検索
      sort = 'relevance', # 関連順に並べる
      safe_search = 1,    # セーフサーチ
      extras = 'url_q, license')
    # 検索結果を確認
    photos = flickr_search['photos']
    pprint(photos)
    try:
        # 1枚ずつ画像をダウンロード
        for i, photo in enumerate(photos['photo']):
            url_q = photo['url_q']
            filepath = savedir + '/' + photo['id'] + '.jpg'
            if os.path.exists(filepath):
                continue
            print(str(i + 1) + ':download=', url_q)
            urlretrieve(url_q, filepath)
            time.sleep(wait_time)
    except:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
