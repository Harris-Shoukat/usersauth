import requests
from django.conf import settings


def get_google_suggestions(query):
    response = requests.get(
        settings.GOOGLE_SUGGEST_URL,
        params={
            "client": "firefox",
            "q": query,
        },
        timeout=5,
    )

    response.raise_for_status()

    data = response.json()

    return data[1]
