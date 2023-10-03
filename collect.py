import bs4
import requests
import pandas as pd

from bs4 import BeautifulSoup


def get_elements(url: str, selector=".o-contentTimeline__item") -> list:
    """
    記事一覧を取得
    """
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, ' \
                                    'like Gecko) Chrome/34.0.1847.131 Safari/537.36'

    res = session.get(url)

    soup = BeautifulSoup(res.text, "html.parser")
    # 記事一覧
    elements = soup.select(selector)

    return elements


def get_note_info(elements: list, name: str, parser, base_df: pd.DataFrame) -> pd.DataFrame:
    """
    記事一覧から、タイトル、投稿日、いいね数を取得
    """
    # タイトル、投稿日、いいね数
    parsed = list(map(parser, elements))

    df = pd.DataFrame(parsed)
    df["team_name"] = name

    note_info = pd.concat([base_df, df], ignore_index=True)
    return note_info


def get_text(element: bs4.ResultSet, selector: str) -> str:
    result = element.contents[0].select(selector)
    return "" if len(result) == 0 else result[0].text


def parse_smarthr_note_info(element: bs4.ResultSet) -> dict:
    # note tile
    title = get_text(element, "h3")
    # published date
    date_ = element.contents[0].select(".m-noteUser__date")[0].next.attrs['datetime']
    # likes
    like_ = get_text(element, "span.text-clickable.pl-2.text-sm").replace("\n", "").replace(" ", "")

    return {"title": title, "date": date_, "likes": like_}


def parse_layerx_note_info(element: bs4.ResultSet) -> dict:
    # note tile
    title = get_text(element, "h3").replace("\n", "").replace(" ", "")
    # published date
    date_ = get_text(element, ".o-timelineFooter__date")
    # likes
    like_ = get_text(element, "span.text-clickable.pl-2.text-sm").replace("\n", "").replace(" ", "")

    return {"title": title, "relative_date": date_, "likes": like_}


def parse_kyash_note_info(element: bs4.ResultSet) -> dict:
    # note tile
    title = get_text(element, "h3").replace("\n", "").replace(" ", "")
    # published date
    date_ = element.contents[0].select("time")[0].attrs["datetime"]
    # likes
    like_ = get_text(element, ".o-noteLikeV3__count").replace("\n", "").replace(" ", "")

    return {"title": title, "date": date_, "likes": like_}


if __name__ == "__main__":
    note_info = pd.DataFrame()

    # ---
    # SmartHR プロダクトデザイン
    url = "https://note.com/smarthr_co/m/m0b87dcc52cb0"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "SmartHR プロダクトデザイン", parse_smarthr_note_info, note_info)

    # ---
    # LayerX Design Magazine
    url = "https://note.layerx.co.jp/m/mbf4be3d31af8"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "LayerX Design Magazine", parse_layerx_note_info, note_info)

    # ---
    # Kyash Design Team
    url = "https://note.com/kyash_designers/m/mdf85f6f4a909"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "Kyash Design Team", parse_kyash_note_info, note_info)

    # ---
    # MoneyForward
    url = "https://note.com/mfdesign/m/m7587cb2186f5"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "マネーフォワード・デザイン", parse_smarthr_note_info, note_info)

    # ---
    # Visional
    url = "https://blog.visional.inc/m/mae2d31341ff7"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "Visional Designer", parse_smarthr_note_info, note_info)

    # Tangity (NTT Data)
    url = "https://note.com/tangity/m/mce037e27e0ac"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "Tangity (NTTデータ)", parse_smarthr_note_info, note_info)

    # Livesense
    url = "https://note.com/livesense_design/m/m776af1726bfd"

    # 記事一覧
    elements = get_elements(url)

    note_info = get_note_info(elements, "Livesense designers", parse_smarthr_note_info, note_info)

    # output
    note_info.to_csv("./design-team-note-likes.csv", index=False)
