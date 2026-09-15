CREATE TABLE IF NOT EXISTS public.job_categories
(
    category_id integer NOT NULL,
    slug character varying(100) COLLATE pg_catalog."default" NOT NULL,
    category_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    tracked_status boolean DEFAULT false,
    CONSTRAINT job_categories_pkey PRIMARY KEY (category_id),
    CONSTRAINT job_categories_category_name_key UNIQUE (category_name),
    CONSTRAINT job_categories_slug_key UNIQUE (slug)
);

CREATE TABLE IF NOT EXISTS public.job_postings
(
    job_id integer NOT NULL,
    published_at timestamp without time zone NOT NULL,
    last_modified timestamp without time zone NOT NULL,
    expires timestamp without time zone NOT NULL,
    slug text COLLATE pg_catalog."default" NOT NULL,
    job_title text COLLATE pg_catalog."default" NOT NULL,
    category_id smallint NOT NULL,
    contact text COLLATE pg_catalog."default",
    work_location text COLLATE pg_catalog."default",
    work_start text COLLATE pg_catalog."default",
    work_end text COLLATE pg_catalog."default",
    hourly_rate text COLLATE pg_catalog."default" NOT NULL,
    work_hours text COLLATE pg_catalog."default",
    job_description text COLLATE pg_catalog."default",
    applicant_profile text COLLATE pg_catalog."default",
    required_skills text COLLATE pg_catalog."default",
    preferred_skills text COLLATE pg_catalog."default",
    company_name text COLLATE pg_catalog."default",
    CONSTRAINT job_postings_pkey PRIMARY KEY (job_id),
    CONSTRAINT job_postings_slug_key UNIQUE (slug),
    CONSTRAINT fk_category FOREIGN KEY (category_id)
        REFERENCES public.job_categories (category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);