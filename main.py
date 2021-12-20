# *-* coding-utf-8 *-*

"""

импорт необходимых модулей

"""
from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty

import logging



from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



import requests

from enum import Enum

from dataclasses import dataclass

class Song(ABC):


    def __init__(self):

        self.engine_system = self._engine_type()

        self.brake_system = self._brake_type()

    @property

    @abstractmethod

    def _engine_type(self):

        raise NotImplementedError()

    @property

    @abstractmethod

    def _brake_type(self):

        raise NotImplementedError()

class EngineSystem(ABC):

    pass

class BrakeSystem(ABC):

    pass


class FooBrakeSystem(BrakeSystem):

    pass

class FooEngineSystem(EngineSystem):

    pass

class FooSong(Song):

    _engine_type = FooEngineSystem

    _brake_type = FooBrakeSystem

if __name__ == '__main__':

    obj = FooSong()

"""

создание enum-класса в базовыми командами

"""

class BaseCommandsEnum(Enum):

    help_command = "help"
    search_command = "search"
    charts_command = "charts"
    top_command = "top"
    
"""

создание enum-класса с базовыми ответами для команд

"""

class BaseReplycsEnum(Enum):

# ответ для команды help

    help_answer =   "Этот бот умеет искать песню по словам. " \
                    "Для поиска воспользуйтесь командой /%s" % (
        BaseCommandsEnum.search_command.value
    )

# ответ для команды search

    process_search_answer = "Введите строку из песни: "

    process_charts_answer = "Данная функция пока что не работает!"

    top_answer = "ТОП по мнение площадки Spotify:\n MORGENSHTERN \n Kizaru \n Skryptonite"

#создание базового датакласса для работы, который содержит:
#адресс API для поиска песни;
#токен бота


@dataclass 
class Config:

    GENIUS_BASE_URL = "https://genius.com/api/search/multi?per_page=5&q="
    GENIUS_CHARTS_URL = "https://genius.com/#top-songs"
    TOKEN = "5052853195:AAFdtzRUSxEvRd4zEEOSkIjI9F9U6br0Ox0"

"""

инициализация логгирования

"""

def configure_logger():

    logging.basicConfig(level=logging.INFO)

"""

базовая настройка

"""

configure_logger()
bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


""" 

состояния для поиска

"""

class SearchSongState(StatesGroup):

    SEARCH_SONG_STATE = State()

#class SearchChartsState(StatesGroup):

#    SEARCH_CHARTS_STATE = State()


"""

логика поиска песни

"""

class SongSearchApiAbstract(ABC):

    __doc__ = """

        Абстрактный класс для поиска песен по фразе
        Показывает, каким является общий интерфейс 

    """

    def __init__(self) -> None: 
        pass 

    """

получение названия песни

    """

    @abstractmethod
    def search_title(self, phrase: str) -> str: 
        pass 
    def charts_title(self, phrase: str) -> str:
        pass
    """

получение исполнителя/исполнителей песни

    """

    @abstractmethod
    def search_artist(self, phrase: str) -> str: 
        pass 

    def _search_base(self, phrase: str) -> dict: 

        """ 
            Получает ответ по нужной фразе
            
        """
        pass 

"""

инициализация класса для работы с API 

"""

class SongSearchApi(SongSearchApiAbstract):

    def __init__(self) -> None: 
        pass 

    """

поиск названия песни

    """

    def search_title(self, phrase: str) -> str:
        pass

    def charts_title(self, phrase: str) -> str:
        pass

    """

поиск исполнителя/исполнителей песни

    """

    def search_artist(self, phrase: str) -> str: 
        pass 

"""

основная логика работы

"""

def search_song(search_text):

    # формирование текста для работы с апи

    search_text = search_text.replace(' ', '+')

    # формирование ссылки для работы с апи

    response = requests.get(
        Config.GENIUS_BASE_URL + search_text

    )
    if response.status_code != 200:
        return "Запрос некорректен, повторите попытку!"

    """

    получение ответа от АПИ в формате json

    """

    full_dict: dict = response.json()

    """

    проверка ответа от АПИ:
    если композиций ноль, то - выполнение первого условия
    если композиций больше нуля, то - выполнение второго условия

    """

    if len(
        full_dict.get(
            'response', {}
        ).get('sections', [])[0].get('hits')
    ) == 0:
        return 'Трек не найден, попробуйте по-другому'

    else:
        
        song_title = full_dict['response']['sections'][0]['hits'][0]['result']['full_title'].split('by')[0].split('(')[0]
        song_artist = full_dict['response']['sections'][0]['hits'][0]['result']['artist_names']

        """

    если найдена композиция:
    возрат значений в формате "Название: ......
                               Исполнитель: ......

        """
        return  "Название: %s \n" \
                "Исполнитель: %s" % (song_title, song_artist)
"""
def search_charts(charts_text):

    # формирование текста для работы с апи

    charts_text = charts_text.replace(' ', '+')

    # формирование ссылки для работы с апи

    response = requests.get(
        Config.GENIUS_CHARTS_URL + charts_text

    )
    if response.status_code != 200:
        return "Запрос некорректен, повторите попытку!"
    # обработка исключения - если ответ от АПИ неудачный
"""

"""

команда "помощь"

"""

@dp.message_handler(commands=[BaseCommandsEnum.help_command.value])
async def process_command_start(
    message: types.Message
) -> None:
    await message.reply(
        BaseReplycsEnum.help_answer.value
    )

@dp.message_handler(commands=[BaseCommandsEnum.top_command.value])
async def process_command_start(
    message: types.Message
) -> None:
    await message.reply(
        BaseReplycsEnum.top_answer.value
    )

"""

команда ввода текста

"""

@dp.message_handler(commands=[BaseCommandsEnum.search_command.value])
async def process_command_start(
    message: types.Message
) -> None:

    await message.reply(BaseReplycsEnum.process_search_answer.value)
    await SearchSongState.SEARCH_SONG_STATE.set()

""" CHARTS ENTER TEXT"""
#@dp.message_handler(commands=[BaseCommandsEnum.charts_command.value])
#async def process_command_start(
#    message: types.Message
#) -> None:

#    await message.reply(BaseReplycsEnum.process_charts_answer.value)
#    await SearchChartsState.SEARCH_CHARTS_STATE.set()

"""

сам поиск

"""

@dp.message_handler(state=SearchSongState.SEARCH_SONG_STATE)
async def search(
    message: types.Message, state: FSMContext
) -> None:
    #  result = search_song(message.text)
    await message.reply(search_song(message.text))
    await state.finish()

#@dp.message_handler(state=SearchChartsState.SEARCH_CHARTS_STATE)
#async def search(
#    message: types.Message, state: FSMContext
#) -> None:
#    #  result = search_charts(message.text)
#    await message.reply(search_charts(message.text))
#    await state.finish()



"""

отлов сообщений, которые не подходят критериям выше 

"""

@dp.message_handler()
async def echo(
    message: types.Message
) -> None:
    
    await message.reply('Введите доступную команду')

"""

Запуск лонг-пулла

"""

if __name__ == "__main__":

    executor.start_polling(
        dp, skip_updates=True
    )
