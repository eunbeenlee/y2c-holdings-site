import unittest
from io import BytesIO
import zipfile
from email_backup import create_payload, encrypt_payload, decrypt_payload

class Tests(unittest.TestCase):
    def test_encrypt_roundtrip(self):
        password='this is a test passphrase longer than 16'
        src=create_payload(b'CREATE TABLE public.y2c_reports(id uuid);',b'COPY public.y2c_reports FROM stdin;\n\\.\n')
        enc=encrypt_payload(src,password)
        self.assertFalse(b'y2c_reports' in enc)
        self.assertEqual(decrypt_payload(enc,password),src)
        with zipfile.ZipFile(BytesIO(decrypt_payload(enc,password))) as z:
            self.assertIn('public_schema.sql',z.namelist())
    def test_wrong_password_rejected(self):
        enc=encrypt_payload(b'test','abcdefghijklmnop')
        with self.assertRaises(Exception): decrypt_payload(enc,'incorrect-password')

if __name__=='__main__': unittest.main()
