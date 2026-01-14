# models.py
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional
import json

@dataclass
class User:
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: str = 'ar'
    is_premium: bool = False
    notify_on_win: bool = False
    created_at: datetime = None
    last_active: datetime = None
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Giveaway:
    giveaway_id: Optional[int]
    chat_id: int
    creator_id: int
    message_id: Optional[int]
    text: str
    conditions: List[Dict] = None
    winner_count: int = 1
    prevent_fraud: bool = False
    auto_draw: Dict = None
    premium_only: bool = False
    status: str = 'active'  # active, finished, cancelled
    created_at: datetime = None
    finished_at: Optional[datetime] = None
    draw_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []
        if self.auto_draw is None:
            self.auto_draw = {}
    
    def to_dict(self):
        data = asdict(self)
        # تحويل التواريخ إلى نص
        for key in ['created_at', 'finished_at', 'draw_at']:
            if data[key]:
                data[key] = data[key].isoformat()
        return data

@dataclass
class Entry:
    entry_id: Optional[int]
    giveaway_id: int
    user_id: int
    is_excluded: bool = False
    verified_at: Optional[datetime] = None
    created_at: datetime = None
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Winner:
    winner_id: Optional[int]
    giveaway_id: int
    user_id: int
    prize_delivered: bool = False
    notified: bool = False
    created_at: datetime = None
    
    def to_dict(self):
        return asdict(self)
