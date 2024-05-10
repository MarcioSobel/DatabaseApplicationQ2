CREATE TABLE pokemon (
    pokedex_number INT,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(25) NOT NULL,
    height DECIMAL(10),
    weight DECIMAL(10),
    hp INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL,
    special_attack INT NOT NULL,
    special_defense INT NOT NULL,
    speed INT NOT NULL,
    total INT NOT NULL,
    capture_rate INT NOT NULL,
    is_legendary TINYINT,
    
    PRIMARY KEY (pokedex_number)
);

CREATE TABLE abilities (
    id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    effect INT,
    
    PRIMARY KEY (id)
);

CREATE TABLE types (
    id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    
    PRIMARY KEY (id)
);

CREATE TABLE moves (
	id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(35) NOT NULL,
    effect INT,
    power INT NOT NULL,
    accuracy INT NOT NULL,
    power_points INT NOT NULL,
    type_id INT,
    
    PRIMARY KEY (id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE pokemon_evolves_to_pokemon (
    evolves_from INT,
    evolves_to INT,
    
    FOREIGN KEY (evolves_from) REFERENCES pokemon(pokedex_number),
    FOREIGN KEY (evolves_to) REFERENCES pokemon(pokedex_number)
);

CREATE TABLE pokemon_has_abilities (
    pokemon_id INT,
    ability_id INT,
    
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokedex_number),
    FOREIGN KEY (ability_id) REFERENCES abilities(id)
);

CREATE TABLE pokemon_has_types (
    pokemon_id INT,
    type_id INT,
    
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokedex_number),
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE pokemon_has_moves (
    pokemon_id INT,
    move_id INT,
    
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokedex_number),
    FOREIGN KEY (move_id) REFERENCES moves(id)
);

CREATE TABLE types_impacts_types (
    type_id INT,
    impacts_type_id INT,
    
    FOREIGN KEY (type_id) REFERENCES types(id),
    FOREIGN KEY (impacts_type_id) REFERENCES types(id)
);
