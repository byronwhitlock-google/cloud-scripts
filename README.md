# CLOUD-SCRIPTS

 Byron's collection of usefull scripts
 
 ## gcs-stats.py
 This small script uses stackdriver to get the total size of all buckets across all projects and shows a grand total. 
 Uses the application default credentials strategy, requires `roles/monitoring.viewer` role on every project, and stackdriver monitorning enabled all projects.
