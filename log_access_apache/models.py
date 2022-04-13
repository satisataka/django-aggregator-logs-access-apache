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




class LastPositionInFileModel(models.Model):
    date = models.DateTimeField(
        _('Data logging'),
        null=False,
        blank=False,
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
        blank=False,
    )
    last_position = models.PositiveBigIntegerField(
        _('Last position'),
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.path_file


    def get_last_position_in_file(self, file):
        """
        check a read new file or no
        if yes: read from the start,
        else: compare last_line in db and last line file in last position
            if last_line matched: read next lines
            else: we consider that the file was cleared and read from the beginning
        """
        if not self.last_line or not self.last_position:
            return 0

        # calculate start last line
        start_last_line = self.last_position - len(self.last_line)
        file.seek(start_last_line)
        last_line_in_file = file.readline()
        if last_line_in_file:
            # the string written to the database does not match the string in the file
            # means the file is new
            if last_line_in_file != self.last_line:
                return 0
        else:
            return 0

        return self.last_position

    class Meta:
        ordering = ['date']
        verbose_name = "File"
        verbose_name_plural = "Files"
