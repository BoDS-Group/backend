PGDMP  %                    }            sc-test    17.2    17.2 %               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            !           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            "           1262    16440    sc-test    DATABASE     |   CREATE DATABASE "sc-test" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_World.1252';
    DROP DATABASE "sc-test";
                     postgres    false            �            1259    16482 
   categories    TABLE     �   CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    parent integer,
    properties jsonb
);
    DROP TABLE public.categories;
       public         heap r       postgres    false            �            1259    16481    categories_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.categories_id_seq;
       public               postgres    false    218            #           0    0    categories_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;
          public               postgres    false    217            �            1259    16512    orders    TABLE     �  CREATE TABLE public.orders (
    id integer NOT NULL,
    line_items jsonb,
    name character varying(255),
    email character varying(255),
    city character varying(255),
    postal_code character varying(20),
    street_address character varying(255),
    country character varying(255),
    paid boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.orders;
       public         heap r       postgres    false            �            1259    16511    orders_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.orders_id_seq;
       public               postgres    false    222            $           0    0    orders_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;
          public               postgres    false    221            �            1259    16529 	   passwords    TABLE     f   CREATE TABLE public.passwords (
    id uuid NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.passwords;
       public         heap r       postgres    false            �            1259    16496    products    TABLE     b  CREATE TABLE public.products (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    images text[],
    category integer,
    properties jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    16495    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public               postgres    false    220            %           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public               postgres    false    219            �            1259    16546    roles    TABLE     ]   CREATE TABLE public.roles (
    id uuid NOT NULL,
    role character varying(50) NOT NULL
);
    DROP TABLE public.roles;
       public         heap r       postgres    false            �            1259    16539    store_users    TABLE     �   CREATE TABLE public.store_users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(127) NOT NULL,
    picture character varying(255),
    address character varying(255)
);
    DROP TABLE public.store_users;
       public         heap r       postgres    false            m           2604    16485    categories id    DEFAULT     n   ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);
 <   ALTER TABLE public.categories ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    217    218    218            q           2604    16515 	   orders id    DEFAULT     f   ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);
 8   ALTER TABLE public.orders ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    221    222    222            n           2604    16499    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    219    220    220                      0    16482 
   categories 
   TABLE DATA           B   COPY public.categories (id, name, parent, properties) FROM stdin;
    public               postgres    false    218   W*                 0    16512    orders 
   TABLE DATA           �   COPY public.orders (id, line_items, name, email, city, postal_code, street_address, country, paid, created_at, updated_at) FROM stdin;
    public               postgres    false    222   �*                 0    16529 	   passwords 
   TABLE DATA           1   COPY public.passwords (id, password) FROM stdin;
    public               postgres    false    223   +                 0    16496    products 
   TABLE DATA           w   COPY public.products (id, title, description, price, images, category, properties, created_at, updated_at) FROM stdin;
    public               postgres    false    220   �+                 0    16546    roles 
   TABLE DATA           )   COPY public.roles (id, role) FROM stdin;
    public               postgres    false    225   �,                 0    16539    store_users 
   TABLE DATA           H   COPY public.store_users (id, email, name, picture, address) FROM stdin;
    public               postgres    false    224   N-       &           0    0    categories_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.categories_id_seq', 8, true);
          public               postgres    false    217            '           0    0    orders_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.orders_id_seq', 1, false);
          public               postgres    false    221            (           0    0    products_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.products_id_seq', 5, true);
          public               postgres    false    219            u           2606    16489    categories categories_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
       public                 postgres    false    218            y           2606    16521    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    222            {           2606    16533    passwords passwords_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.passwords
    ADD CONSTRAINT passwords_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.passwords DROP CONSTRAINT passwords_pkey;
       public                 postgres    false    223            w           2606    16505    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    220                       2606    16550    roles roles_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public                 postgres    false    225            }           2606    16545    store_users store_users_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.store_users
    ADD CONSTRAINT store_users_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.store_users DROP CONSTRAINT store_users_pkey;
       public                 postgres    false    224            �           2606    16490 !   categories categories_parent_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_fkey FOREIGN KEY (parent) REFERENCES public.categories(id);
 K   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_parent_fkey;
       public               postgres    false    218    218    4725            �           2606    16506    products products_category_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_fkey FOREIGN KEY (category) REFERENCES public.categories(id);
 I   ALTER TABLE ONLY public.products DROP CONSTRAINT products_category_fkey;
       public               postgres    false    220    4725    218            �           2606    16551    roles roles_id_fkey    FK CONSTRAINT     s   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_id_fkey FOREIGN KEY (id) REFERENCES public.store_users(id);
 =   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_id_fkey;
       public               postgres    false    4733    224    225               �   x�3�t��/�H-���V*άJU�R�V
V�QP�> "B�X ����_R[�e����X���_ԛ6��˂3 1���hd0�H�Ɛ���^��y� #�3�J�,��������H���qqq ��-�            x������ � �         �   x�͹!@�x��Ѕ��	��/����O�"T���jr����2̥���sh���;�'>B��$��n��FVY��[�̣I���W��u�]v��7,��݌K�jIl]U�J�H��?��d��rjQ�m��X���3��+A5j           x�}��j�0���S,�6��+][(�@C�c/��[�2�spM޽�cJ҆�vg��c"�Wu;@�)������V�F��"E�P��3�h|�e	Al (lc�|=/�`�Po)߲8�4�qH�$L9{����ѰWm�������tf��u��W�l��W�0�9Cw�Z����C6�@�dB�P.�$�����;�J{g���ѡ�=L���c��.h�Ww}m[�� B��>��0�ѕ�e��zF���M����2Y,�D�l� Ky��̿.~'�o(�~�         u   x�U�91 �����G�DZ

@J$�$������M3��^��A�t��$�B���<_��e������ ��y�ɮʓ�hl���^h8!�ppREîu6<��9���&         �   x�u��J�@�u�}�I撙�B�EjK��X,��̟Lk.�L%�o��N8��9��T�1"�a$++Iu@Pd��
�[85���h	��]�踽&f�+A%e��d��Ĉk�Psǔ͹�������$�ԑ�"`������r9���dx�����~��|�l���|�]�6^$u��^Fl���m�BZ<Ժ�+�^���s��s���[M;��������\l���y���Y�'?E���1���#�a#     