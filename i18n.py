import gettext
from pathlib import Path

from fastapi import Depends, Query, Request

LOCALES_DIR = Path(__file__).parent / "locales"
SUPPORTED_LANGUAGES = ["en", "fa"]
DEFAULT_LANGUAGE = "en"

# بارگذاری همه‌ی ترجمه‌ها یک بار، هنگام شروع برنامه
translations = {
    lang: gettext.translation(
        "messages", localedir=LOCALES_DIR, languages=[lang], fallback=True
    )
    for lang in SUPPORTED_LANGUAGES
}


def parse_accept_language(header: str) -> list[str]:
    """هدر Accept-Language را به لیست زبان‌ها به ترتیب اولویت تبدیل می‌کند."""
    languages = []
    for part in header.split(","):
        pieces = part.strip().split(";q=")
        code = pieces[0].split("-")[0].lower()
        try:
            quality = float(pieces[1]) if len(pieces) > 1 else 1.0
        except ValueError:
            quality = 0.0
        languages.append((quality, code))

    languages.sort(key=lambda item: item[0], reverse=True)
    return [code for _, code in languages]


def get_language(request: Request, lang: str | None = Query(default=None)) -> str:
    """زبان کاربر را تشخیص می‌دهد: اول از ?lang= بعد از هدر، در غیر این صورت پیش‌فرض."""
    if lang:
        code = lang.split("-")[0].lower()
        if code in SUPPORTED_LANGUAGES:
            return code

    header = request.headers.get("accept-language", "")
    for code in parse_accept_language(header):
        if code in SUPPORTED_LANGUAGES:
            return code

    return DEFAULT_LANGUAGE


def get_translator(language: str = Depends(get_language)):
    """تابع ترجمه‌ی مخصوص زبان همین درخواست را برمی‌گرداند."""
    return translations[language].gettext