-- Drop tables if already exist. This script is run at database startup
drop table if exists people;
drop table if exists places;

-- Assuming non-pk fields can be Null
create table `people` (
  `id` int not null auto_increment,
  `Given_name` varchar(80) default null,
  `Family_name` varchar(80) default null,
  `Date_of_birth` DATE default null,
  `Place_of_birth` varchar(80) default null, -- represents the City of Birth
  primary key (`id`)
);

-- Assuming non-pk fields can be Null
create table `places` (
  `id` int not null auto_increment,
  `City` varchar(80) default null,
  `County` varchar(80) default null,
  `Country` varchar(80) default null,
  primary key (`id`)
);
