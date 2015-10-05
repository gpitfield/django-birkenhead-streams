=====
Django Birkenhead Streams
=====

Django Birkenhead Streams is the streams model for the Birkenhead live streaming
project. It handles stream metadata and management including chores that need
to be done (e.g. monitoring a stream in progress)

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "streams" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'streams',
    )

2. Run `python manage.py migrate` to create the diagnostics models.

3. Configure settings::

    STREAM_SETTINGS = {
        'PLAYLIST_BASE_URL' = 'http://52.1.188.156/hls',
        'PUBLISH_BASE_URL' = 'rtmp://52.1.188.156/src',
        'ARCHIVE_STREAMS' = True,
    }