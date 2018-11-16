# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
import requests

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/explore/tags/'+i.strip()+'/?__a=1' for i in open('tags/update.txt').readlines()]


#get all image
    def parse(self, response):
        base_url = "https://www.instagram.com/"
        graphql = json.loads(response.text)
        # if next page
        has_next = graphql['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        # all nodes
        edges = graphql['graphql']['hashtag']['edge_hashtag_to_media']['edges']

        for edge in edges:
            id=edge['node']['id']
            shortcode = edge['node']['shortcode']
            comment=edge['node']['edge_media_to_comment']['count']
            media_url=edge['node']['display_url']
            data = {"id":id,
                    "shortcode":shortcode,
                    "comment":comment,
                    "media_url":media_url}


            yield  Request(base_url+ 'p/'+shortcode+"/?__a=1",meta=data,callback=self.parse_post, dont_filter=True)

## get post
    def parse_post(self,response):
        graphql = json.loads(response.text)
        media = graphql['graphql']['shortcode_media']
        display_url = media['display_url']
        response.meta['display_url']=display_url
        data = response.meta
        location = media.get('location', {})

        if location is not None:
            loc_id = location.get('id', 0)

            request= Request("https://www.instagram.com/explore/locations/" + loc_id + "/?__a=1",meta =data,
                                     callback=self.parse_post_location, dont_filter=True)
            yield request
      #  else:
            media['location'] = {}
            yield data
         #   yield self.makePost(media)


        #get location
    def parse_post_location(self,response):
        location = json.loads(response.text)
        location_name = location['graphql']['location']['name']
        locaiton_lat = location['graphql']['location']['lat']
        location_lng = location['graphql']['location']['lng']
        response.meta['locaiton_lat']=location_lng

        print(response.meta)
        media['location'] = location
        return None
     #   yield self.makePost(media)


