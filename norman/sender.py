# -*- coding: utf-8 -*-

import os
import base64

import requests
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from bs4 import BeautifulSoup


class Mailer():

    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def host_images(self, html):
        # Clean old images
        response = resources_by_tag("email_test")
        count = len(response.get('resources', []))
        if (count > 0):
            delete_resources_by_tag('email_test')

        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find_all('img')
        for img in imgs:
            resp = upload(img['src'], tags="email_test")
            url, options = cloudinary_url(resp['public_id'], format=resp['format'])
            img['src'] = url

        return soup.prettify()

    def send_email(self, html, targets):
        r = requests.post(
            "https://api.mailgun.net/v3/%s/messages" % self.domain,
            auth=("api", self.api_key),
            data={
                "from": "Email Test <test@%s>" % self.domain,
                "to": targets,
                "subject": "Email Test",
                "html": html
            }
        )
