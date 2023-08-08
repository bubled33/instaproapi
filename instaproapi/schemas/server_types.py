from __future__ import annotations

from enum import Enum


class ActionStatuses(str, Enum):
    waiting = 'WAITING'
    completed = 'COMPLETED'
    failed = 'FAILED'
    pause = 'PAUSE'

    @classmethod
    def get_title(cls, status: ActionStatuses) -> str:
        match status:
            case cls.waiting:
                return 'Выполняется'
            case cls.completed:
                return 'Выполнено'
            case cls.failed:
                return 'Провалено'
            case cls.pause:
                return 'На паузе'
            case _:
                raise ValueError

class UsersTypes(str, Enum):
    foreign = 'FOREIGN'
    massive_followers = 'MASSIVE_FOLLOWS'

    @classmethod
    def get_title(cls, value: UsersTypes):
        match value:
            case UsersTypes.foreign:
                return 'Иностранцы'
            case UsersTypes.massive_followers:
                return 'Массфоловеры'
            case _:
                return 'Не выбрано'

class ActionTypes(str, Enum):
    watch_stories = 'WATCH_STORIES'
    login = 'LOGIN'
    incomplete_analysis = 'INCOMPLETE_ANALYSIS'
    complete_analysis = 'COMPLETE_ANALYSIS'
    unfollowing = 'UNFOLLOWING'

    @classmethod
    def get_title(cls, action_type) -> str:
        match action_type:
            case cls.watch_stories:
                return 'Просмотр историй'
            case cls.incomplete_analysis:
                return 'Неполный анализ'
            case cls.complete_analysis:
                return 'Полный анализ'
            case _:
                raise ValueError


class UsersGetterType(str, Enum):
    users = 'USERS'
    locations = 'LOCATIONS'
    hash_tags = 'HASH_TAGS'
