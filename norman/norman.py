# -*- coding: utf-8 -*-

import os
import base64

import requests
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from bs4 import BeautifulSoup


class Mailer():

    def __init__(self, domain, api_key):
        self.domain = domain
        self.api_key = api_key

    def host_images(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find_all('img')
        for img in imgs:
            resp = upload(img['src'])
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
