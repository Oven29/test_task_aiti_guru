INSERT INTO
    categories (name, parent_id)
VALUES
    ('Бытовая техника', NULL), -- id 1
    ('Стиральные машины', 1), -- id 2
    ('Холодильники', 1), -- id 3
    ('Однокамерные', 3), -- id 4
    ('Двухкамерные', 3), -- id 5
    ('Телевизоры', 1), -- id 6
    ('Компьютеры', NULL), -- id 7
    ('Ноутбуки', 7), -- id 8
    ('17"', 8), -- id 9
    ('19"', 8), -- id 10
    ('Моноблоки', 7);

INSERT INTO
    users (name, address)
VALUES
    ('Иван Петров', 'ул. Ленина, д. 10, кв. 5'),
    ('Мария Сидорова', 'ул. Гагарина, д. 25, кв. 12'),
    ('Алексей Козлов', 'пр. Мира, д. 100, кв. 45');

INSERT INTO
    products (name, category_id, count, price)
VALUES
    ('Стиральная машина LG F2J5WN4W', 2, 5, 45000),
    ('Стиральная машина Bosch WAW32540OE', 2, 3, 65000),
    ('Холодильник Samsung RB34T670FSA', 5, 2, 55000),
    ('Холодильник Atlant ХМ 4012-022', 4, 8, 25000),
    ('Телевизор Samsung UE55AU7100U', 6, 12, 42000),
    ('Ноутбук ASUS VivoBook 17', 9, 6, 38000),
    ('Ноутбук Honor MagicBook 19', 10, 6, 38000),
    ('Моноблок HP 24-df1032ur', 11, 4, 52000);

INSERT INTO
    orders (user_id, status, amount)
VALUES
    (1, 'pending', 0);