import psycopg2
from datetime import datetime

from pydq import _queue, TIME_FORMAT


class Postgres(_queue):
    DB_NAME = 'pydq'

    def __init__(self, name, db_name=DB_NAME, db_host='localhost', db_user='pydq', db_password=None):
        super().__init__(name)
        self.db_name = db_name
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.init_db(self.db_name, self.db_host, self.db_user, self.db_password)
        conn = psycopg2.connect(dbname=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS "%s" (qid TEXT NOT NULL, ts TEXT NOT NULL, val BYTEA, PRIMARY KEY(qid, ts))' % name)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def init_db(db_name=DB_NAME, db_host='localhost', db_user='pydq', db_password=None):
        conn = psycopg2.connect(dbname='postgres', host=db_host, user=db_user, password=db_password)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pg_database WHERE datname = '%s'" % db_name)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute('CREATE DATABASE ' + db_name)
        conn.commit()
        cursor.close()
        conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        conn = psycopg2.connect(dbname=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
        c = conn.cursor()
        for txn in self.get_log():
            action, qitem = txn
            if action == self.CREATE:
                c.execute('INSERT INTO "{name}" (qid, ts, val) VALUES (%s, %s, %s) ON CONFLICT (qid, ts) DO UPDATE SET val = %s WHERE "{name}".qid = %s AND "{name}".ts = %s'.format(name=self.name),
                          (qitem['qid'], qitem['ts'], qitem['val'], qitem['val'], qitem['qid'], qitem['ts']))
            elif action == self.DELETE:
                c.execute('DELETE FROM "{name}" WHERE "{name}".qid = %s AND "{name}".ts = %s'.format(name=self.name), (qitem['qid'], qitem['ts']))
        c.close()
        conn.commit()
        conn.close()

    def __call__(self, qid=None, start_time=None, end_time=None, limit=0):
        start_time = datetime(1, 1, 1) if start_time is None else start_time
        end_time = datetime.utcnow() if end_time is None else end_time
        stmt = ['SELECT qid, ts, val from "%s" WHERE ts >= \'%s\' AND ts <= \'%s\'' %
                (self.name, start_time.strftime(TIME_FORMAT), end_time.strftime(TIME_FORMAT))]
        conn = psycopg2.connect(dbname=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
        c = conn.cursor()
        if qid is not None:
            stmt.append(' AND qid = \'%s\'' % qid)
        stmt.append(' ORDER BY ts desc')
        if limit > 0:
            stmt.append(' LIMIT %i' % limit)
        c.execute(''.join(stmt))
        results = [{'qid': i[0], 'ts': i[1], 'val': i[2]} for i in c.fetchall()]  # TODO: Page this
        c.close()
        conn.close()
        with self.mutex:
            self.queue.extend(results)
        return self

    @staticmethod
    def list_all(db_name=DB_NAME, db_host='localhost', db_user='pydq', db_password=None):
        Postgres.init_db(db_name, db_host, db_user, db_password)
        conn = psycopg2.connect(dbname=db_name, host=db_host, user=db_user, password=db_password)
        c = conn.cursor()
        c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        return [i[0] for i in c.fetchall()]
