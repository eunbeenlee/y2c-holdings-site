#!/usr/bin/env python3
"""Supabase Free low-activity monitor for Y2C.

Queries the actual Y2C report table read-only. This may reduce inactivity
pausing but it is *not* an uptime guarantee. DB credentials are read only
from GitHub Actions secrets; no secrets should appear in the repository.
"""
from __future__ import annotations
import argparse
from email.message import EmailMessage
import os
import smtplib
import sys
import time

QUERY = 'SELECT id FROM public.y2c_reports LIMIT 1'


def check_database(url: str, connector=None) -> None:
    if not url or not url.startswith(('postgresql://','postgres://')):
        raise ValueError('Missing or unsupported DB connection URI')
    if connector is None:
        import psycopg  # available on GitHub runner; not needed for tests
        connector = psycopg.connect
    # SSL and read-only SQL; no INSERT, dummy rows or artificial writes.
    with connector(conninfo=url, sslmode='require', connect_timeout=18) as conn:
        conn.read_only = True
        with conn.cursor() as cur:
            cur.execute(QUERY)
            cur.fetchone()  # an empty report table is still a valid check


def send_failure_alert() -> None:
    sender = os.environ.get('SMTP_USER', '').strip()
    recipient = os.environ.get('BACKUP_TO','').strip()
    app_pw = os.environ.get('SMTP_APP_PASSWORD','')
    if not sender or not recipient or not app_pw:
        print('Alert not sent: SMTP/recipient secrets have not been configured.', file=sys.stderr)
        return
    host = os.environ.get('SMTP_HOST','smtp.gmail.com')
    port = int(os.environ.get('SMTP_PORT','465'))
    run_url = '/'.join([
        os.environ.get('GITHUB_SERVER_URL','https://github.com').rstrip('/'),
        os.environ.get('GITHUB_REPOSITORY','eunbeenlee/y2c-holdings-site'),
        'actions','runs',os.environ.get('GITHUB_RUN_ID','')
    ])
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = '[Y2C] Supabase DB 상태 점검 실패'
    msg.set_content(
        'Y2C의 Supabase 데이터베이스 점검이 실패했습니다.\n\n'
        '로그인 및 시장조사 보고서 저장이 중단되었는지 확인하세요.\n'
        'Supabase Dashboard에서 프로젝트가 Paused라면 직접 Resume project를 실행해야 합니다.\n'
        f'GitHub Actions 실행 기록: {run_url}\n\n'
        '이 메일에는 DB 비밀번호, API 키, 고객 정보가 포함되지 않습니다.\n'
    )
    with smtplib.SMTP_SSL(host, port, timeout=35) as smtp:
        smtp.login(sender, app_pw)
        smtp.send_message(msg)
    print('Sent an alert email to the configured recipient.')


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=('check', 'failure-alert'))
    p.add_argument('--attempts', type=int, default=3)
    args = p.parse_args()
    if args.command == 'failure-alert':
        send_failure_alert()
        return 0
    if not 1 <= args.attempts <= 5:
        p.error('--attempts must be between 1 and 5')
    url = os.environ.get('SUPABASE_DB_URL','')
    # Never print the URI or unredacted database exceptions.
    for attempt in range(1, args.attempts+1):
        try:
            check_database(url)
            print(f'Y2C database read-only check OK (attempt {attempt}).')
            return 0
        except Exception as exc:
            # Error CLASS only. Full database connection errors can contain
            # sensitive hostname/user details, so don't echo exception text.
            print(f'Y2C database check failed ({attempt}/{args.attempts}): {type(exc).__name__}', file=sys.stderr)
            if attempt < args.attempts:
                time.sleep(8 * attempt)
    print('All retries failed; check Supabase Dashboard and GitHub Secrets.',file=sys.stderr)
    return 1

if __name__ == '__main__':
    sys.exit(main())
