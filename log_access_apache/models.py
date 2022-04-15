from django.db import models
from django.utils.translation import gettext_lazy as _


class LogAccessApacheModel(models.Model):
    host = models.GenericIPAddressField(
        _('Remote hostname'),
        null=False,
        blank=False,
        db_index=True,
    )
    logname = models.CharField(
        _('Remote logname'),
        max_length= 100,
        null=True,
        blank=True,
    )
    user = models.CharField(
        _('Remote user'),
        max_length= 100,
        null=True,
        blank=True,
    )
    date = models.DateTimeField(
        _('Request time'),
        null=False,
        blank=False,
        db_index=True,
    )
    request_line = models.TextField(
        _('First request line'),
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(
        _('Status'),
        null=True,
        blank=True,
    )
    bytes = models.PositiveIntegerField(
        _('Size response in bytes'),
        null=True,
        blank=True,
    )
    referer = models.TextField(
        _('Referer'),
        null=True,
        blank=True,
    )
    user_agent = models.TextField(
        _('User-Agent'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.host

    class Meta:
        ordering = ['date', 'host']
        verbose_name = "Log Access Apache"
        verbose_name_plural = "Logs Access Apache"


class FileLogModel(models.Model):
    date = models.DateTimeField(
        _('Data logging'),
        auto_now=True,
    )
    path_file = models.TextField(
        _('Path file'),
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )
    last_line = models.TextField(
        _('Last line'),
        null=False,
        blank=True,
        default='',
    )
    last_position = models.PositiveBigIntegerField(
        _('Last position'),
        null=False,
        blank=False,
        default=0,
    )

    def __str__(self):
        return self.path_file

    @classmethod
    def get_filelog_and_check_last_position(cls, file):
        """
        check a read new file or no
        if new: read from the start,
        else: compare last_line in db and last line file in last position
            if last_line matched: read next lines
            else: we consider that the file was cleared and read from the beginning
        """
        file_log, create = FileLogModel.objects.get_or_create(path_file=file.name)

        if not create and (file_log.last_line or file_log.last_position):
            # calculate start last line
            start_last_line = file_log.last_position - len(file_log.last_line)
            file.seek(start_last_line)
            last_line_in_file = file.readline()
            if not last_line_in_file or last_line_in_file != file_log.last_line:
                file_log.last_line=''
                file_log.last_position=0
                file_log.save()
        return file_log


    class Meta:
        ordering = ['date']
        verbose_name = "File Log"
        verbose_name_plural = "File Logs"
