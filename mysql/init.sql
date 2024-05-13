CREATE TABLE pokemon (
    pokedex_number INT,
    pokemon VARCHAR(20) NOT NULL,
    description TEXT,
    category VARCHAR(25),
    height DECIMAL(10),
    weight DECIMAL(10),
    hp INT,
    attack INT,
    defense INT,
    special_attack INT,
    special_defense INT,
    speed INT,
    total INT,
    capture_rate INT,
    is_legendary TINYINT,
    is_mythical TINYINT,
    
    PRIMARY KEY (pokedex_number)
);

CREATE TABLE abilities (
    id INT AUTO_INCREMENT,
    ability VARCHAR(20) NOT NULL,
    description TEXT,
    effect INT,
    
    PRIMARY KEY (id)
);

CREATE TABLE types (
    id INT AUTO_INCREMENT,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    
    PRIMARY KEY (id)
);

CREATE TABLE moves (
	id INT AUTO_INCREMENT,
    move VARCHAR(50) NOT NULL,
    description TEXT,
    effect INT,
    power INT,
    accuracy INT,
    power_points INT,
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

CREATE TABLE type_effectiveness (
    attacking_type_id INT,
    defending_type_id INT,
    defending_type2_id INT,
    multiplier DECIMAL(3, 2),

    FOREIGN KEY (attacking_type_id) REFERENCES types(id),
    FOREIGN KEY (defending_type_id) REFERENCES types(id),
    FOREIGN KEY (defending_type2_id) REFERENCES types(id)
);
