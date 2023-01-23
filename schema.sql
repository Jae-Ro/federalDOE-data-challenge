-- Drop tables if already exist. This script is run at database startup
drop table if exists people;
drop table if exists places;

-- Assuming non-pk fields can be Null
create table `people` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` DATE default null,
  `place_of_birth` varchar(80) default null, -- represents the City of Birth
  primary key (`id`)
);

-- Assuming non-pk fields can be Null
create table `places` (
  `id` int not null auto_increment,
  `city` varchar(80) default null,
  `county` varchar(80) default null,
  `country` varchar(80) default null,
  primary key (`id`)
);
