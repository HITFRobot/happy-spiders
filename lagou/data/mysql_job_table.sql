create table job
(
	url varchar(300) not null,
	url_object_id varchar(50) not null
		primary key,
	title varchar(100) not null,
	salary varchar(20) null,
	job_city varchar(10) null,
	work_years varchar(100) null,
	degree_need varchar(30) null,
	job_type varchar(20) null,
	publish_time varchar(20) not null,
	tags varchar(100) null,
	job_advantage varchar(1000) null,
	job_desc longtext not null,
	job_addr varchar(50) null,
	company_url varchar(300) null,
	company_name varchar(100) null,
	crawl_time datetime null
)
;

