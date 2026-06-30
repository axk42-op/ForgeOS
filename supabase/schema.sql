-- Forge OS Supabase schema
-- Run in Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql

create table if not exists public.forge_users (
    id uuid primary key default gen_random_uuid(),
    username text not null unique,
    password_hash text not null,
    salt text not null,
    created_at timestamptz not null default now()
);

create index if not exists forge_users_username_idx on public.forge_users (username);

comment on table public.forge_users is 'Forge OS accounts (password_hash + salt only; never plain passwords)';

-- Optional: enable RLS if using anon key instead of service role
-- alter table public.forge_users enable row level security;
