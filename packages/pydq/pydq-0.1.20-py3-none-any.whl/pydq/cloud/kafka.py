from datetime import datetime, timedelta
from kafka import KafkaConsumer, KafkaProducer, TopicPartition, KafkaAdminClient
from kafka.partitioner.default import murmur2

from pydq import _queue, TIME_FORMAT


def __partitioner__(key, all_partitions, available):
    # partition by date string
    key = key.decode('utf-8').split('T')[0].encode('utf-8')
    idx = murmur2(key)
    idx &= 0x7fffffff
    idx %= len(all_partitions)
    return all_partitions[idx]


class Kafka(_queue):
    def __init__(self, name, bootstrap_servers='localhost:9092', partitioner=__partitioner__, retention_days=30):
        super().__init__(name)
        self.bootstrap_servers = bootstrap_servers
        self.partitioner = partitioner
        self.retention_days = retention_days

    def __exit__(self, exc_type, exc_val, exc_tb):
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, partitioner=self.partitioner)
        for txn in self.get_log():
            action, qitem = txn
            key = qitem['ts'] if isinstance(qitem['ts'], str) else qitem['ts'].strftime(TIME_FORMAT)
            key = key.encode('utf-8')
            if action == self.CREATE:
                value = str(qitem['val']).encode('utf-8')
                producer.send(topic=self.name, value=value, key=key, headers=[('qid', qitem['qid'].encode('utf-8'))])
            elif action == self.DELETE:
                # Set value to None to delete
                producer.send(topic=self.name, value=None, key=key, headers=[('qid', qitem['qid'].encode('utf-8'))])
        producer.flush()

    def __call__(self, qid, start_time, end_time, limit):
        start_time = datetime.utcnow() - timedelta(days=30) if start_time is None else start_time
        start_time = max(start_time, datetime.utcnow() - timedelta(days=self.retention_days))
        end_time = datetime.utcnow() if end_time is None else end_time

        consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers, consumer_timeout_ms=1000)
        dates = [(start_time + timedelta(n)).strftime(TIME_FORMAT).encode('utf-8') for n in range(int((end_time - start_time).days) + 1)]
        partitions = [self.partitioner(d, list(consumer.partitions_for_topic(self.name)), None) for d in dates]
        consumer.assign([TopicPartition(self.name, p) for p in set(partitions)])
        consumer.seek_to_beginning()

        results = []
        skip = []
        try:
            for msg in consumer:
                msg_qid = msg.headers[0][1].decode('utf-8')
                msg_ts = datetime.strptime(msg.key.decode('utf-8'), TIME_FORMAT)
                msg_val = msg.value
                if msg_val is None:
                    skip.append(msg_ts)
                    print('skipping %s' % msg_ts)
                    continue
                else:
                    msg_val = msg_val.decode('utf-8')
                if qid is not None and msg_qid != qid:
                    continue
                if msg_ts < start_time:
                    continue
                if msg_ts > end_time:
                    # all messages after this should be later than end_time
                    break
                results.append({'qid': msg_qid, 'ts': msg_ts, 'val': msg_val})
                if len(results) >= limit:
                    break
        except StopIteration:
            pass
        finally:
            consumer.unsubscribe()
            consumer.close()
        with self.mutex:
            self.queue.extend([r for r in results if r['ts'] not in skip])
        return self

    def delete(self):
        client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        client.delete_topics([self.name])

    @staticmethod
    def list_all(bootstrap_servers='localhost:9092'):
        return list(KafkaConsumer(bootstrap_servers=bootstrap_servers).topics())