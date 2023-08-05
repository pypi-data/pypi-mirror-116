import random
from .enums import Enum
from .errors import *
import requests

BASE_URL_SEARCH = "https://g.tenor.com/v1/search"
BASE_URL_TRENDING = "https://g.tenor.com/v1/trending"
BASE_URL_RANDOM =  "https://g.tenor.com/v1/random"
BASE_URL_GIF = "https://g.tenor.com/v1/gifs"
class Tenor:
    """[Tenor api wrapper used to request gif's from the website]
        This was original made to be used with discord.py bot development
        Why? , Cause i felt like it
    """
    def __init__(self):
        self.api = "AC0JT282BT3C"

    
    def __parse_gif_id_request(
        self , 
        response , 
        mediafilter: str
    ):
        response = response.json() 
        if mediafilter == Enum.MediaFilter.GIF: 
            return response.get("results")[0].get("url")
        return response.get("results")[0].get("media")[0].get(mediafilter).get("url")

    def __get_url_from_response(
        self , 
        response , 
        limit: int , 
        mediafilter: str , 
    ): 
        response = response.json()
        if response.get("code"): 
            raise DoesNotExist("Request set of gif(s) does not exist")
        urls = []
        for index in range(limit): 
            url = response.get("results")[index].get("media")[0].get(mediafilter).get("url")
            urls.append(url)
        return urls

    def search_for_gifs(
        self , *,
        query: str ,
        limit: int = 5 , 
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        pos: int = 0 , 
        locale: Enum = Enum.LocaleMedia.EN_US
    ):
        """[Request gif's from the tenor website starting from most popular gif's to least]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = requests.get(
            url = "%s?q=%s&limit=%s&contentfilter=%s&mediafilter=%s&pos=%s&locale=%s&key=%s"
            % 
            (BASE_URL_SEARCH , query , limit , contentfilter , mediafilter , pos , locale , self.api)
        )
        return self.__get_url_from_response(data , limit , mediafilter)

    def trending_gifs(
        self , *,
        limit: int = 5 , 
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ):
        """[Request trending gif's from the tenor website]

        Args:
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = requests.get(
            url = "%s?limit=%s&contentfilter=%s&mediafilter=%s&locale=%s&key=%s"
            % 
            (BASE_URL_TRENDING , limit , contentfilter , mediafilter , locale , self.api)
        )

        return self.__get_url_from_response(data , limit , mediafilter)

    def c_random_gifs(
        self , *,
        query: str ,
        limit: int = 5 , 
        pos: int = 5 ,
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ):
        """[Request random gif's from the tenor website with each call , When i say random i mean random]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """

        return self.random_gifs(
            query=query,
            limit=limit,
            contentfilter=contentfilter,
            mediafilter=mediafilter,
            pos=random.randint(0 , pos),
            locale=locale,
        )


    def random_gifs(
        self , *,
        query: str ,
        limit: int = 5 , 
        pos: int = 0 ,
        contentfilter: Enum = Enum.ContentFilter.OFF , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
        locale: Enum = Enum.LocaleMedia.EN_US
    ):
        """[Request random gif's from the tenor , Would use tenor_gif_search]

        Args:
            query (str): [The tag to be used to find the gif]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            contentfilter (Enum, optional): [The gif format the gif's will be returned in]. Defaults to Enum.ContentFilter.OFF.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.
            pos (int, optional): [The position you want to start collection gif's from]. Defaults to 0.
            locale (Enum, optional): [The default language to interpret search string]. Defaults to Enum.LocaleMedia.EN_US.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = requests.get(
            url = "%s?q=%s&limit=%s&contentfilter=%s&mediafilter=%s&pos=%s&locale=%s&key=%s"
            % 
            (BASE_URL_RANDOM , query , limit , contentfilter , mediafilter , pos , locale , self.api)
        )

        return self.__get_url_from_response(data , limit , mediafilter)

    def gif_by_id(
        self , *,
        id: int ,
        limit: int = 5 , 
        mediafilter: Enum = Enum.MediaFilter.GIF, 
    ):
        """[Request a specific gif from the tenor website]

        Args:
            ids (int): [The gif id]
            limit (int, optional): [The amount of gif's that will be returned from tenor]. Defaults to 5.
            mediafilter (Enum, optional): [The content safety of the gif]. Defaults to Enum.MediaFilter.GIF.

        Returns:
            tuple[str]: [GIF URLS]
        """
        data = requests.get(
            url = "%s?ids=%s&limit=%s&mediafilter=%s&key=%s"
            % 
            (BASE_URL_GIF , id , limit ,  mediafilter , self.api)
        )

        return self. __parse_gif_id_request(data , mediafilter)
