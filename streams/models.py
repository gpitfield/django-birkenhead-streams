import string
import random
import md5
from django.db import models
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings

STREAM_SETTINGS = getattr(settings, 'STREAM_SETTINGS' , {})
PLAYLIST_BASE_URL = STREAM_SETTINGS.get('PLAYLIST_BASE_URL', 'http://52.1.188.156/hls')
PUBLISH_BASE_URL = STREAM_SETTINGS.get('PUBLISH_BASE_URL', 'rtmp://52.1.188.156/src')
BASE_ICON_URL = STREAM_SETTINGS.get('BASE_ICON_URL', 'http://tbd.com/')
ARCHIVE_STREAMS = STREAM_SETTINGS.get('ARCHIVE_STREAMS', True)


class Stream(models.Model):
	#TODO which metadata lives here vs livestream
	timestamp = models.DateTimeField(db_index=True)
	publish_key = models.CharField(max_length=32, unique=True, db_index=True, blank=True)
	subscription_key = models.CharField(max_length=32, unique=True, db_index=True, blank=True)
	archive = models.BooleanField(default=ARCHIVE_STREAMS)
	title = models.TextField(null=True, blank=True)
	status = models.CharField(max_length=12, choices=(
		('live', 'live'), ('ended', 'ended'),
		('paused', 'paused'), ('preload', 'preload'),
		('scheduled', 'scheduled'),
	), default='scheduled', db_index=True)
	duration = models.FloatField(default=0.0)

	def save(self, *args, **kwargs):
		if not self.timestamp:
			self.timestamp = timezone.now()
		if not self.publish_key:
			self.publish_key = md5.new(''.join([random.choice(string.letters) for i in range(20)])).hexdigest()
			self.subscription_key = md5.new(self.publish_key + 'subscription_key').hexdigest()
		super(Stream, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		# clear cache
		super(Stream, self).delete(*args, **kwargs)


	@staticmethod
	def subsription_url(subscription_key):
		return '%s/%s'%(PLAYLIST_BASE_URL, subscription_key)

	@staticmethod
	def publish_url(publish_key):
		return '%s/%s'%(PUBLISH_BASE_URL, publish_key)

	@staticmethod
	def update_for_id(id, values_dict):
		Stream.objects.filter(id=id).update(**values_dict)
		# clear cache

	@staticmethod
	def json_for_id(id):
		# TODO: pull from the cache
		try:
			stream_json = Stream.objects.filter(id=id).values()[0]
			# stream_json['publish_root'] = Stream.publish_url(stream_json['publish_key'])
			# stream_json['subscription_root'] = Stream.subsription_url(stream_json['subscription_key'])
			# stream_json['subscription_root'] = Stream.subsription_url(stream_json['publish_key']) # TODO: delete this line & user actual subscription url
			stream_json['publish_root'] = PUBLISH_BASE_URL
			stream_json['publish_url'] = Stream.publish_url(stream_json['publish_key'])
			stream_json['subscription_root'] = PLAYLIST_BASE_URL
			stream_json['subscription_key'] = stream_json['publish_key'] + '.m3u8'
			stream_json['subscription_url'] = PLAYLIST_BASE_URL + '/' + stream_json['publish_key'] + '.m3u8'
			# for k in ['publish_key', 'subscription_key', 'chat_key']:
			# 	del stream_json[k]
		except IndexError:
			return None
		return stream_json
