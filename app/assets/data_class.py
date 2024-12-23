from dataclasses import dataclass


@dataclass
class UserInfo:
    id: int
    name: str
    birthday: str
    luna_birthday: str
    address: str
    phone: str


@dataclass
class Revenue:
    id: int
    uid: int
    uname: str
    time: str
    is_empty: bool
    gift_id: int
    gift_name: str
    gift_img: str
    gift_num: int
    hamster: int
    gold: int
    silver: int
    ios_hamster: int
    normal_hamster: int
    ios_gold: int
    normal_gold: int
    is_hybrid: bool
    is_open_platfrom: int
    open_platfrom_rate: float
    receive_title: str
    room_id: int
