CREATE TABLE product (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE product_configurations (
    id INT PRIMARY KEY,
    product_id INT,
    variant VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE stock (
    id INT PRIMARY KEY,
    product_config_id INT,
    depot_id INT,
    quantity INT,
    FOREIGN KEY (product_config_id) REFERENCES product_configurations(id)
);
INSERT INTO product (id, name) VALUES
(1, 'Shampooing'),
(2, 'Crème visage');

INSERT INTO product_configurations (id, product_id, variant) VALUES
(101, 1, '250ml'),
(102, 1, '500ml'),
(201, 2, '50ml');

INSERT INTO stock (id, product_config_id, depot_id, quantity) VALUES
(1, 101, 1, 20),
(2, 101, 2, 0),
(3, 102, 1, 5),
(4, 201, 1, 0);
SELECT 
    p.name AS Product_name,
    pc.variant,
    s.depot_id,
    s.quantity,
    CASE 
        WHEN s.quantity > 0 THEN 'true'
        ELSE 'false'
    END AS is_available
FROM 
    product p
JOIN 
    product_configurations pc ON p.id = pc.product_id
JOIN 
    stock s ON pc.id = s.product_config_id
WHERE 
    p.name = 'Shampooing' 
    AND pc.variant = '250ml'
    AND s.depot_id = 2;
SELECT 
    p.name AS Product_name,
    pc.variant,
    s.depot_id,
    s.quantity,
    CASE 
        WHEN s.quantity > 0 THEN 'true'
        ELSE 'false'
    END AS is_available
FROM 
    product p
JOIN 
    product_configurations pc ON p.id = pc.product_id
JOIN 
    stock s ON pc.id = s.product_config_id
WHERE 
    p.name = 'Crème visage' 
    AND pc.variant = '50ml'
    AND s.depot_id = 1;

