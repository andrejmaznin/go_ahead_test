from sqlalchemy import Table


def postgresql_settings(table: Table):
    def wrapper(schema_cls):
        setattr(schema_cls, 'psql_table', table)
        return schema_cls

    return wrapper
