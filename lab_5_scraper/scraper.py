"""
Crawler implementation.
"""

# pylint: disable=too-many-arguments, too-many-instance-attributes, unused-import, undefined-variable, unused-argument
import pathlib
import json
from exceptions import *
import requests
import shutil
import re
from typing import Pattern, Union
from core_utils.config_dto import ConfigDTO
from core_utils.constants import CRAWLER_CONFIG_PATH, ASSETS_PATH


class Config:
    """
    Class for unpacking and validating configurations.
    """

    def __init__(self, path_to_config: pathlib.Path) -> None:
        """
        Initialize an instance of the Config class.

        Args:
            path_to_config (pathlib.Path): Path to configuration.
        """
        self.path_to_config = path_to_config
        self._validate_config_content()
        self.config = self._extract_config_content()

    def _extract_config_content(self) -> ConfigDTO:
        """
        Get config values.

        Returns:
            ConfigDTO: Config values
        """
        with self.path_to_config.open("r", encoding="UTF-8") as config_file:
            config = json.load(config_file)
            return ConfigDTO(**config)

    def _validate_config_content(self) -> None:
        """
        Ensure configuration parameters are not corrupt.
        """
        config = self._extract_config_content()

        # Seed URL validation
        correct_seed_url_regex = re.compile("https?://(www.)?")
        if not (isinstance(config.seed_urls, list) and all(
                correct_seed_url_regex.match(url) for url in config.seed_urls)):
            raise IncorrectSeedURLError

        # Number of articles validation
        if not (isinstance(config.total_articles, int) and config.total_articles >= 0):
            raise IncorrectNumberOfArticlesError
        if config.total_articles < 1 or config.total_articles > 150:
            raise NumberOfArticlesOutOfRangeError

        # Headers validation
        if not isinstance(config.headers, dict):
            raise IncorrectHeadersError

        # Encoding validation
        if not isinstance(config.encoding, str):
            raise IncorrectEncodingError

        # Timeout validation
        if not (isinstance(config.timeout, int) and 0 < config.timeout < 60):
            raise IncorrectTimeoutError

        # Verify certificate validation
        if not isinstance(config.should_verify_certificate, bool):
            raise IncorrectVerifyError

    def get_seed_urls(self) -> list[str]:
        """
        Retrieve seed urls.

        Returns:
            list[str]: Seed urls
        """
        return self.config.seed_urls

    def get_num_articles(self) -> int:
        """
        Retrieve total number of articles to scrape.

        Returns:
            int: Total number of articles to scrape
        """
        return self.config.total_articles

    def get_headers(self) -> dict[str, str]:
        """
        Retrieve headers to use during requesting.

        Returns:
            dict[str, str]: Headers
        """
        return self.config.headers

    def get_encoding(self) -> str:
        """
        Retrieve encoding to use during parsing.

        Returns:
            str: Encoding
        """
        return self.config.encoding

    def get_timeout(self) -> int:
        """
        Retrieve number of seconds to wait for response.

        Returns:
            int: Number of seconds to wait for response
        """
        return self.config.timeout

    def get_verify_certificate(self) -> bool:
        """
        Retrieve whether to verify certificate.

        Returns:
            bool: Whether to verify certificate or not
        """
        return self.config.should_verify_certificate

    def get_headless_mode(self) -> bool:
        """
        Retrieve whether to use headless mode.

        Returns:
            bool: Whether to use headless mode or not
        """
        return self.config.headless_mode


def make_request(url: str, config: Config) -> requests.models.Response:
    """
    Deliver a response from a request with given configuration.

    Args:
        url (str): Site url
        config (Config): Configuration

    Returns:
        requests.models.Response: A response from a request
    """
    response = requests.get(url=url,
                            headers=config.get_headers(),
                            timeout=config.get_timeout(),
                            verify=config.get_verify_certificate())
    response.encoding = config.get_encoding()
    return response


#
#
# class Crawler:
#     """
#     Crawler implementation.
#     """
#
#     #: Url pattern
#     url_pattern: Union[Pattern, str]
#
#     def __init__(self, config: Config) -> None:
#         """
#         Initialize an instance of the Crawler class.
#
#         Args:
#             config (Config): Configuration
#         """
#
#     def _extract_url(self, article_bs: BeautifulSoup) -> str:
#         """
#         Find and retrieve url from HTML.
#
#         Args:
#             article_bs (bs4.BeautifulSoup): BeautifulSoup instance
#
#         Returns:
#             str: Url from HTML
#         """
#
#     def find_articles(self) -> None:
#         """
#         Find articles.
#         """
#
#     def get_search_urls(self) -> list:
#         """
#         Get seed_urls param.
#
#         Returns:
#             list: seed_urls param
#         """
#
#
# # 10
# # 4, 6, 8, 10
#
#
# class HTMLParser:
#     """
#     HTMLParser implementation.
#     """
#
#     def __init__(self, full_url: str, article_id: int, config: Config) -> None:
#         """
#         Initialize an instance of the HTMLParser class.
#
#         Args:
#             full_url (str): Site url
#             article_id (int): Article id
#             config (Config): Configuration
#         """
#
#     def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
#         """
#         Find text of article.
#
#         Args:
#             article_soup (bs4.BeautifulSoup): BeautifulSoup instance
#         """
#
#     def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> None:
#         """
#         Find meta information of article.
#
#         Args:
#             article_soup (bs4.BeautifulSoup): BeautifulSoup instance
#         """
#
#     def unify_date_format(self, date_str: str) -> datetime.datetime:
#         """
#         Unify date format.
#
#         Args:
#             date_str (str): Date in text format
#
#         Returns:
#             datetime.datetime: Datetime object
#         """
#
#     def parse(self) -> Union[Article, bool, list]:
#         """
#         Parse each article.
#
#         Returns:
#             Union[Article, bool, list]: Article instance
#         """
#
#
def prepare_environment(base_path: Union[pathlib.Path, str]) -> None:
    """
    Create ASSETS_PATH folder if no created and remove existing folder.

    Args:
        base_path (Union[pathlib.Path, str]): Path where articles stores
    """
    if base_path.exists():
        shutil.rmtree(base_path)
    base_path.mkdir(parents=True)


def main() -> None:
    """
    Entrypoint for scrapper module.
    """
    configuration = Config(path_to_config=CRAWLER_CONFIG_PATH)
    prepare_environment(ASSETS_PATH)
    print(configuration.get_num_articles())


if __name__ == "__main__":
    main()
