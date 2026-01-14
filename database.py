# database.py
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.users = {}
        self.giveaways = {}
        logger.info("✅ تم تهيئة قاعدة البيانات")
    
    def add_user(self, user_data):
        """إضافة مستخدم"""
        self.users[user_data['id']] = {
            **user_data,
            'created_at': datetime.now(),
            'notify_on_win': False
        }
        logger.info(f"✅ تم إضافة مستخدم: {user_data['id']}")
        return True

# إنشاء نسخة عامة
db = Database() [])),
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
