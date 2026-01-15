-- 1. Add supplier_id to existing products table (if it doesn't exist)
do $$ 
begin 
    if not exists (select 1 from information_schema.columns where table_name = 'products' and column_name = 'supplier_id') then
        alter table products add column supplier_id uuid references auth.users(id);
    end if; 
end $$;

-- 2. Create User Roles Table (if it doesn't exist)
create table if not exists user_roles (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) not null,
  role text not null check (role in ('admin', 'supplier', 'user')),
  created_at timestamp with time zone default timezone('utc'::text, now()),
  unique(user_id)
);

-- 3. Enable RLS on user_roles
alter table user_roles enable row level security;

-- 4. Create Policies (Drop first to avoid errors if re-running)
drop policy if exists "Allow read access for authenticated users" on user_roles;
create policy "Allow read access for authenticated users" on user_roles
  for select using (auth.role() = 'authenticated');
  
drop policy if exists "Allow insert access for authenticated users" on user_roles;
create policy "Allow insert access for authenticated users" on user_roles
  for insert with check (auth.role() = 'authenticated');
