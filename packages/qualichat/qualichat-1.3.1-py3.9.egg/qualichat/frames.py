"""
MIT License

Copyright (c) 2021 Qualichat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import (
    Any,
    List,
    Dict,
    Callable,
    Optional,
    Union,
    DefaultDict,
    Set
)
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Fix matplotlib backend warning.
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import spacy
from pandas import DataFrame
from pandas.core.generic import NDFrame
from plotly.subplots import make_subplots # type: ignore
from plotly.graph_objects import Scatter # type: ignore
from wordcloud.wordcloud import WordCloud, STOPWORDS # type: ignore
from colorama import Fore

from .chat import Chat
from .models import Message
from .enums import MessageType
from .utils import log, progress_bar, Menu


__all__ = (
    'BaseFrame',
    'KeysFrame',
)


DataFrames = Dict[str, Union[DataFrame, NDFrame]]
WordClouds = Dict[str, WordCloud]


# TODO: Add return type to this function.
# TODO: Add docstring for this function.
# TODO: Perhaps there is a way to completely automate the creation of
# charts, all you need to say is which columns Qualichat should 
# analyze.
def generate_chart(
    *,
    bars: Optional[List[str]] = None,
    lines: Optional[List[str]] = None,
    title: Optional[str] = None
):
    if bars is None:
        bars = []

    if lines is None:
        lines = []

    def decorator(method: Callable[..., DataFrames]) -> Callable[..., None]:
        def generator(self: BaseFrame, *args: Any, **kwargs: Any) -> None:
            specs = [[{'secondary_y': True}]]

            fig = make_subplots(specs=specs) # type: ignore
            dataframes = method(self, *args, **kwargs)

            # buttons: List[Dict[str, Any]] = []

            # for filename, dataframe in dataframes.items():
            #     button: Dict[str, Any] = dict()
            #     button['label'] = filename
            #     button['method'] = 'update'

            #     ranges: List[Any] = [{'title': {'text': 'Sample text'}}]
            #     button['args'] = ranges

            #     buttons.append(button)

            filename, dataframe = list(dataframes.items())[0]
            index = dataframe.index # type: ignore

            if bars is not None:
                for bar in bars:
                    filtered = getattr(dataframe, bar)
                    options = dict(x=index, y=list(filtered), name=bar) # type: ignore
                    fig.add_bar(**options) # type: ignore

            if lines is not None:
                for line in lines:
                    filtered = getattr(dataframe, line)
                    scatter = Scatter(x=index, y=list(filtered), name=line) # type: ignore
                    fig.add_trace(scatter, secondary_y=True) # type: ignore

            # menus: List[Dict[str, Any]] = [{'active': 0, 'showactive': True, 'buttons': buttons}]
            title_text = f'{title} ({filename})'

            fig.update_layout(title_text=title_text) # type: ignore
            fig.update_xaxes(rangeslider_visible=True) # type: ignore
            fig.show() # type: ignore

        # Dummy implementation for the decorated function to inherit
        # the documentation.
        generator.__doc__ = method.__doc__
        generator.__annotations__ = method.__annotations__

        return generator
    return decorator


stopwords: Set[str] = set(STOPWORDS)
stopwords.update([
    'da', 'meu', 'em', 'você', 'de', 'ao', 'os', 'eu', 'Siga-nos'
])


# TODO: Add return type to this function.
# TODO: Add docstring for this function.
def word_cloud():
    def decorator(method: Callable[..., WordClouds]) -> Callable[..., None]:
        def generator(self: BaseFrame, *args: Any, **kwargs: Any) -> None:
            word_clouds = method(self, *args, **kwargs)

            for _, word_cloud in word_clouds.items():
                word_cloud.stopwords = stopwords

                plt.figure()
                plt.axis('off')

                plt.imshow(word_cloud, interpolation='bilinear') # type: ignore
                plt.show()

        # Dummy implementation for the decorated function to inherit
        # the documentation.
        generator.__doc__ = method.__doc__
        generator.__annotations__ = method.__annotations__

        return generator
    return decorator


class BaseFrame:
    """Represents the base of a Qualichat frame.
    Generally, you should use the built-in frames that Qualichat
    offers you. However, you can subclass this class and create your
    own frames.

    .. note::

        To automatically generate charts, you must create a method
        decorated with :meth:`generate_chart` that returns a
        :class:`pandas.DataFrame`.

    Attributes
    ----------
    chats: List[:class:`.Chat`]
        All the chats loaded via :meth:`qualichat.load_chats`.
    """

    __slots__ = ('chats', 'charts')

    fancy_name: str = ''

    def __init__(self, chats: List[Chat]) -> None:
        self.chats: List[Chat] = chats
        self.charts: Dict[str, Callable[..., Any]] = {}

        for attr in dir(self):
            if attr.startswith('_'):
                continue

            obj: Callable[..., Any] = getattr(self, attr)

            if not callable(obj):
                continue

            self.charts[attr] = obj

    def __repr__(self) -> str:
        return '<BaseFrame>'


nlp = spacy.load('pt_core_news_sm') # type: ignore


CYAN  = Fore.CYAN
RESET = Fore.RESET


class KeysFrame(BaseFrame):
    """A frame that adds charts generator related to chat messages.

    .. note::

        This frame is already automatically added to Qualichat.

    Attributes
    ----------
    chats: List[:class:`.Chat`]
        All the chats loaded via :meth:`qualichat.load_chats`.
    """

    __slots__ = ()

    fancy_name = 'Keys'

    def __repr__(self) -> str:
        return '<KeysFrame>'

    @word_cloud()
    def keyword(self) -> WordClouds:
        """Analyzes the keyword and returns a word cloud with the
        desired type (word cloud of verbs, adjectives or nouns).
        """
        word_clouds: WordClouds = {}

        log('info', 'Enter the keyword you want to analyze:')
        keyword = input('» ')

        for chat in self.chats:
            data: List[str] = []
            messages: DefaultDict[str, List[Message]] = defaultdict(list)
            all_messages: List[Message] = []

            for message in chat.messages:
                if message['Type'] is not MessageType.default:
                    continue

                if keyword not in message.content.lower():
                    continue

                all_messages.append(message)
                messages[message.created_at.strftime("%B %Y")].append(message)

            types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

            menu = Menu('Choose your word cloud type:', types)
            pos = menu.run()

            selected_messages = ['All', 'Choose a chat epoch']

            menu = Menu('Which messages should be selected?', selected_messages)
            selected = menu.run()

            if selected == 'All':
                chat_messages = all_messages
            else:
                menu = Menu('Choose a chat epoch:', messages, multi=True)
                selected_messages = menu.run()

                chat_messages: List[Message] = []

                for messages in selected_messages:
                    chat_messages.extend(messages) # type: ignore

            for i, message in enumerate(chat_messages, start=1):
                text = message['Qty_char_text'] # type: ignore
                doc = nlp(text) # type: ignore

                for token in doc: # type: ignore
                    if token.pos_ == pos: # type: ignore
                        data.append(token.text) # type: ignore

                prefix = f'{CYAN}[{chat.filename}]{RESET} Progress'
                progress_bar(i, len(chat_messages), prefix=prefix)

            parent = Path(__file__).resolve().parent
            path = parent / 'fonts' / 'Roboto-Regular.ttf'

            configs = {}
            configs['width'] = 1920
            configs['height'] = 1080
            configs['font_path'] = str(path)
            configs['background_color'] = 'white'
            
            all_words = ' '.join(data)
            word_cloud = WordCloud(**configs).generate(all_words) # type: ignore

            word_clouds[chat.filename] = word_cloud

        return word_clouds

    @word_cloud()
    def messages(self) -> WordClouds:
        """Analyzes the chats and returns a word cloud with the desired
        type (word cloud of verbs, adjectives or nouns).
         """
        word_clouds: WordClouds = {}

        for chat in self.chats:
            data: List[str] = []
            messages: List[Message] = []

            for message in chat.messages:
                if message['Type'] is not MessageType.default:
                    continue

                messages.append(message)

            types = {'Verbs': 'VERB', 'Nouns': 'NOUN', 'Adjectives': 'ADJ'}

            menu = Menu('Choose your word cloud type:', types)
            pos = menu.run()

            for i, message in enumerate(messages, start=1):
                text = message['Qty_char_text']
                doc = nlp(text) # type: ignore

                for token in doc: # type: ignore
                    if token.pos_ == pos: # type: ignore
                        data.append(token.text) # type: ignore

                prefix = f'{CYAN}[{chat.filename}]{RESET} Progress'
                progress_bar(i, len(messages), prefix=prefix)

            parent = Path(__file__).resolve().parent
            path = parent / 'fonts' / 'Roboto-Regular.ttf'

            configs = {}
            configs['width'] = 1920
            configs['height'] = 1080
            configs['font_path'] = str(path)
            configs['background_color'] = 'white'
            
            all_words = ' '.join(data)
            word_cloud = WordCloud(**configs).generate(all_words) # type: ignore

            word_clouds[chat.filename] = word_cloud

        return word_clouds

    @generate_chart(
        bars=[
            'Qty_char_links', 'Qty_char_emails',
            'Qty_char_marks', 'Qty_char_mentions',
            'Qty_char_emoji'
        ],
        lines=['Qty_messages'],
        title='Keys Frame (Laminations)'
    )
    def laminations(self) -> DataFrames:
        """Shows what are the most common lamination aspects in
        messages per month.

        Laminations aspects can be interpreted as:

        - Links/URLs
        - E-mails
        - Mentions
        - Símbolos/Emojis

        And it will be compared with the total messages sent per month.
        """
        dataframes: DataFrames = {}

        columns = [
            'Qty_char_links', 'Qty_char_emails',
            'Qty_char_marks', 'Qty_char_mentions',
            'Qty_char_emoji', 'Qty_messages'
        ]

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                links = 0
                marks = 0
                emojis = 0
                emails = 0
                mentions = 0
                total_messages = 0

                for message in messages:
                    links += len(message['Qty_char_links'])
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    emails += len(message['Qty_char_emails'])
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append(
                    [links, marks, emojis, emails, mentions, total_messages]
                )

            index = list(data.keys())
            dataframe = DataFrame(rows, index=index, columns=columns)
                
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=['Qty_char_links'],
        lines=['Qty_messages'],
        title='Keys Frame (Links)'
    )
    def links(self) -> DataFrames:
        """Shows the amount of links sent in the chat per month and it
        will be compared with the total messages sent.
        """
        dataframes: DataFrames = {}
        columns = ['Qty_char_links', 'Qty_messages']

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                links = 0
                total_messages = 0

                for message in messages:
                    links += len(message['Qty_char_links'])
                    total_messages += 1

                rows.append([links, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=['Qty_char_mentions'],
        lines=['Qty_messages'],
        title='Keys Frame (Mentions)'
    )
    def mentions(self) -> DataFrames:
        """Shows the amount of mentions sent in the chat per month and
        it will be compared with the total messages sent.
        """
        dataframes: DataFrames = {}
        columns = ['Qty_char_mentions', 'Qty_messages']

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                mentions = 0
                total_messages = 0

                for message in messages:
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append([mentions, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=['Qty_char_emails'],
        lines=['Qty_messages'],
        title='Keys Frame (E-mails)'
    )
    def emails(self) -> DataFrames:
        """Shows the amount of e-mails sent in the chat per month and
        it will be compared with the total messages sent.
        """
        dataframes: DataFrames = {}
        columns = ['Qty_char_emails', 'Qty_messages']

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                mentions = 0
                total_messages = 0

                for message in messages:
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append([mentions, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=['Qty_char_marks', 'Qty_char_emoji'],
        lines=['Qty_messages'],
        title='Keys Frame (Textual symbols)'
    )
    def textual_symbols(self) -> DataFrames:
        """Shows the amount of textual symbols sent in the chat per 
        month and it will be compared with the total messages sent.
        """
        dataframes: DataFrames = {}
        columns = ['Qty_char_marks', 'Qty_char_emoji', 'Qty_messages']

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                marks = 0
                emojis = 0
                total_messages = 0

                for message in messages:
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    total_messages += 1

                rows.append([marks, emojis, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=[
            'Qty_char_emails', 'Qty_char_marks',
            'Qty_char_mentions', 'Qty_char_emoji',
        ],
        lines=['Qty_messages'],
        title='Keys Frame (Without links)'
    )
    def without_links(self) -> DataFrames:
        """Shows the amount of lamination elements *except links*
        sent in the chat per month and it will be compared with the
        total messages sent.
        """
        dataframes: DataFrames = {}
        columns = [
            'Qty_char_emails', 'Qty_char_marks',
            'Qty_char_mentions', 'Qty_char_emoji',
            'Qty_messages'
        ]

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                emails = 0
                marks = 0
                emojis = 0
                mentions = 0
                total_messages = 0

                for message in messages:
                    if message['Qty_char_links']:
                        continue

                    emails += len(message['Qty_char_emails'])
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append([emails, marks, emojis, mentions, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=[
            'Qty_char_links', 'Qty_char_emails',
            'Qty_char_marks', 'Qty_char_emoji',
        ],
        lines=['Qty_messages'],
        title='Keys Frame (Without mentions)'
    )
    def without_mentions(self) -> DataFrames:
        """Shows the amount of lamination elements *except mentions*
        sent in the chat per month and it will be compared with the
        total messages sent.
        """
        dataframes: DataFrames = {}
        columns = [
            'Qty_char_links', 'Qty_char_emails',
            'Qty_char_marks', 'Qty_char_emoji',
            'Qty_messages'
        ]

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                links = 0
                emails = 0
                marks = 0
                emojis = 0
                total_messages = 0

                for message in messages:
                    if message['Qty_char_mentions']:
                        continue
                    
                    links += len(message['Qty_char_links'])
                    emails += len(message['Qty_char_emails'])
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    total_messages += 1

                rows.append([links, emails, marks, emojis, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=[
            'Qty_char_links', 'Qty_char_marks',
            'Qty_char_emoji', 'Qty_char_mentions',
        ],
        lines=['Qty_messages'],
        title='Keys Frame (Without e-mails)'
    )
    def without_emails(self) -> DataFrames:
        """Shows the amount of laminations elements *except e-mails*
        sent in the chat per month and it will be compared with the
        total messages sent.
        """
        dataframes: DataFrames = {}
        columns = [
            'Qty_char_links', 'Qty_char_marks',
            'Qty_char_emoji', 'Qty_char_mentions',
            'Qty_messages'
        ]

        for chat in self.chats:
            data: DefaultDict[str, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                data[message.created_at.strftime('%B %Y')].append(message)

            for messages in data.values():
                links = 0
                marks = 0
                emojis = 0
                mentions = 0
                total_messages = 0

                for message in messages:
                    if message['Qty_char_emails']:
                        continue
                    
                    links += len(message['Qty_char_links'])
                    marks += len(message['Qty_char_marks'])
                    emojis += len(message['Qty_char_emoji'])
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append(
                    [links, marks, emojis, mentions, total_messages]
                )

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes

    @generate_chart(
        bars=['Qty_char_links', 'Qty_char_emails', 'Qty_char_mentions',],
        lines=['Qty_messages'],
        title='Keys Frame (Without textual symbols)'
    )
    def without_textual_symbols(self) -> DataFrames:
        """Shows the amount of laminations elements *except textual
        symbols* sent in the chat per month and it will be compared
        with the total messages sent.
        """
        dataframes: DataFrames = {}
        columns = [
            'Qty_char_links', 'Qty_char_emails',
            'Qty_char_mentions', 'Qty_messages'
        ]

        for chat in self.chats:
            data: DefaultDict[datetime, List[Message]] = defaultdict(list)
            rows: List[List[int]] = []

            for message in chat.messages:
                created_at = message.created_at.replace(hour=0, minute=0, second=0)
                data[created_at].append(message)

            for messages in data.values():
                links = 0
                emails = 0
                mentions = 0
                total_messages = 0

                for message in messages:
                    if message['Qty_char_marks'] or message['Qty_char_emoji']:
                        continue
                    
                    links += len(message['Qty_char_links'])
                    emails += len(message['Qty_char_emails'])
                    mentions += len(message['Qty_char_mentions'])
                    total_messages += 1

                rows.append([links, emails, mentions, total_messages])

            index = list(data.keys())

            dataframe = DataFrame(rows, index=index, columns=columns)
            dataframes[chat.filename] = dataframe

        return dataframes
