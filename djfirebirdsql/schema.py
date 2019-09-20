from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from .cursor import FirebirdCursorWrapper, _quote_value     # NOQA isort:skip


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    sql_rename_table = "Rename table is not allowed"  # Not supported
    sql_delete_table = "DROP TABLE %(table)s"
    sql_create_column = "ALTER TABLE %(table)s ADD %(column)s %(definition)s"
    sql_alter_column_type = "ALTER %(column)s TYPE %(type)s"
    sql_alter_column_default = "ALTER COLUMN %(column)s SET DEFAULT %(default)s"
    sql_alter_column_no_default = "ALTER COLUMN %(column)s DROP DEFAULT"
    sql_delete_column = "ALTER TABLE %(table)s DROP %(column)s"
    sql_rename_column = "ALTER TABLE %(table)s ALTER %(old_column)s TO %(new_column)s"
    sql_create_fk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s FOREIGN KEY (%(column)s) REFERENCES %(to_table)s (%(to_column)s) ON DELETE CASCADE"
    sql_delete_fk = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    sql_pk_to_unique = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s, ADD CONSTRAINT %(name)s UNIQUE (%(column)s)"
    sql_unique_to_pk = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s, ADD CONSTRAINT %(name)s PRIMARY KEY (%(column)s)"
    sql_delete_constraint = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    sql_add_identity = "ALTER TABLE %(table)s ALTER COLUMN %(column)s SET GENERATED BY DEFAULT"
    sql_delete_identity = "ALTER TABLE %(table)s ALTER COLUMN %(column)s DROP IDENTITY"

    def execute(self, query, params=()):
        super().execute(query, params)
        if self.connection.connection:
            self.connection.connection.commit()

    def quote_value(self, value):
        return _quote_value(value)

    def prepare_default(self, value):
        return self.quote_value(value)

    def _get_field_indexes(self, model, field):
        with self.connection.cursor() as cursor:
            indexes = self.connection.introspection._get_field_indexes(cursor, model._meta.db_table, field.column)
        return indexes

    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        if old_type != new_type:
            for r in self.connection.introspection._get_references(model._meta.db_table):
                if r[4] == old_field:
                    self.execute(self.sql_delete_fk % {'name': r[0], 'table': r[1].upper()})

        super()._alter_field(model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params)

    def remove_field(self, model, field):
        for index_name in self._get_field_indexes(model, field):
            sql = self._delete_constraint_sql(self.sql_delete_index, model, index_name)
            self.execute(sql)
        super(DatabaseSchemaEditor, self).remove_field(model, field)

    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        if new_field.get_internal_type() == 'AutoField':
            new_type = 'integer'
        elif new_field.get_internal_type() == 'BigAutoField':
            new_type = 'bigint'
        elif new_field.get_internal_type() == 'SmallAutoField':
            new_type = 'smallint'
        return super()._alter_column_type_sql(model, old_field, new_field, new_type)

    def delete_model(self, model):
        """Delete a model from the database."""
        # delete related foreign key constraints
        for r in self.connection.introspection._get_references(model._meta.db_table):
            self.execute(self.sql_delete_fk % {'name': r[0], 'table': r[1].upper()})
        super().delete_model(model)

    def _create_index_sql(
        self, model, fields, *, name=None, suffix='', using='',
        db_tablespace=None, col_suffixes=(), sql=None, opclasses=(),
        condition=None, concurrently=False,
    ):
        return super()._create_index_sql(
            model, fields, name=name, suffix=suffix, using=using, db_tablespace=None,
            col_suffixes=col_suffixes, sql=sql, opclasses=opclasses, condition=None,
        )

