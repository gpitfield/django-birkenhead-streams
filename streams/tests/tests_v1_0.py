import sys
import os
import datetime
import hashlib
import json
import pickle
import uuid

from django.db import transaction
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from streams.views.v1_0 import StreamViewSet, ViewerViewSet, LikeViewSet, CommentViewSet


class StreamTests(APITestCase):
    fixtures = ['streams/fixtures/v1_0.yaml',]
    version = 'v1.0'

    def setUp(self):
        self.client_2 = APIClient()
        for u in User.objects.all(): # can't be easily set in yaml
            u.set_password('password')
            u.save()

    def test_streams(self):
        # list, get, create, update, delete
        response = self.client.get('/streams')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        response = self.client.get('/streams/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

        response = self.client.post('/streams', {'title': 'test title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put('/streams/1', {'title': 'test title changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/streams/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username='test_handle_2', password='password')
        # this user doesn't own the stream
        response = self.client.put('/streams/1', {'title': 'test title changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/streams/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client_2.login(username='test_handle', password='password')
        response = self.client_2.put('/streams/1', {'title': 'test title changed', 'status': 'live' })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('changed' in response.data['title'])
        self.assertEqual(response.data['status'], 'live')
        response = self.client_2.delete('/streams/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/streams/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # can't schedule w/ someone else's handle
        response = self.client.post('/streams', {'title': 'a new stream', 'status': 'live', 'profile': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/streams', {'title': 'a new stream', 'status': 'live', 'profile': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stream_id = response.data['id']
        response = self.client.post('/streams/%d/profiles'%stream_id, {'profile': 2,})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/streams/%d/profiles'%stream_id, {'profile': 2,})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sum([1 for p in response.data['profiles'] if p['status']=='accepted']), 1)
        self.assertEqual(sum([1 for p in response.data['profiles'] if p['status']=='invited']), 1)
        response = self.client_2.delete('/streams/%d/profiles'%stream_id, {'profile': 2,})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client_2.put('/streams/%d/profiles/2'%stream_id, {'status': 'accepted'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sum([1 for p in response.data['profiles'] if p['status']=='accepted']), 2)
        response = self.client.delete('/streams/%d/profiles/2'%stream_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_profiles(self):
        # anonymous user
        response = self.client.get('/profiles')
        self.assertEqual(len(response.data), 3)
        response = self.client.post('/profiles', {'handle': 'lou_dog', 'role': 'owner'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put('/profiles/1', {'handle': 'lou_dog', 'role': 'owner'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/profiles/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # POST
        self.client.login(username='test_handle_2', password='password')
        response = self.client.post('/profiles', {'handle': 'lou_dog', 'role': 'owner'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client_2.login(username='test_handle', password='password')
        with transaction.atomic():
            response = self.client_2.post('/profiles', {'handle': 'lou_dog', 'role': 'owner'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
        # PUT
        response = self.client.put('/profiles/2', {'role': 'member', 'user': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with transaction.atomic():
            response = self.client_2.put('/profiles/2', {'role': 'member', 'user': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client_2.put('/profiles/2', {'role': 'member', 'user': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put('/profiles/2', {'role': 'member', 'user': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE
        response = self.client.delete('/profiles/2', {'user': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/profiles/2', {'user': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client_2.delete('/profiles/2', {'user': 1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_viewers(self):
        self.client.login(username='test_handle_2', password='password')
        response = self.client.post('/streams/%d/viewers'%1, {'timestamp': 10.2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/streams/%d/viewers'%1, {'timestamp': 10.2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_2.login(username='test_handle', password='password')
        response = self.client_2.put('/streams/%d/viewers/%d'%(1, response.data['id']), {'timestamp': 10.2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put('/streams/%d/viewers/%d'%(1, response.data['id']), {'timestamp': 10.2, 'status': 'subscribed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'subscribed')

    def test_likes(self):
        self.client.login(username='test_handle_2', password='password')
        response = self.client.post('/streams/%d/likes'%1, {'timestamp': 10.2, 'type': 'like'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_comments(self):
        self.client.login(username='test_handle_2', password='password')
        response = self.client.post('/streams/%d/comments'%1, {'timestamp': 10.2, })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post('/streams/%d/comments'%1, {'timestamp': 10.2, 'text_value': 'nice stream'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_users(self):
        response = self.client.post('/users', {'username': 'testerino', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/users', {'username': 'testerino', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/users', {'username': 'testerino', 'password': 'password2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put('/users/%s'%('testerino'), {'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
