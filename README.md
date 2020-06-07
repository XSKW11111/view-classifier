# view-classsifier
Tensorflow Text classification with TensorFlow Hub: Movie reviews Deploy on minikube with cassandra DB

## This project require :

* minikube

* Dokcer

## Execute Command 

Before apply the config file, you have to mount the local volume path into minikube :

```
minikube mount PATH_of_ProjectDirectory/model:/minikube_model
```

```
minukube mount PATH_of_ProjectDirectory/CassandraDB/data:/cassandra_data
```

After mounting the volume into minikube, apply config file to create deployment : 

```
kubectl apply -f configs
```

Then we need to find out which ip cassandra container is:

```
kubectl exec -it cassandra-0 -- nodetool status
```



Copy the ip of cassandra container to cassandra_helper.py.



~~~
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory


cluster = Cluster(['IP OF Cassandra'], port=9042)  # paste the ip of cassandra here
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
~~~



Then we can start bash in pod-viewclassifier and move to directory of model to prepare to start:

```
kubectl exec -it pod-viewclassifier -c cntr-viewclassifier -- /bin/bash

cd /home/viewclassifer/minikube_model
```



first we use **flask run** to examine the if there is any error in python program

``` 
export FLASK_APP=app.py 
flask run
```

if flask run without any problem, we are ready to go.

Execute :

```
uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app
```



In your local terminal type : 

```
minikube service svc-nodeport-httpd
```



