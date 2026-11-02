-- Run AFTER creating an email/password user in Supabase Authentication > Users.
-- Replace the example address below with your real admin email. Never put a password here.
insert into public.y2c_admins (user_id, role, active)
select id, 'admin', true from auth.users
where email = 'REPLACE_WITH_ADMIN_EMAIL@example.com'
on conflict (user_id) do update set role='admin', active=true;

-- Check the row was actually added (0 rows means email did not match an Auth user):
select a.user_id, a.role, a.active from public.y2c_admins a
join auth.users u on u.id = a.user_id
where u.email='REPLACE_WITH_ADMIN_EMAIL@example.com';
