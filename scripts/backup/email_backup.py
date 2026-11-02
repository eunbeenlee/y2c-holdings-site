#!/usr/bin/env python3
"""Y2C encrypted schema/data email backup. Python 3.12 + cryptography.
Data format: 8-byte magic + 16-byte random salt + 12-byte nonce + AESGCM ciphertext.
No backup output is written to the public git repository.
"""
from __future__ import annotations
import argparse
import datetime as dt
from email.message import EmailMessage
from io import BytesIO
import json
import os
from pathlib import Path
import secrets
import smtplib
import sys
import zipfile
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC = b'Y2CBAK01'
SALT_BYTES = 16
NONCE_BYTES = 12
PBKDF2_ITERS = 600_000
MAX_EMAIL_FILE_BYTES = 14 * 1024 * 1024  # Gmail 25MB includes MIME/base64 overhead


def derive_key(password: str, salt: bytes) -> bytes:
    if len(password) < 16:
        raise ValueError('Backup encryption password must contain at least 16 characters')
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=PBKDF2_ITERS).derive(password.encode('utf-8'))


def create_payload(schema: bytes, data: bytes) -> bytes:
    blob = BytesIO()
    with zipfile.ZipFile(blob, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        z.writestr('public_schema.sql', schema)
        z.writestr('public_data.sql', data)
        z.writestr('manifest.json', json.dumps({
            'project': 'Y2C HOLDINGS',
            'created_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'scope': 'Supabase public schema and data only. No auth.users, passwords or Storage objects.',
            'restore_warning': 'User identities in auth.users need independent recovery/remapping.'
        },ensure_ascii=False,indent=2))
    return blob.getvalue()


def encrypt_payload(data: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(SALT_BYTES)
    nonce = secrets.token_bytes(NONCE_BYTES)
    key = derive_key(password, salt)
    header = MAGIC + salt + nonce
    return header + AESGCM(key).encrypt(nonce, data, header)


def decrypt_payload(data: bytes, password: str) -> bytes:
    hlen = len(MAGIC) + SALT_BYTES + NONCE_BYTES
    if len(data) < hlen + 16 or not data.startswith(MAGIC):
        raise ValueError('Not a Y2C encrypted backup file')
    salt = data[len(MAGIC):len(MAGIC)+SALT_BYTES]
    nonce = data[len(MAGIC)+SALT_BYTES:hlen]
    key = derive_key(password, salt)
    return AESGCM(key).decrypt(nonce, data[hlen:], data[:hlen])


def send_mail(subject: str, body: str, attachment: bytes | None = None, filename: str = ''):
    sender = os.environ['SMTP_USER'].strip()
    recipient = os.environ['BACKUP_TO'].strip()
    host = os.environ.get('SMTP_HOST') or 'smtp.gmail.com'
    port = int(os.environ.get('SMTP_PORT') or '465')
    passwd = os.environ['SMTP_APP_PASSWORD']
    if not sender or not recipient or not passwd:
        raise ValueError('SMTP user/recipient/app password not configured')
    if len(recipient.split(',')) > 3:
        raise ValueError('Only up to 3 recipients supported; comma separated')
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)
    if attachment is not None:
        msg.add_attachment(attachment, maintype='application', subtype='octet-stream', filename=filename)
    with smtplib.SMTP_SSL(host, port, timeout=35) as client:
        client.login(sender, passwd)
        client.send_message(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['send','decrypt','failure-alert'])
    parser.add_argument('--schema', type=Path)
    parser.add_argument('--data', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    if args.command == 'failure-alert':
        send_mail('[Y2C] 자동백업 실패', 'GitHub Actions에서 백업이 실패했습니다. GitHub Actions 실행 내역을 확인해 주세요.\n백업 파일은 첨부되지 않았습니다.\n')
        print('Failure notification sent.')
        return
    password = os.environ.get('BACKUP_PASSWORD','')
    if args.command == 'send':
        if not args.schema or not args.data or not args.output:
            parser.error('send requires --schema, --data, --output')
        schema = args.schema.read_bytes()
        data = args.data.read_bytes()
        if not schema or not data:
            raise RuntimeError('Empty schema or data dump; refusing to email')
        payload = create_payload(schema, data)
        encrypted = encrypt_payload(payload, password)
        if len(encrypted) > MAX_EMAIL_FILE_BYTES:
            raise RuntimeError(f'Encrypted backup {len(encrypted)//1024//1024} MiB exceeds safe email size; use secure remote storage instead.')
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_bytes(encrypted)
        date = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d')
        send_mail(f'[Y2C] DB 암호화 백업 {date}',
                  'Y2C 관리자 데이터베이스(public schema) 암호화 백업입니다.\n\n'
                  '첨부된 .y2cbackup 파일은 BACKUP_PASSWORD가 있어야 복원할 수 있습니다.\n'
                  '백업 비밀번호는 이메일로 보내지 않습니다.\n'
                  '범위: public schema + data. Auth 로그인 계정 및 파일 스토리지는 별도입니다.\n',
                  encrypted, f'Y2C_{date}.y2cbackup')
        print(f'Encrypted email backup sent ({len(encrypted)} bytes); no artifacts stored.')
        return
    if not args.input or not args.output:
        parser.error('decrypt requires --input and --output')
    result = decrypt_payload(args.input.read_bytes(),password)
    with zipfile.ZipFile(BytesIO(result),'r') as z:
        allowed = {'public_schema.sql', 'public_data.sql', 'manifest.json'}
        if not set(z.namelist()).issubset(allowed):
            raise ValueError('Unexpected contents in backup archive')
        if not {'public_schema.sql','public_data.sql','manifest.json'}.issubset(set(z.namelist())):
            raise ValueError('Incomplete backup archive')
        args.output.mkdir(parents=True, exist_ok=True)
        for name in sorted(allowed):
            (args.output / name).write_bytes(z.read(name))
    print(f'Backup decrypted and checked into {args.output}. Do not commit these files to GitHub.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Backup operation failed: {type(e).__name__}: {e}', file=sys.stderr)
        sys.exit(1)
