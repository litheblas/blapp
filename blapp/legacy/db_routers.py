from django.db import DatabaseError

LEGACY_APP_LABEL = 'legacy'
LEGACY_DATABASE_LABEL = 'legacy'


class LegacyRouter:
    """
    A database router to route all queries from the legacy app to the legacy database.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == LEGACY_APP_LABEL:
            return LEGACY_DATABASE_LABEL
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == LEGACY_APP_LABEL:
            raise DatabaseError('Writing to the legacy database is not allowed.')
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label == LEGACY_APP_LABEL or obj2._meta.app_label == LEGACY_APP_LABEL):
            # Don't allow relations with tables in the legacy database.
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == LEGACY_DATABASE_LABEL or app_label == LEGACY_APP_LABEL:
            # Don't allow migrations to be run on the legacy database.
            return False
        return None
