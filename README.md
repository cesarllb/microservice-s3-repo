# Neuroscience data storage and management microservices subsystem.
The neurodata management process starts once the administrator obtains the information of new images to be added, a group to be modified or a group to be deleted. All operations will be recorded in a log file that keeps the history of all changes made.
The administrator is in charge of selecting the specific bucket in which the neurodata should be stored and the name under which he/she wants to store it as a MinIO object. This operation is performed by creating an event in Kafka. This event is handled by a handler module that processes the event, indexes the object's metadata and inserts the neurodata into MinIO.

![Graph1](https://github.com/cesarllb/repo-brainssys/assets/60330558/e55af91c-b4a1-4fe6-b5c9-b51750f05467)


The process of accessing neurodata begins when a researcher has data to search in the repository, also if he/she has to filter any of its metadata. In the case of searching, the researcher must insert the bucket or the name of the image to be searched. On the other hand, for the query of all existing objects in a bucket, the researcher must only specify the specific bucket related to that standard.
Filtering through metadata is performed with ElasticSearch, which contains a previously indexed copy of the metadata of each object. To access and download any neurodata, the system returns a download URL, which has an expiration date set by the administrator.

![graph2](https://github.com/cesarllb/repo-brainssys/assets/60330558/a3ee5290-36e2-4bee-99c1-e3cbd2ed932e)

