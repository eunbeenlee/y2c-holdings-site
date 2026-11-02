import unittest
import sys
import pathlib
from unittest.mock import patch, MagicMock
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from supabase_keepalive import check_database, QUERY, send_failure_alert, main

class FakeCursor:
    def __init__(self): self.executed=[]
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def execute(self, query): self.executed.append(query)
    def fetchone(self): return None

class FakeConnection:
    def __init__(self): self.read_only=False; self.cur=FakeCursor()
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def cursor(self): return self.cur

class MonitorTests(unittest.TestCase):
    def test_checks_real_table_without_writes(self):
        conn=FakeConnection()
        def connect(**kwargs):
            self.assertEqual(kwargs['sslmode'],'require')
            self.assertEqual(kwargs['connect_timeout'],18)
            return conn
        check_database('postgresql://user:password@example.net:5432/db', connector=connect)
        self.assertTrue(conn.read_only)
        self.assertEqual(conn.cur.executed,[QUERY])
        self.assertEqual(QUERY,'SELECT id FROM public.y2c_reports LIMIT 1')

    def test_rejects_missing_connection(self):
        with self.assertRaises(ValueError):check_database('')

    def test_failure_alert_without_secrets_only_logs_no_message(self):
        with patch.dict('os.environ',{},clear=True), patch('smtplib.SMTP_SSL') as smtp:
            send_failure_alert()
            smtp.assert_not_called()

    def test_main_returns_failure_safely(self):
        with patch('sys.argv',['monitor.py','check','--attempts','1']), patch.dict('os.environ',{},clear=True):
            self.assertEqual(main(),1)

if __name__=='__main__': unittest.main()
