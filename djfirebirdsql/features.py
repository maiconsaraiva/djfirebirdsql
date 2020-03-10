from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.utils import InterfaceError


class DatabaseFeatures(BaseDatabaseFeatures):
    supports_partial_indexes = False
    supports_functions_in_partial_indexes = False
    supports_regex_backreferencing = False
    can_return_columns_from_insert = True
    supports_transactions = True
    can_introspect_small_integer_field = True
    closed_cursor_error_class = InterfaceError
    has_case_insensitive_like = False
    implied_column_null = True
    ignores_table_name_case = True
    truncates_names = True
    bare_select_suffix = " FROM RDB$DATABASE"
    supports_sequence_reset = False
    supports_subqueries_in_group_by = False
    supports_partially_nullable_unique_constraints = False
    supports_mixed_date_datetime_comparisons = False
    can_introspect_autofield = True
    supports_over_clause = True
    has_bulk_insert = False
    can_introspect_duration_field = False
    supports_timezones = False
    has_zoneinfo_database = False
    supports_select_intersection = False
    supports_select_difference = False
    supports_ignore_conflicts = False
    can_create_inline_fk = False
    supports_atomic_references_rename = False
    supports_column_check_constraints = False
    supports_table_check_constraints = False
    can_introspect_check_constraints = False
    max_query_params = 999
    connection_persists_old_columns = True
    supports_index_column_ordering = False
    supports_index_on_text_field = False
    supports_forward_references = False

    def introspected_boolean_field_type(self, field=None, created_separately=False):
        """
        What is the type returned when the backend introspects a BooleanField?
        The optional arguments may be used to give further details of the field to be
        introspected; in particular, they are provided by Django's test suite:
        field -- the field definition
        created_separately -- True if the field was added via a SchemaEditor's AddField,
                              False if the field was created with the model

        Note that return value from this function is compared by tests against actual
        introspection results; it should provide expectations, not run an introspection
        itself.
        """

        return 'SmallIntegerField'
