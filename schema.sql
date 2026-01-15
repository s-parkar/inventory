-- Create Products Table
create table products (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  quantity integer default 0,
  price numeric(10, 2) default 0.00,
  created_at timestamp with time zone default timezone('utc'::text, now()),
  supplier_id uuid references auth.users(id) -- Track who added it
);

-- Create Logs Table
create table logs (
  id uuid default gen_random_uuid() primary key,
  action text not null,
  timestamp timestamp with time zone default timezone('utc'::text, now())
);

-- Create User Roles Table
create table user_roles (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) not null,
  role text not null check (role in ('admin', 'supplier', 'user')),
  created_at timestamp with time zone default timezone('utc'::text, now()),
  unique(user_id)
);

-- Enable Row Level Security (RLS)
alter table products enable row level security;
alter table logs enable row level security;
alter table user_roles enable row level security;

-- Policies
create policy "Allow all access for authenticated users" on products
  for all using (auth.role() = 'authenticated');

create policy "Allow all access for authenticated users" on logs
  for all using (auth.role() = 'authenticated');

create policy "Allow read access for authenticated users" on user_roles
  for select using (auth.role() = 'authenticated');
  
create policy "Allow insert access for authenticated users" on user_roles
  for insert with check (auth.role() = 'authenticated');
