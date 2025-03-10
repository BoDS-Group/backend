PGDMP                      }            sc-test    17.2    17.2 5    @           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            A           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            B           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            C           1262    16440    sc-test    DATABASE     |   CREATE DATABASE "sc-test" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_World.1252';
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
       public               postgres    false    218            D           0    0    categories_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;
          public               postgres    false    217            �            1259    16573    cities    TABLE     �   CREATE TABLE public.cities (
    id integer NOT NULL,
    city character varying(50) NOT NULL,
    lat character varying(20),
    lng character varying(20)
);
    DROP TABLE public.cities;
       public         heap r       postgres    false            �            1259    16572    cities_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.cities_id_seq;
       public               postgres    false    227            E           0    0    cities_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.cities_id_seq OWNED BY public.cities.id;
          public               postgres    false    226            �            1259    16556    images    TABLE     �   CREATE TABLE public.images (
    image_id uuid NOT NULL,
    file_path character varying(255) NOT NULL,
    file_name text NOT NULL,
    mime_type text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.images;
       public         heap r       postgres    false            �            1259    16512    orders    TABLE     �  CREATE TABLE public.orders (
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
       public               postgres    false    220            F           0    0    orders_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;
          public               postgres    false    219            �            1259    16529 	   passwords    TABLE     f   CREATE TABLE public.passwords (
    id uuid NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.passwords;
       public         heap r       postgres    false            �            1259    16739    products    TABLE     �  CREATE TABLE public.products (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    images text[],
    category integer[],
    properties jsonb,
    store_id uuid,
    barcode character varying,
    carbon_savings character varying(127),
    status boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    16738    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public               postgres    false    230            G           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public               postgres    false    229            �            1259    16546    roles    TABLE     ]   CREATE TABLE public.roles (
    id uuid NOT NULL,
    role character varying(50) NOT NULL
);
    DROP TABLE public.roles;
       public         heap r       postgres    false            �            1259    16539    store_users    TABLE     �   CREATE TABLE public.store_users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(127) NOT NULL,
    picture character varying(255),
    address character varying(255),
    store_id uuid
);
    DROP TABLE public.store_users;
       public         heap r       postgres    false            �            1259    16599    stores    TABLE       CREATE TABLE public.stores (
    id uuid NOT NULL,
    name character varying(127) NOT NULL,
    description text,
    city character varying(50) NOT NULL,
    location character varying(255) NOT NULL,
    image uuid,
    sustainability_achievement text,
    home_delivery boolean
);
    DROP TABLE public.stores;
       public         heap r       postgres    false            �            1259    16564    system_admin    TABLE     �  CREATE TABLE public.system_admin (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    phone_number character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);
     DROP TABLE public.system_admin;
       public         heap r       postgres    false            ~           2604    16485    categories id    DEFAULT     n   ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);
 <   ALTER TABLE public.categories ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    16576 	   cities id    DEFAULT     f   ALTER TABLE ONLY public.cities ALTER COLUMN id SET DEFAULT nextval('public.cities_id_seq'::regclass);
 8   ALTER TABLE public.cities ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    227    227                       2604    16515 	   orders id    DEFAULT     f   ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);
 8   ALTER TABLE public.orders ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    219    220    220            �           2604    16742    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    230    229    230            1          0    16482 
   categories 
   TABLE DATA           B   COPY public.categories (id, name, parent, properties) FROM stdin;
    public               postgres    false    218   �>       :          0    16573    cities 
   TABLE DATA           4   COPY public.cities (id, city, lat, lng) FROM stdin;
    public               postgres    false    227   @       7          0    16556    images 
   TABLE DATA           W   COPY public.images (image_id, file_path, file_name, mime_type, created_at) FROM stdin;
    public               postgres    false    224   �U       3          0    16512    orders 
   TABLE DATA           �   COPY public.orders (id, line_items, name, email, city, postal_code, street_address, country, paid, created_at, updated_at) FROM stdin;
    public               postgres    false    220   JX       4          0    16529 	   passwords 
   TABLE DATA           1   COPY public.passwords (id, password) FROM stdin;
    public               postgres    false    221   gX       =          0    16739    products 
   TABLE DATA           �   COPY public.products (id, title, description, price, images, category, properties, store_id, barcode, carbon_savings, status, created_at, updated_at) FROM stdin;
    public               postgres    false    230   �Y       6          0    16546    roles 
   TABLE DATA           )   COPY public.roles (id, role) FROM stdin;
    public               postgres    false    223   jr       5          0    16539    store_users 
   TABLE DATA           R   COPY public.store_users (id, email, name, picture, address, store_id) FROM stdin;
    public               postgres    false    222   s       ;          0    16599    stores 
   TABLE DATA           y   COPY public.stores (id, name, description, city, location, image, sustainability_achievement, home_delivery) FROM stdin;
    public               postgres    false    228   �t       8          0    16564    system_admin 
   TABLE DATA           s   COPY public.system_admin (id, name, email, password, phone_number, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    225   �v       H           0    0    categories_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.categories_id_seq', 38, true);
          public               postgres    false    217            I           0    0    cities_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.cities_id_seq', 419, true);
          public               postgres    false    226            J           0    0    orders_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.orders_id_seq', 1, false);
          public               postgres    false    219            K           0    0    products_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.products_id_seq', 10, true);
          public               postgres    false    229            �           2606    16489    categories categories_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
       public                 postgres    false    218            �           2606    16578    cities cities_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.cities DROP CONSTRAINT cities_pkey;
       public                 postgres    false    227            �           2606    16563    images images_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (image_id);
 <   ALTER TABLE ONLY public.images DROP CONSTRAINT images_pkey;
       public                 postgres    false    224            �           2606    16521    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    220            �           2606    16533    passwords passwords_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.passwords
    ADD CONSTRAINT passwords_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.passwords DROP CONSTRAINT passwords_pkey;
       public                 postgres    false    221            �           2606    16748    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    230            �           2606    16550    roles roles_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public                 postgres    false    223            �           2606    16545    store_users store_users_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.store_users
    ADD CONSTRAINT store_users_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.store_users DROP CONSTRAINT store_users_pkey;
       public                 postgres    false    222            �           2606    16605    stores stores_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.stores DROP CONSTRAINT stores_pkey;
       public                 postgres    false    228            �           2606    16571    system_admin system_admin_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.system_admin
    ADD CONSTRAINT system_admin_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.system_admin DROP CONSTRAINT system_admin_pkey;
       public                 postgres    false    225            �           2606    16490 !   categories categories_parent_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_fkey FOREIGN KEY (parent) REFERENCES public.categories(id);
 K   ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_parent_fkey;
       public               postgres    false    4745    218    218            �           2606    16749    products products_store_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);
 I   ALTER TABLE ONLY public.products DROP CONSTRAINT products_store_id_fkey;
       public               postgres    false    228    4761    230            �           2606    16551    roles roles_id_fkey    FK CONSTRAINT     s   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_id_fkey FOREIGN KEY (id) REFERENCES public.store_users(id);
 =   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_id_fkey;
       public               postgres    false    222    4751    223            1   |  x�mRMO�0=O�O��U��KXXX"e%.\,gJ,9��S��q���X���<�޼�JK��:uK8�q�G��^��o�\�-u�߆u�.�K�Kdǂ���zOoء�����������I3]�P��yl��!���O��=9�3���s�K���ؼa�v������*���QT���9˓|���FM���NqD��Ɲ�*V����u#u�{���*:��S�S���@I]��7��p��r;�l�6��pk��N��PN˔��	���0]���].�DkEՒ���e�ב��:M��
*ņ��Aǌ~)��e���V$�8)9eE�|Z���M��p8C[x0�-G�XT����F�l�2����$�ec/?f��!_�#      :      x�mZY��H��OQ'�!$�����J�g���l~P#��h A��\aN���.�.6����?�0_n�xxx�������H���e.|�6��6���O���mc�]�öN�P��O�ȿ�e������&��i���X�o}J��*��ùm�ϛ_m�X�M*�����_=��k6u��zy�1﯇�E�*�����M.���ԏȍ�6�6�9l��vw�K49NH�ƕ�Ӹ\ƃl�u�ƹ�y�z��Lpۼq�x;vü,� Wk�0�X�t�a�U8���
��S7.�_~1~�A�j�qiG�3��q���k*>v�����H��m��/���0^ڡ�L�JL�[.���}w������ƍ��c{����[�Í��y/Ǌr�m��\ԓ�\�Rh6�c�~/f�8	�qw[����ΊW�)6&�^F/?�r�m����~�r�r<j�9��Ȋ�x��c�t�i�k�n��0D���.���fF�-󢎍A=^b�)���-W���n�yXqJ��2�Nry�a�Mp�S7�]���7_��s�c�V��*l��S�N������!����yqOU�FI�����&5��/�ǰ~y���y�H�!	2�lI`����Ǘ������26w��ӷ�j�M-GS��xslϓS�>�H����h�Qc�)�[�a�v�Ѣ)�V�H�8e/s�9ť�ob(^���%^���pŸG����ג��̩i�j �O�4p�
�Ý~E��=��6l�Zs�S&d�*�Z~71oz�(��9�e^�ABN�v�9E���'�m�l9�Vӣ��Ų����]�罸ׯ>�u+_���γ]L�����aS����l��<���=�Ѣ�Jz쇈A����(����C� z��iލ�� �c>�:o�������D�XQ���^tF���Zzv�� A��q���}ЬTǟ i��:0'���a��B�#���\)�G0)�["衿���$�`����k;��P<T�T�}+�N�j�{*�	,H�@��<��ǳ���2H $�ʼ�;HL7b9�'�=5�_`�Y+�Ef�����[d4bخv��N�C >hV׾���#�νU�R+� yM(Ũ�H���Qy�C?ߣ=�$�����G�+ٙ>�Q65��t���C�y����5"��o���)���c��O/��������cc��\����Bhn �?������Q����"��aVD�72 �u�6b��ʀ�����/��ˌJͽ�P��<5P>#+��������\r]|>\z��%�&(��j
�^A;��l,Z�_S"���dN%s��4�x�L�k�?~=��J�}P*Є���+�K:'��һM�/ݎh\��+ue��
�<Y+��f������,�X����i��C1�v�q��\�F}�d��^���$�P���?��UC"R"6���4��${$0�a۲Lv����*�h�E4�Y%bd����|�oAꐻO����S��'�"V�`m�y�Q�U����0�i)�U	{�q�h^��=W�+��_'n�̄-� ]z$���Y}[T�NB?RW��<�݂�8v����wAAT<6n�u�gf�y;Ǡ������	�����)��Ft8u]��W�&�8P�7���T�x���a%n�J۟;�#A�ڑ�����0��g��2���
t� SY,h)�D3KJ�[GQ���JpC���=.t�$���g:�H�hz�:Knr��-��z/H�SH\!��-�q�I5�o�c7�w��8��ר^�ʙ��+V\J����G1�Q88���+2S[��jXR�qक़��[����y������|UFQ�AFG�,��p
�@��} jR�#)����匘�<&	*8� ��J#X��T�:<�M;|��,��b%~���A��x:=Lm��&�[�5̗�w࡟���*gp�ō�����F�]:K)ް�$z06�/�zc
6�K��d��kպr����0+9�z*D�u����X��V�(9�ΰ�˾.��H'K�xc����O=�R��E���5l�:��Y�z�!G���Ϛ̶�R|����o�C��UaS�(���v�JѷN.b0��n�1��e��T����e�.!�Q1Z�j�;�0�a��{��ؤ��x��tX��6��#�V�q�O���R��mE�����6c4�	,�V駱 _�������y��tޮx3�,݈�R&�4Ɂ��~���.�*$��>�e�8���A�F�����%;��|�S�����?�!�y	�����vAՁ�x��e�ZN��R��
p���(�k��4��&�( ��"�_*��2��/?�At��N�����^�n�bxn��7,�w�I�����a�i�@��9ZJ���H���~I2М/}F,���]`��P{�q5�k�f��e���t�o�e�ɑ��Y��!�N�'��YH���z���u�.����%�@v4��{x�����w�|P�Կ�Ňe֊R3������8Yd{���D��;\�(�]�q ����>�f��r�v��Ϣ"e��XW2��sJ���]Cv�]c�KKC��S���V�`���++�ny_���6P�����8�KI�zQV���
�N�����x�E �f��'��(u#=W	������Ɉ*U�,��9�Pr���6~�G��N'a�1/1V��MO�K�'r��U��w1~^�-q@Ea`���uO�F��@xr^�L�ńc'�@z?u�<��}@���|���f�#�OeŃ���[�\i�T�Ev*k����<YiS<�����y���3�N�cǼ���XJ��� �~\�H�D1�ct�M�*�<x��8���kJ�UrF�<~���F��1w�)��$u�T| "��V�2!�x�Gw6a�g�Ķƃ�~�VnRf#�ܭ���`��";�8
��v��8�\z��//?v�o�oP�9�"#��yo}s嵭�g�w?��c{'5l�Y+lYvE��ڛ�����]����Ҳ#�Z����:ؑ� I�ЮtE6c�'fCIA(���1�Љ�}#|�5��}��2��V5z���M|Y�
��γV��-h�3=�ṿ�O��,
�Ñ��6�ɲّ�x��'��U(d�DNd�{�`���~�un��3�VϚHA�/�xw��=�v�|M��MvF�,{����!?���(���F{b /$��OaXĖ���馢&��=z���y�L%FȂ�XPV��^�%�����O�2W��3��0�5��T�$r}LڌK��r�d�B�i|k?+[c�{��zU�]����vX�'i,���YpW#o��L���:���)�E��-P�_E�)�����+vOh	��7�g�A~?�&�^%��AC�v�z��vH�A�� ���= ���l=�.�h��]�	�bq�n�6vId��РJ����`Ko���n�,�����<b�3.���60���̼�_�x�d7�Z��p�E�$ �*U"s�Z��-c�$���ϝ�VC�6�0ES�ϝ��Q�jDL���g��m� ��,��SG#༯e�B^�4�EI&]צ-Z	��7��?�0Q"zg�_[4��>��f�+�n�69��A�l`$��'�m�����L2_��5�
d���br})�zU������r���8��U���c�.z�}��` ͽ0���yj���E���:��N�O�;����z�{������0�|-7����7(O�܉6�^_*��4{?fH����s��V����=Vmɔ&��fcb�����󈍀��!]ʃ{qrP�w��h�͠Y6��FP�O/?��v�����a*V�n��� ���$ൟ�'g
��Z"��jߑH<�Aފ:����2i�gy���sb��䒊�v�\������j�,�hw�~3���n�,�]��E5N��9�@f?��E0kW��,
'u��� ��+���Ps��p��4?~�>��ƹj�U+�ܮb�{ *���u�ė�S���Ea&���G�䢪n!	�P�_ߣ������Zp0����ڵq �  �w�@=w\v��C������W��㙒��[����-0TeH���]`�n�L\G_��d�먨�4��ۏ���Op�C ,lkV]Z޼��D�1��t���,��:\x��[�I >�I�+�U����V<z���&�SP��&�e%��	9t�UOwl^�h�1���p�/�{mi� 3j8�\�_���l����[��I3.��r=�ȭ���s� �˯��Z1;�:���a�j�\�֨��໯��̕GĪ ���n����(O�eЧ�*&\��/�0��?��A3�ɲeW~�0C������K	Ͼ��ϕA	�n�I���3�*K�^>@ݞ��Ab6������K�R7����;�ۓ�����'aa�ĩ����?gB��z��â+�kX�h�0�X2
���z؀,�/��߾
N%FV� ��U����a��Cdپ+)��_��(�sQ9zU�*1x��ߦEr�}Kߣ"�Cd���DR���W���~�d��~�R˲��V�K��װ�*��aLR t��r<�L�op4+���>P�V�r{ �}z����s} ���5GJ}G��4�:]���n��"����<X��Q��xKZ����ʉ����2�)�+c$�w�#��S��n�mX g�O
�ʂ�u�����>��$0�w�i��l=#��Q�C�`5�~y�
�e�HA�u	�R�C��ˌu��0�N�S�-F+�WF��2Z���rX�tn�)"�|M8��;߼ē\��*\x:/��Ce�˛V�Qb�h����R����-�E��������6q��˲*�4�$�렜J����FA �{�G��J����A4�aX��7	55�#u���@��z|�#jύ���^��`����WdYd�M +�����1W�6gTPbz��QNi��jKъ�źR9[$b~D��az������y�	U ���s���Z=�ㆩ_cC5�ϕ�7\��ŕ}�ñZ8����Y��d�,/���NUQ��//�]���������a^4h�I;:�0���F���^x�&$���n�
[[�d"D G~Z�s�on������ǯ�s�M�2[����o݃O�����LD��� �"� ���緃.WJ+ί�x}�v畈s	��?��v �}��ME~Z��~���w��T	�o�H�Gtz÷������A/�s���� yA���Nk�W�������ry���z�Z!���p��׆�uE
Y׻�H�H���_c�"�0jd?��WtB�*�h�,���������r�i���@�5�]ߣ�?��?#�~����?�E��@�����������n�����]�[���fg�P���V:X/�sy��U%[�9`7~)s0wC������ �N���p�W�O[uSq#h�3آ֟���ҷ���n6����&�      7   �  x���M��:���S�tH��>�l�;H� ������N ��h���LYB�S����ـ�� g&$�J��0������?g{����ͯ�??^L�����P?�R&:F����`Ub��e�
��L"h3?�;�;xy ������c$�ݒF)CaX_�xu���ߡ�!�,���¼f�M	��jQ�bXS�5�?�;�8�C�d69V���&�	N3�c�X^B�>�;�;�<R:�P!?&F�45���A<�5ʲ2����z�w�����������l�0�ʙ̄�J���AіAf�R�fX	gU��<�;���̉N��$-n���+e��]+0��db��d�o���L/~�pZ�Mh�D�C����XW�]�f��������ά��8yo�H��v�vHQb↌v�ˎ��m�&�`�hP�1s�,e@͑]�Ԭ��W�;�{v99	�t�4D9<�8L�ʄN%�ib�vۆx�]���ь}В#/R-�x��1�ڼ�2�d�߳?]Q��!+s�"����AIjXe-JFW�n�oلg俙�Sxg�I�,�K�n�j[���{C��q�r�2c��,�9�wA[����l���l�߳����1��>X,n�h�6#.�"��X0\��5���l!>��v-��y�/_�      3      x������ � �      4     x���ɭ$0�ӹ0�Y�2̒�C� �J�؄�-�j<����i��']�8i[���v��]�d�V$�x���1Z)I����1��3$�!�QVgĶ [��a���gQ�Q�}�zK���;�Qd��(R�%��,ޛ��J��X�G��(�f�Z��SYb�pK$z�@���`�xYta�A��B�ڊuf�1��ir�s�,ᖍ��`-��n��˝��[e}OI��q��q^O��U����(�����>�7�@������=������Ѩ�
      =      x��[˒�u]�_�b�53r�Px��l��irZDs(��E�*��z`��hC� /��J������O�97� 4�3�#V���7���sofzK�Fe�WoL�U��M�;]i5�wmQ��Z-7��}ؘB�����Ԫ)U��7���S�[cbOe��Q��>�1|~k��I�����&�E�BZ��Ôj��[S�+�ʶ���-����i�QyY;/�(<ə5�K�Z���M�G��ܧ�_��<�`k�ۗ�J�j��X�0b�6jSf�foW���m_��y�te���y����,S1$M�J��UZ�{�i:�}$�*^�c?NB4	��|���&�a22A����8�So0���_zz���$�h���h揦����U����\�80��������~�`�l0|L�AL&���x�I��6�7�Tו��6W�3,V-M�by���۫m�W6�ꝁ*�&�3j����*�1dW���Ku���N���L׵
�9l���h<5Q�etk`_]�"J3�k�N�i���̐fw�RW�8௝l7U�����t�6����7�q���:D\�Z����Y	�������۲j�e���^�O��Q�c����."�����n0F����J׍�n��OU��j�	9iZD��5n#�:]�Y��=��VQft!~J��,����ꍆ IU�j���g��?/�Lm�l��Agύg��έ86����5}V��	W˩"L	��lϨ���Tx��	�AE:��C��Q�)ָ�S�����n��H�!�w��r�Q\5��
��:W�cƌ}-!��m-���\�B�J &�p��oR��d�� I�=�{Ǵ���kC3Tt���E����'&ܦ�@(vZ��[�D�N޾z	����� Z�x]��4�����uM��Y�˨p�6ё������Vɜ���Iw�m3���s�چ�����ۂ8��2 ~�i�X	/��j�biQ�wZ�X��< c�z�����w�P�Zwtw�8G�K�;�V��ۘ�z/RA ylW���W_�I�4��m�F�B"d=���+ �2¶J!8cUB������o���
�4I�¼̷3x2�sҴ.�jlơZ!vb�b>�A
��Z���Tt,��C�K��*�C�Bn� �n,�^ť9��M31`�鋚�sa�� �0c!�ꦁ���h�����i���N^����]��0��i�r�1�#���T�sΪ��(N]�W
Y�W�`u��t8)y�*u���s������[�*���7%���<H�� ��SKmʴ�?�PK ��u��{�bҀ�E8����@�,�r��@,��p����Q8L���W����gs60���ǁ��s$���%���x�s��p�ɰw��������/�jYf��u	���-�$VY1����}��>
��j�.^���}ӽ@�����w6������CY����6�����_�+!z񳬬;��Ht�{\���O�O�SH�O��T��|"��bq����k���fqy�T
I���qj�5Q�tQ���3�x���LAK<2������ 
W-��~���}�W1S7���<�L��n��6�?�k�j�I�IXF}�B���X������>_�* �B����X=���?S� ��A���4*S�ϑ_���{��-�&\X.^C�- N��H���A3v�A���x����F���?���+������g�;m|����A�͎s�Y;i���v�m�lm�!��BG쫟I���Hj�@�Q��I�	�h�w�Z�a�6/�$�r����w�RX獏λ����2dWF�"���l���lgk��[�΀a����rǪ�>-�?x����A�@��,��L_�ؕ�-��
/�٬Z�v��-��2�9�r��������FӅ���
���eF$� �
Ӕ�Z z�y;&�a�Q��
d
S���E�r��A����\�&��ue���U,���y�������H5bV�&]�8����`�������i$�[�"�$��w�5���Xt��������9|UE	3�jL�I��[}u�'jƠ����]OH8�'�c�/J9��l�,F��ŐU*��N ٲ(V,q�5+�����I7�H�l��fP�w#�� %<��Т�?)�\� �=�"��l���[��@��|6�}­`�\��N�u�������ǏO-O����+������X���������O�s���y`�MY�$(�nG�"S5�Q����'��Ҳ��K�e��ąC%Qf�qV"B$,�P�^����qᏂ�㋍U;Y��׾z�XZ#��ð�
��Q	 P �ɹ�㎦���0ଆ����M��'f�c��ï�T��}�:Ճ�8,�@����J��H+��i��R���^�5:t���s]�,�3)Ubd=B��
�f�噄�DJ`(א`�|g :�՟YU�CH�fnڮ ת�KF��Q*�~gX��g���3R1��ۭ�L�T{
�4|zO�c8=�@�Bӏl,�fL�}��5�81���ciY9|�tb�a+B\G��?�8��CvW���E�WY�$�g���ְ�A}�E��~NJH)u2��u�6�]�'Q2��Uu���\�����Ag�N7�P$H7����h�Gubv1z�F��_t���	�	c�CA��߽}z�ϗ/���^\���Mv�ҍ��	�v�D���>E�`ү01��Q6�G� �S��ꐊ���x9
�UyϠt,�㎙�蒷��O�I�\��-�Ѿ��0�	�=�g�A��JHy��8ע�ך0�~����Z �(�0�m���-]SJ�C�}�t;����$-a?t0��p��U��wuf���[I��T�+|k��;�6�߼V�QE��u��Wo��P �\�Se)�qlJ��D̒���FV�&��Z绎p�DdR�]��u�9Jn!U�\ӽ�& �|�e�����n`+[j5;�+�>�f���{cKh
������c����� �4Ւ�K����h�x�ө<�\ڂ���,w>��ϓ��U����c��o�#�3��(D`:SW��3)��D�T��}&��ً_��l�|�4���y,�We[s�}�h��CI�sv|X}��G`�L� ��<���y��p:�������������`��p5WALW�-��/�0���l6<�09��d�[DR"�����9���0S7�z���J� �k#��΀f�@���?�:U_��c��S���(��-V�4��Z��f�4�O{a��U�^��k3� �ޢX��E.��+��PoM��ř|�>���Ҳ�b�xr�oJ�-\ٷ�UW�/��L���%	�K�6$|;�b]�� �m��tRC�z�E�X����&K,��خ��@�cu�����L�yu&�BS�͇�{~K�m�K�ʮ�	i:�ZbUe�����"��G�^�C$���!�}�����`ڟ�{gf:�c�-���=��`5���4�ߗٍ���#�1�9=�}2�-��-�����<��x{~�qz��ž��c(��1��	�
D���y��wi���͕�:���R�YYA��IZٕ8��}
�r��*:���2?��[�Q���xL�FHE�s`�'vB>͹�,#�iYE�cc�b��	�?��߭��`͡��1�M��((���U����X2�W(�P۹�(w�c榚YJ�����Q .��*���'��5�a}Ҥo�!��l!�XI�\��q�N��)Q�{�E�p���;[�`�]Z�poס!��7%� R!\�JL�L�ާ
���//o�}5 ���HT����P=/�	�9q��zS��A����W6�'�ܫ�˶j����a�4�}��4qݛ��� �}���h�f� IV���?���f��������1��h���a8��G���'�޷��w77P� �lu-�j��uU�@t��aO��C���R缷jcކ�\�J(�[��XU�M��*�|��_f�=_})! ���k��k���R��ƃM�����L�Guq(�I���К�d��?�M޺�g�A��P�x]�j\㠶Et�B�����r�քk5�V��,`���j��k�y] �  ����˰�cD7�l��Xo��`OA�T<��#׷�=�Kh�t!���k����,�m��Y4y*�aW�E��'�ˎ&`�I�۸��PReV"��%�0�vFo�6�i9*r*�k�J�CVX��X��� T�ʂn�i��mr=�@;-����r_�����d��&���[�Y���S�-,�/�˄�|,��s���I��禪-\���]%����ʎ]��K�\~�"V���m�9l5��%od��|�/��#M �,�?GV<����/sB��a鸔��ò�i�sG��rv����q�	��J4L.�G�TE�c]�4E�p[�p�Bo}n/X6ƽ	+С�+�#��	����񤂭���k��j�9����JY�-:�Rg����t�[c�!j\���-ٵ�[�a�mʲv�X�:�Uy*M�-e��P��v^}��"K���;{��m����$J�Y��jΓ�`�g��?ꙿ
���x4^ͣ�,�(M��ϧ�0����>������������?/�=������
|��? f�G��`8pav�	�����}̏�z��+9y�	\��j�x�o�ʕ�����@�av�	����d�sL�SU��{E�����ד�Llb�ٴu{��W��%��tki6.��9�#�u�p+?*�C�ԏ��X�$m�+wF��b�_�F�����I�(\�P��*��s��mnIPy��c��m'�<'��L��\�X�U�]��1%ۗu$gljk3�Fy�\��p�����+iX`����d�D�|̝��7� ,�<n)u�&�ó'wn�MN��� KYM��Es|J�As�'<�sg����푇Kw
9nz�uT��(�֦�3>?����
�b��ͺ��{��@�������\�i���،]1nZ�.���ql?�s��wN`�E3*�Dl�,u=`9t���q`tA����Y�� ���S[c�rq��u��2�&q��$�z�CTn��]U~pg$��$�F��R��1�N�m��
��p���l�'.!މ ���\�[wpa#�D׍�WuY��`EY�<i��O���=����(+א�2�Ta%^F�ESi�ւ^��Q�L9�����89��У�j���ٴh��;�x�oI� ^ �JH�V+����:�a����}��Oy�b-;�,7S�[X�\�m�ʳ�,(lZ�vFnJ6}7c�.�Y)�ɶ��:،��0rXMcA�])��2kcπ��Y(?N�V��"�p��8��������J]`��QN-���p��Yw��L�Lޞ:�(����5=��jH�'�l(_;��
SwIjj@+�G��_�Pq��qBe��USۣ��l���;$ј�}[�v�vL�g�:�u�6&�<�jO�?�_.��ouɯE}��&���LGx�Y�k_]�y�8N��=q\���Cģd���Χ�Ȍ#6$�Ɓ%�`8���_�����p2�O'>'w��zQ������+܀����98�͆I��GwYֺ��s9�h��O����{�M�qO����b������%8)��X~�a�-������G�ּJ��������/��U�s{�'됛�s�	릵4�vMQ��%$ �O�ӿH`f������I�a�V�D�|A1�*������B�-+��-%shw*B!���ګ�hTC��3�T�u`�{k�t�^w�e����~��)��t��R���u���ہ��ºJm�y�
)^p��U��
����ԒT����uwd���ȳ1����.�|�^~����T,G��N-g�e|7�Me�h��D�ȼ�{��=�|r��I�c�-��g'���^��O~J���۶ڲ�:-!�H[;$k������>f>�d,��Ll���]]��Tچ%�70�_����غ$jO׀ل�E���O��LGNC>�i=^%�|ī�K�� �A Pz�N�>��ޥ�n6	��@��a0P�,ôl*-ZPV��z`^�u��S7|ey�nq�����������E/��(Q'3���?�Q�Nu⯒x�GA�x8Ifv�)�"`��͇�l�x;���A�;�������������)
�t���|�w0��Z�+�&s�]䲿-��%G�����[�SF۲q����t��Jx��,��yT�;V$-2�L��	�����j�rr�>��6ϻ/W��/����y��8ƣ`6�z:^��������4i�L����S��_�,L<�<���O�'O��7���      6   �   x�U�;J@A�ڷ�+3�L�R��B�$���� �o��H�	R���6�&�J�e����ϗߧ����3l1�8���ʡ6�O��N+�ָ҅ �.����:�����g���'�x�}1�R��o�V�)�dBVn�d�z����7��x]�}3@m      5   e  x�e�K�1�u�)�jlI.K��m!��m9)��:4Bnw�E�W�����j0q��Ar%��)4]������v��q�m?��e��m���^��cz�|?��;r�X�3f0-���-8�L��3���+)%R�D��Z:IMS����~�ˇ�����,�LX�F��
�£��Vr�<�֖�@X����nJ��S����_�<�����G�5���+�:^��I!TdcOI�^����� �����d����i��';oo]�1W��W��8j7�q,���U*^���b�f��J%�$%K!��4�����.O~>۫Wc��Ch:>����R	�K�,�i~>���\`�d      ;   �  x�U��j1��>O1_䱽l�"���
�hl)1�3�̴���sIK�,���B�,=�0� ���D��h�w.��Fc]_�m��=�sY:�J��y}��Z���驪O4M|x亯�Z������h����}f���8jb�h�M���)�����np��	R6|�K@6"� ���8ToǍ���Ph��:5����^扯�-��������[g�sG��f��E2�S�B�N� ����c�S&G[��%��M	���~�8ο�]3A�*�$�r�e��(�v;<m�m�ϕ���j�Nl�����R62盲�b=&��J���8��Gh#q0`�\����kB�8f��?�u�}#����z��ga��K'�S٢�±@|����C�A�s-�>]��	,	�2`��u�����W�L�zW[dw���:O�,祻}�ǵ�]љ��2�5�sKbF	)�hW�v	C2��U�����z����R�D      8   �   x�ȱ
1 й��K�4I{��� :8�4I�D���Wx��n����b%r#����� V���㱭���k[ֶ���may?���c;|l��*�]<�UYԹr�T�KVq��XT��.��@:���c��!!q.�T�#`D���SN�Dv��v�n�0?�p2�     