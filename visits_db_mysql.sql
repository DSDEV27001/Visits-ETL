CREATE TABLE `facts` (
  `fact_id` int PRIMARY KEY AUTO_INCREMENT,
  `currency_id` int,
  `procedure_id` int,
  `hospital_id_surrogate` int,
  `owner_id_surrogate` int,
  `address_id` int,
  `pet_id_surrogate` int,
  `species_id` int,
  `breed_id` int,
  `averages_counts_and_totals` decimal,
  `kpis_and_other_derived_figures` decimal
);

CREATE TABLE `visits` (
  `visit_id_surrogate` int PRIMARY KEY AUTO_INCREMENT,
  `visit_id` int,
  `visit_start_date` date,
  `visit_end_date` date,
  `visit_cost` float
);

CREATE TABLE `currencies` (
  `currency_id` int PRIMARY KEY AUTO_INCREMENT,
  `currency_symbol` varchar(255)
);

CREATE TABLE `procedures` (
  `procedure_id` int PRIMARY KEY AUTO_INCREMENT,
  `procedure_code` varchar(255),
  `procedure_desc` text
);

CREATE TABLE `hospitals` (
  `hospital_id_surrogate` int PRIMARY KEY AUTO_INCREMENT,
  `hospital_id` int,
  `hospital_name` varchar(255)
);

CREATE TABLE `owners` (
  `owner_id_surrogate` int PRIMARY KEY AUTO_INCREMENT,
  `owner_id` int,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `email` varchar(255)
);

CREATE TABLE `addresses` (
  `address_id` int PRIMARY KEY AUTO_INCREMENT,
  `postcode` varchar(255),
  `address` text,
  `city` varchar(255)
);

CREATE TABLE `pets` (
  `pet_id_surrogate` int PRIMARY KEY AUTO_INCREMENT,
  `pet_id` int,
  `pet_name` varchar(255),
  `pet_dob` date
);

CREATE TABLE `species` (
  `species_id` int PRIMARY KEY AUTO_INCREMENT,
  `species` varchar(255)
);

CREATE TABLE `breeds` (
  `breed_id` int PRIMARY KEY AUTO_INCREMENT,
  `breed` varchar(255)
);

ALTER TABLE `facts` ADD FOREIGN KEY (`fact_id`) REFERENCES `visits` (`visit_id_surrogate`);

ALTER TABLE `facts` ADD FOREIGN KEY (`procedure_id`) REFERENCES `procedures` (`procedure_id`);

ALTER TABLE `facts` ADD FOREIGN KEY (`currency_id`) REFERENCES `currencies` (`currency_id`);

ALTER TABLE `facts` ADD FOREIGN KEY (`hospital_id_surrogate`) REFERENCES `hospitals` (`hospital_id_surrogate`);

ALTER TABLE `facts` ADD FOREIGN KEY (`owner_id_surrogate`) REFERENCES `owners` (`owner_id_surrogate`);

ALTER TABLE `facts` ADD FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`);

ALTER TABLE `facts` ADD FOREIGN KEY (`pet_id_surrogate`) REFERENCES `pets` (`pet_id_surrogate`);

ALTER TABLE `facts` ADD FOREIGN KEY (`species_id`) REFERENCES `species` (`species_id`);

ALTER TABLE `facts` ADD FOREIGN KEY (`breed_id`) REFERENCES `breeds` (`breed_id`);
