from glob import iglob
from apachelogs import LogParser, COMBINED
from django.conf import settings


def log_save_db(parse_log_list, last_position_in_file, last_line, last_position):
	LogAccessApacheModel.objects.bulk_create(parse_log_list)
	last_position_in_file.last_line = last_line
	last_position_in_file.last_position =  last_position
	last_position_in_file.save()


def parser_log():
	parser = LogParser(COMBINED)
	path_files = os.path.join(settings.PARSER_LOG_PATH, settings.PARSER_LOG_FILE_MASK)
	files = iglob(path_files)

	for file in files:
		with open(file, "r+", encoding='UTF-8') as f:
			last_position_in_file, _ = LastPositionInFileModel.objects.get_or_create(
				path_file=file,
				defaults={
					'last_line': '',
					'last_position': 0,
				},
			)

			last_position = last_position_in_file.get_last_position_in_file(f)
			f.seek(last_position)
			line = f.readline()
			parse_log_list = []
			num_line = 0

			while line:
				entry = parser.parse(line)
				log = LogAccessApacheModel(
						host = entry.remote_host,
						logname = entry.remote_logname,
						user = entry.remote_user,
						date = entry.request_time,
						request_line = entry.request_line,
						status = entry.final_status,
						bytes = entry.bytes_sent,
						referer = entry.headers_in["Referer"],
						user_agent = entry.headers_in["User-Agent"],
					)
				parse_log_list.append(log)
				num_line += 1

				previous_line = line
				line = f.readline()

				# write to the database if the required amount has been accumulated or if the file has ended
				if num_line == settings.PARSER_LOG_CREATED_SINGLE_QUERY or not line:
					log_save_db(parse_log_list, last_position_in_file, previous_line, f.tell())
					parse_log_list = []
					num_line = 0


if __name__ == '__main__':
	import os
	import sys

	sys.path.append(os.path.split(os.path.dirname(__file__))[0])
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggregator_logs.settings")

	import django
	django.setup()

	from log_access_apache.models import LogAccessApacheModel, LastPositionInFileModel

	parser_log()
else:
	from .models import LogAccessApacheModel, LastPositionInFileModel
