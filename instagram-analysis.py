from models import (
    InstagramCommentScraper,
    TextTranslator,
    SentimentAnalysis,
    CSVExporter,
)

try:
    from settings import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_CONTENT_URL
except ModuleNotFoundError as e:
    print(
        "settings.py file not found. Please create one and add INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_CONTENT_URL variables."
    )
    exit()

scraper = InstagramCommentScraper(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
scraped_comments = scraper.get_comments(INSTAGRAM_CONTENT_URL)
comments = []

for comment in scraped_comments:
    # Translate each comment to english
    comment_text_en = TextTranslator.to_english(comment["content"])
    # Analyze each comment's sentiment in src language (polarity, subjectivity, afinn_score)
    polarity, subjectivity = SentimentAnalysis.analyze(comment["content"])
    afinn_score = SentimentAnalysis.analyze_afinn(comment["content"])
    # Analyze each comment's sentiment in en language (polarity_en, subjectivity_en, afinn_score_en)
    polarity_en, subjectivity_en = SentimentAnalysis.analyze(comment_text_en)
    afinn_score_en = SentimentAnalysis.analyze_afinn(comment_text_en)

    comment_dict = {
        "user_pk": comment["author"]["id"],
        "name": comment["author"]["name"],
        "profile_pic_url": comment["author"]["thumbnails"][0]["url"],
        "text": comment["content"],
        "text_translated": comment_text_en,
        "published": comment["published"],
        "like_count": comment["votes"]["simpleText"],
        "reply_count": comment["replyCount"],
        "polarity": polarity,
        "subjectivity": subjectivity,
        "afinn_score": afinn_score,
        "polarity_en": polarity_en,
        "subjectivity_en": subjectivity_en,
        "afinn_score_en": afinn_score_en,
    }
    print(comment_dict)
    comments.append(comment_dict)

csv_exporter = CSVExporter()
csv_exporter.export(comments)

print("completed main.py successfully")