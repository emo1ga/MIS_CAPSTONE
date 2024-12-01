from bs4 import BeautifulSoup
import requests
import pandas as pd
sites = [
    { # 주석추가.
        "name": "한경",
        "url": "https://search.hankyung.com/search/news?query={keyword}&page={page}",
        "base_url": "https://www.hankyung.com",
        "article_selector": "ul.article > li",
        "title_selector": "div.txt_wrap > a",
        "content_selector": "div#articletxt"
    },
    {
        "name": "CNN",
        "url": "https://edition.cnn.com/search?q={keyword}&page={page}",
        "base_url": "https://edition.cnn.com",
        "article_selector": "div.cnn-search__result",
        "title_selector": "h3.cnn-search__result-headline > a",
        "content_selector": "div.l-container"
    }
    # 추가적인 사이트 설정 가능
]
def crawl_news_from_sites(sites, keyword, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102"
    }

    news_data = []

    for site in sites:
        print(f"크롤링 중: {site['name']}")
        for page in range(1, num_pages + 1):
            try:
                # 페이지 URL 생성
                page_url = site["url"].format(keyword=keyword, page=page)
                response = requests.get(page_url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                # 기사 목록 추출
                articles = soup.select(site["article_selector"])
                for article in articles:
                    try:
                        # 제목 추출
                        title_element = article.select_one(site["title_selector"])
                        title = title_element.get_text(strip=True) if title_element else "제목 없음"

                        # 링크 추출
                        link = title_element["href"] if title_element else "링크 없음"
                        if not link.startswith("http"):
                            link = site["base_url"] + link

                        # 본문 추출
                        article_response = requests.get(link, headers=headers)
                        article_soup = BeautifulSoup(article_response.text, "html.parser")
                        content_element = article_soup.select_one(site["content_selector"])
                        content = content_element.get_text(strip=True) if content_element else "본문 없음"

                        # 데이터 저장
                        news_data.append({
                            "사이트": site["name"],
                            "제목": title,
                            "링크": link,
                            "내용": content
                        })

                    except Exception as e:
                        print(f"기사 처리 중 오류 발생: {e}")
                        continue

            except Exception as e:
                print(f"{site['name']}의 {page}페이지 처리 중 오류 발생: {e}")
                continue

    return news_data

# 크롤링 대상 사이트 설정
sites = [
    {
        "name": "한경",
        "url": "https://search.hankyung.com/search/news?query={keyword}&page={page}",
        "base_url": "https://www.hankyung.com",
        "article_selector": "ul.article > li",
        "title_selector": "div.txt_wrap > a",
        "content_selector": "div#articletxt"
    },
    {
        "name": "네이버 뉴스",
        "url": "https://search.naver.com/search.naver?where=news&query={keyword}&start={page}",
        "base_url": "",
        "article_selector": "div.news_area",
        "title_selector": "a.news_tit",
        "content_selector": "div#articleBodyContents"
    }
    # 다른 사이트 추가 가능
]

# 크롤링 실행
keyword = "금 ETF"  # 조사하고자 하는 키워드
num_pages = 2       # 페이지 수 설정

news_data = crawl_news_from_sites(sites, keyword, num_pages)

# 결과를 CSV로 저장
df = pd.DataFrame(news_data)
csv_filename = f"{keyword.replace(' ', '_')}_news.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
print(f"크롤링 결과가 {csv_filename}로 저장되었습니다.")