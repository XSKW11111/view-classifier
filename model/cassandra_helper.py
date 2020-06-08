from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory


cluster = Cluster(['IP OF Cassandra'], port=9042)
session = cluster.connect('predicted_comment')

print(session.execute("SELECT release_version FROM system.local").one())


def Insert(hashvalue, content, predicted_class, time, table):
    session.execute(
        """
        INSERT INTO """ + table + """ (hash_value, content, predicted_class, time)
        VALUES (%s, %s, %s, %s);
        """,
        (hashvalue, content, predicted_class, time)
    )
    