CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "role_id" integer,
  "username" varchar,
  "email" varchar,
  "password" varchar,
  "created_at" timestamp
);
COMMENT ON TABLE "users" IS 'Таблица пользователей. Хранит информацию о всех зарегистрированных пользователях.';
COMMENT ON COLUMN "users"."id" IS 'Идентификатор пользователя';
COMMENT ON COLUMN "users"."role_id" IS 'Роль пользователя (ссылается на таблицу roles)';
COMMENT ON COLUMN "users"."username" IS 'Имя пользователя';
COMMENT ON COLUMN "users"."email" IS 'Электронная почта пользователя';
COMMENT ON COLUMN "users"."password" IS 'Зашифрованный пароль пользователя';
COMMENT ON COLUMN "users"."created_at" IS 'Дата и время регистрации пользователя';

CREATE TABLE "roles" (
  "id" integer PRIMARY KEY,
  "name" varchar
);
COMMENT ON TABLE "roles" IS 'Таблица ролей. Хранит все возможные роли пользователей.';
COMMENT ON COLUMN "roles"."id" IS 'Идентификатор роли';
COMMENT ON COLUMN "roles"."name" IS 'Название роли';

CREATE TABLE "tasks" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "title" varchar,
  "description" text,
  "status" varchar,
  "created_at" timestamp
);
COMMENT ON TABLE "tasks" IS 'Таблица задач. Хранит информацию о задачах, созданных пользователями.';
COMMENT ON COLUMN "tasks"."id" IS 'Идентификатор задачи';
COMMENT ON COLUMN "tasks"."user_id" IS 'Идентификатор пользователя, который создал задачу (ссылается на таблицу users)';
COMMENT ON COLUMN "tasks"."title" IS 'Заголовок задачи';
COMMENT ON COLUMN "tasks"."description" IS 'Описание задачи';
COMMENT ON COLUMN "tasks"."status" IS 'Статус задачи (например, "в процессе", "завершена")';
COMMENT ON COLUMN "tasks"."created_at" IS 'Дата и время создания задачи';

CREATE TABLE "follows" (
  "id" serial PRIMARY KEY,
  "following_user_id" integer,
  "followed_user_id" integer,
  "created_at" timestamp
);
COMMENT ON TABLE "follows" IS 'Таблица подписок. Хранит информацию о том, кто на кого подписан.';
COMMENT ON COLUMN "follows"."id" IS 'Идентификатор подписки';
COMMENT ON COLUMN "follows"."following_user_id" IS 'Идентификатор пользователя, который подписывается (ссылается на таблицу users)';
COMMENT ON COLUMN "follows"."followed_user_id" IS 'Идентификатор пользователя, на которого подписались (ссылается на таблицу users)';
COMMENT ON COLUMN "follows"."created_at" IS 'Дата и время создания подписки';

CREATE TABLE "task_comments" (
  "id" serial PRIMARY KEY,
  "task_id" integer,
  "user_id" integer,
  "comment" text,
  "created_at" timestamp
);
COMMENT ON TABLE "task_comments" IS 'Таблица комментариев к задачам. Хранит комментарии пользователей по задачам.';
COMMENT ON COLUMN "task_comments"."id" IS 'Идентификатор комментария';
COMMENT ON COLUMN "task_comments"."task_id" IS 'Идентификатор задачи, к которой оставлен комментарий (ссылается на таблицу tasks)';
COMMENT ON COLUMN "task_comments"."user_id" IS 'Идентификатор пользователя, который оставил комментарий (ссылается на таблицу users)';
COMMENT ON COLUMN "task_comments"."comment" IS 'Текст комментария';
COMMENT ON COLUMN "task_comments"."created_at" IS 'Дата и время создания комментария';

CREATE TABLE "task_tags" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "created_at" timestamp
);
COMMENT ON TABLE "task_tags" IS 'Таблица тегов. Хранит список всех возможных тегов для задач.';
COMMENT ON COLUMN "task_tags"."id" IS 'Идентификатор тега';
COMMENT ON COLUMN "task_tags"."name" IS 'Название тега';
COMMENT ON COLUMN "task_tags"."created_at" IS 'Дата и время создания тега';

CREATE TABLE "task_tags_map" (
  "id" serial PRIMARY KEY,
  "task_id" integer,
  "tag_id" integer
);
COMMENT ON TABLE "task_tags_map" IS 'Таблица связей между задачами и тегами. Определяет, какие теги привязаны к задачам.';
COMMENT ON COLUMN "task_tags_map"."id" IS 'Идентификатор связи';
COMMENT ON COLUMN "task_tags_map"."task_id" IS 'Идентификатор задачи (ссылается на таблицу tasks)';
COMMENT ON COLUMN "task_tags_map"."tag_id" IS 'Идентификатор тега (ссылается на таблицу task_tags)';

ALTER TABLE "users" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id");

ALTER TABLE "tasks" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "follows" ADD FOREIGN KEY ("following_user_id") REFERENCES "users" ("id");

ALTER TABLE "follows" ADD FOREIGN KEY ("followed_user_id") REFERENCES "users" ("id");

ALTER TABLE "task_comments" ADD FOREIGN KEY ("task_id") REFERENCES "tasks" ("id");

ALTER TABLE "task_comments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "task_tags_map" ADD FOREIGN KEY ("task_id") REFERENCES "tasks" ("id");

ALTER TABLE "task_tags_map" ADD FOREIGN KEY ("tag_id") REFERENCES "task_tags" ("id");