create table articles
(
	title varchar(200) not null,
	create_date date null,
	url varchar(300) not null,
	url_object_id varchar(50) not null
		primary key,
	front_image_url varchar(300) null,
	front_image_path varchar(200) null,
	praise_nums int null,
	fav_nums int null,
	comment_nums int null,
	content longtext null,
	tags varchar(200) null
)
;


