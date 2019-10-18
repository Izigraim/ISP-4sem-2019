from shop.models import Comment


class DBRouter(object):

    def db_for_read(self, model, **hints):

        if model == Comment:
            return 'comments'
        return None

    def db_for_write(self, model, **hints):

        if model == Comment:
            return 'comments'
        return None


