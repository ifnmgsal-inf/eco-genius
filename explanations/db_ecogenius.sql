/* This SQL file displays the structure of the system-specific tables in the database.
 * Intended for understanding the database structure of the system.
 */

CREATE TABLE public.lifetable_answer (
    id bigint NOT NULL,
    value text,
    cell_id bigint,
    student_id bigint,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE public.lifetable_attributelifetable (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE public.lifetable_cell (
    id bigint NOT NULL,
    value text,
    line integer NOT NULL,
    column_id bigint,
    table_id bigint,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE public.lifetable_columnlifetable (
    id bigint NOT NULL,
    attribute_id bigint,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE public.lifetable_lifetable (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(2560) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE public.lifetable_user (
    user_ptr_id bigint NOT NULL,
    is_student boolean NOT NULL,
    course character varying(100) NOT NULL,
    period integer NOT NULL
);

