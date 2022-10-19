import requests
from bs4 import BeautifulSoup

def grab_audio_link(soup):
    """We can find the audio download button under wrapper > primary audio >
    audio-module-tools > audio-tool audio-tool-download ...."""
    audio_container = soup.find("li", class_ ="audio-tool audio-tool-download")
    attributes = audio_container.find("a")
    print(attributes['href'])

def extract_transcript(soup) -> list[str]:
    audio_tool_transcript = soup.find("li", class_="audio-tool audio-tool-transcript").a.get("href")

    page = requests.get(audio_tool_transcript)
    transcript_soup = BeautifulSoup(page.content, "html.parser")

    text_container = transcript_soup.find(class_ = "transcript storytext")
    text_tags = text_container.find_all("p")[:-2] # Last two lines are just disclaimers and copyright
    sentences = []
    for lines in text_tags:
        sentences.append(lines.text)

    return sentences

def extract_metadata(soup):
    title = soup.find("div", class_ = 'storytitle').get_text().strip("\n")
    # todo add speakers
    date = soup.find("span", attrs={"class":"date"}).text.strip().split('/')[0]
    return title, date


if __name__ == "__main__":
    url = "https://www.npr.org/2012/09/28/161974470/week-in-politics-u-n-general-assembly-debates"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(extract_transcript(soup))


