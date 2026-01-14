# database.py
import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection_pool = None
        self.init_pool()
        self.create_tables()
    
    def init_pool(self):
        """تهيئة مجمع الاتصالات"""
        try:
            DATABASE_URL = os.getenv('DATABASE_URL')
            if not DATABASE_URL:
                logger.warning("⚠️ DATABASE_URL غير محدد، باستخدام SQLite للتنمية")
                return self.init_sqlite()
            
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20, DATABASE_URL, sslmode='require'
            )
            logger.info("✅ تم الاتصال بقاعدة البيانات PostgreSQL")
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
            self.connection_pool = None
    
    def init_sqlite(self):
        """تهيئة SQLite للتنمية"""
        import sqlite3
        self.db_path = "giveaway.db"
        logger.info(f"✅ استخدام SQLite للتنمية: {self.db_path}")
        return True
    
    def get_connection(self):
        """الحصول على اتصال قاعدة البيانات"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        else:
            # استخدام SQLite
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
    
    def return_connection(self, conn):
        """إرجاع الاتصال إلى المجمع"""
        if self.connection_pool:
            self.connection_pool.putconn(conn)
        else:
            conn.close()
    
    def create_tables(self):
        """إنشاء الجداول الأساسية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    language_code VARCHAR(10) DEFAULT 'ar',
                    is_premium BOOLEAN DEFAULT FALSE,
                    notify_on_win BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول القنوات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id BIGINT PRIMARY KEY,
                    title VARCHAR(255),
                    username VARCHAR(255),
                    type VARCHAR(50),
                    creator_id BIGINT,
                    is_log_channel BOOLEAN DEFAULT FALSE,
                    log_notifications_chat_id BIGINT,
                    bot_added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (creator_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول السحوبات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS giveaways (
                    giveaway_id SERIAL PRIMARY KEY,
                    chat_id BIGINT,
                    creator_id BIGINT,
                    message_id BIGINT,
                    text TEXT,
                    conditions JSONB DEFAULT '[]',
                    winner_count INTEGER DEFAULT 1,
                    prevent_fraud BOOLEAN DEFAULT FALSE,
                    auto_draw JSONB DEFAULT '{}',
                    premium_only BOOLEAN DEFAULT FALSE,
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP,
                    draw_at TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                    FOREIGN KEY (creator_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول المشاركات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    entry_id SERIAL PRIMARY KEY,
                    giveaway_id INTEGER,
                    user_id BIGINT,
                    is_excluded BOOLEAN DEFAULT FALSE,
                    verified_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(giveaway_id, user_id),
                    FOREIGN KEY (giveaway_id) REFERENCES giveaways(giveaway_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول الفائزين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS winners (
                    winner_id SERIAL PRIMARY KEY,
                    giveaway_id INTEGER,
                    user_id BIGINT,
                    prize_delivered BOOLEAN DEFAULT FALSE,
                    notified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (giveaway_id) REFERENCES giveaways(giveaway_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول النجوم
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stars_purchases (
                    purchase_id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    giveaway_id INTEGER,
                    amount INTEGER,
                    feature VARCHAR(100),
                    transaction_id VARCHAR(255) UNIQUE,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (giveaway_id) REFERENCES giveaways(giveaway_id)
                )
            ''')
            
            # جدول سجل التدقيق
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    log_id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    action VARCHAR(100),
                    details JSONB,
                    ip_address VARCHAR(100),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            conn.commit()
            logger.info("✅ تم إنشاء جميع الجداول")
            
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء الجداول: {e}")
            conn.rollback()
        finally:
            self.return_connection(conn)
    
    # ========== دوال المستخدمين ==========
    
    def add_or_update_user(self, user_data):
        """إضافة أو تحديث مستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users 
                (user_id, username, first_name, last_name, language_code, last_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                language_code = EXCLUDED.language_code,
                last_active = EXCLUDED.last_active
            ''', (
                user_data['id'],
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name'),
                user_data.get('language_code', 'ar'),
                datetime.now()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في إضافة المستخدم: {e}")
            conn.rollback()
            return False
        finally:
            self.return_connection(conn)
    
    def get_user(self, user_id):
        """الحصول على بيانات مستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"❌ خطأ في جلب المستخدم: {e}")
            return None
        finally:
            self.return_connection(conn)
    
    def update_user_notify(self, user_id, notify):
        """تحديث إشعارات الفوز"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'UPDATE users SET notify_on_win = %s WHERE user_id = %s',
                (notify, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في تحديث الإشعارات: {e}")
            conn.rollback()
            return False
        finally:
            self.return_connection(conn)
    
    # ========== دوال السحوبات ==========
    
    def create_giveaway(self, giveaway_data):
        """إنشاء سحب جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO giveaways 
                (chat_id, creator_id, text, conditions, winner_count, 
                 prevent_fraud, auto_draw, premium_only, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING giveaway_id
            ''', (
                giveaway_data['chat_id'],
                giveaway_data['creator_id'],
                giveaway_data['text'],
                json.dumps(giveaway_data.get('conditions', [])),
                giveaway_data['winner_count'],
                giveaway_data.get('prevent_fraud', False),
                json.dumps(giveaway_data.get('auto_draw', {})),
                giveaway_data.get('premium_only', False),
                'active'
            ))
            
            giveaway_id = cursor.fetchone()[0]
            conn.commit()
            return giveaway_id
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء السحب: {e}")
            conn.rollback()
            return None
        finally:
            self.return_connection(conn)
    
    def add_giveaway_entry(self, giveaway_id, user_id):
        """إضافة مشاركة في سحب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO entries (giveaway_id, user_id, verified_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (giveaway_id, user_id) DO NOTHING
            ''', (giveaway_id, user_id, datetime.now()))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"❌ خطأ في إضافة المشاركة: {e}")
            conn.rollback()
            return False
        finally:
            self.return_connection(conn)
    
    # ========== دوال الإحصائيات ==========
    
    def get_user_stats(self, user_id):
        """الحصول على إحصائيات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # عدد السحوبات المنشأة
            cursor.execute('''
                SELECT COUNT(*) as created_count 
                FROM giveaways 
                WHERE creator_id = %s
            ''', (user_id,))
            created = cursor.fetchone()['created_count']
            
            # عدد المشاركات
            cursor.execute('''
                SELECT COUNT(*) as entries_count 
                FROM entries 
                WHERE user_id = %s
            ''', (user_id,))
            entries = cursor.fetchone()['entries_count']
            
            # عدد الفوز
            cursor.execute('''
                SELECT COUNT(*) as wins_count 
                FROM winners 
                WHERE user_id = %s
            ''', (user_id,))
            wins = cursor.fetchone()['wins_count']
            
            return {
                'giveaways_created': created,
                'entries_count': entries,
                'wins_count': wins,
                'user_since': self.get_user(user_id)['created_at'] if self.get_user(user_id) else None
            }
        except Exception as e:
            logger.error(f"❌ خطأ في جلب الإحصائيات: {e}")
            return None
        finally:
            self.return_connection(conn)
    
    def close(self):
        """إغلاق مجمع الاتصالات"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("✅ تم إغلاق اتصالات قاعدة البيانات")

# إنشاء نسخة عامة
db = Database()
