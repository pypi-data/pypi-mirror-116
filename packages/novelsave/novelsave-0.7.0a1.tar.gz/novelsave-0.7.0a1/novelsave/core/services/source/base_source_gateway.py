from abc import ABC, abstractmethod
from typing import List, Tuple

from novelsave.core import dtos


class BaseSourceGateway(ABC):

    @abstractmethod
    def source_name(self) -> str:
        """:return current source name"""

    @abstractmethod
    def is_search_capable(self) -> bool:
        """identifies whether the source provides search capability"""

    @abstractmethod
    def is_login_capable(self) -> bool:
        """identifies whether the source provides login capability"""

    @abstractmethod
    def search(self, keyword: str) -> List[dtos.NovelDTO]:
        """search the source library for novels with keyword"""

    @abstractmethod
    def login(self, username: str, password: str):
        """login to the source website, making available services or novels which might otherwise be absent"""

    @abstractmethod
    def novel_by_url(self, url: str) -> Tuple[dtos.NovelDTO, List[dtos.ChapterDTO], List[dtos.MetaDataDTO]]:
        """scrape and parse a novel by its url"""

    @abstractmethod
    def update_chapter_content(self, chapter: dtos.ChapterDTO) -> dtos.ChapterDTO:
        """update a chapter's content by following its url"""
