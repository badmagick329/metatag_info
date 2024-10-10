from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup as bs


@dataclass
class MetaTag:
    name: str
    content: str

    def to_markdown(self) -> str:
        return "\n".join([f"## {self.name}\n", f"{self.content}\n"])


class MetaTagInfo:
    _url: str
    _selected_tags: list[str] | None
    meta_tags: list[MetaTag]
    status_code: int | None

    def __init__(
        self,
        url: str,
        selected_tags: list[str] | None,
    ) -> None:
        self._url = url
        self._selected_tags = selected_tags
        self.meta_tags = list()
        self.status_code = None

    def fetch(self) -> None:
        try:
            response = requests.get(self._url, timeout=3)
        except Exception:
            self.status_code = 500
            return

        self.status_code = response.status_code
        if not self.status_code == 200:
            return

        self._parse(response)

    def _parse(self, response: requests.Response) -> None:
        assert response.status_code == 200, "Response is not 200"
        soup = bs(response.text, features="html.parser")
        metas = soup.find_all("meta")
        title = soup.find("title")
        h1 = soup.find_all("h1")
        h2 = soup.find_all("h2")
        if title:
            self.meta_tags.append(MetaTag(name="title", content=title.text))

        if h1:
            self.meta_tags.extend([MetaTag(name="h1", content=h.text) for h in h1])
        if h2:
            self.meta_tags.extend([MetaTag(name="h2", content=h.text) for h in h2])

        self.meta_tags.extend(
            [
                MetaTag(
                    name=meta.attrs.get("name", ""),
                    content=meta.attrs.get("content", ""),
                )
                for meta in metas
                if "name" in meta.attrs
            ]
        )

        if self._selected_tags:
            self.meta_tags = [
                t for t in self.meta_tags if t.name in self._selected_tags  # type: ignore
            ]

    def to_markdown(self) -> str:
        if not self.status_code == 200:
            return "\n".join(
                [
                    f"# {self._url}",
                    f"Error while fetching response. Status code: {self.status_code}",
                ]
            )
        output = [
            f"# {self._url}\n",
        ]
        for tag in self.meta_tags:
            output.append(tag.to_markdown())
        return "\n".join(output)
