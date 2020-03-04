from google.cloud import storage
from google.cloud import resource_manager
from google.cloud import monitoring_v3
import sys
import time
# gcs-stats.py 
# quick and dirty script to get the total cloud storage usage across all projects
# Requires stackdriver metrics enabled and stackdriver.metrics.viewer permission on all projects
# byronwhitlock@google.com 3-3-2019
#
def get_bucket_size(project_id, bucket):
  metric_type = "storage.googleapis.com/storage/total_bytes"
  filter_ = 'metric.type = "{}" AND resource.labels.bucket_name = "{}"'.format(metric_type,bucket)
  name = monitoring_client.project_path(project_id)
  interval = monitoring_v3.types.TimeInterval()
  now = time.time()
  interval.end_time.seconds = int(now)
  interval.end_time.nanos = int(
      (now - interval.end_time.seconds) * 10**9)
  interval.start_time.seconds = int(now - 1200)
  interval.start_time.nanos = interval.end_time.nanos
  view = monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL
  # Iterate over all results
  results = monitoring_client.list_time_series(name, filter_, interval, view)
  # Select the latest sample
  bucket_bytes = list(results)[0].points[0].value.double_value
  return bucket_bytes


rm_client = resource_manager.Client()
storage_client = storage.Client()
monitoring_client = monitoring_v3.MetricServiceClient()

project_count=0
bucket_count=0
total_size=0
project_size=0

for project in rm_client.list_projects():
	project_count=project_count+1
	try:
		# if more than 500 need to add paging logic
		buckets = storage_client.list_buckets(project=project.project_id, max_results=500) 
		project_size = 0
		for bucket in buckets:
			try:
				bucket_count = bucket_count+1
				project_size = project_size + get_bucket_size(project.project_id,bucket.name)
			except Exception as err:
				print(" error: {0}".format(err) )

		print("{} ({} MiBytes)".format( project.name , round(project_size/1024/1024)))
		total_size=total_size+project_size
		
	except Exception as err:
		print(" error: {0}".format(err) )
print ("==========================================")
print("Total Cloud Storage Usage: {0} MiBytes".format(round(total_size/1024/1024)))

