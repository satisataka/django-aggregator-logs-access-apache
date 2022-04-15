from glob import iglob
from apachelogs import LogParser, COMBINED
from django.conf import settings
from .models import LogAccessApacheModel, FileLogModel


def parser_log():
    parser = LogParser(COMBINED)
    files = iglob(settings.PARSER_LOG_PATH)

    for file in files:
        with open(file, "r+", encoding='UTF-8') as f:
            file_log = FileLogModel.get_filelog_and_check_last_position(f)
            f.seek(file_log.last_position)

            parse_log_list = []
            num_line = 0

            line = f.readline()
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
                last_position = f.tell()
                line = f.readline()

                # write to the database if the required amount has been accumulated or if the file has ended
                if not settings.PARSER_LOG_CREATED_SINGLE_QUERY or not line or num_line == settings.PARSER_LOG_CREATED_SINGLE_QUERY:
                    LogAccessApacheModel.objects.bulk_create(parse_log_list)
                    file_log.last_line = previous_line
                    file_log.last_position = last_position
                    file_log.save()
                    parse_log_list = []
                    num_line = 0
