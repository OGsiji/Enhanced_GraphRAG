# from dataclasses import dataclass


# @dataclass
# class URL:
#     url1: str = "https://www.rottentomatoes.com/m/side_by_side_2012"
#     url2: str = "https://www.rottentomatoes.com/m/matrix"
#     url3: str = "https://www.rottentomatoes.com/m/matrix_revolutions"
#     url4: str = "https://www.rottentomatoes.com/m/matrix_reloaded"
#     url5: str = "https://www.rottentomatoes.com/m/speed_1994"


from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class URL:
    urls: Dict[str, str] = field(
        default_factory=lambda: {
            "url1": "https://www.rottentomatoes.com/m/side_by_side_2012",
            "url2": "https://www.rottentomatoes.com/m/matrix",
            "url3": "https://www.rottentomatoes.com/m/matrix_revolutions",
            "url4": "https://www.rottentomatoes.com/m/matrix_reloaded",
            "url5": "https://www.rottentomatoes.com/m/speed_1994",
        }
    )

    def add_url(self, url: str) -> None:
        """Add a new URL to the collection"""
        new_key = f"url{len(self.urls) + 1}"
        self.urls[new_key] = url

    def remove_url(self, url_key: str) -> None:
        """Remove a URL by its key"""
        if url_key in self.urls:
            del self.urls[url_key]
            # Reindex remaining URLs
            new_urls = {}
            for i, (_, url) in enumerate(sorted(self.urls.items()), 1):
                new_urls[f"url{i}"] = url
            self.urls = new_urls

    def get_all_urls(self) -> List[str]:
        """Get all URLs as a list"""
        return list(self.urls.values())

    def clear_urls(self) -> None:
        """Clear all URLs"""
        self.urls = {}
