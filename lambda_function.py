from ics import Calendar
import requests
import boto3
import json

def lambda_handler(event, context):

    url = "https://calendar.google.com/calendar/ical/orhqd94aam77t8d2lnvduttnig%40group.calendar.google.com/public/basic.ics"

    # Get a calendar and extract which events are taking place now()
    c = Calendar(requests.get(url).text)
    events = c.timeline.now()

    # Add a preamble!
    important_data = ['Idag serveras det']

    # Extract names, which in this case is what's being served in the school cafeteria
    for x in events:
        important_data.append(x.name)
        important_data.append('. ') # This is for proper pauses between events

    a_string_to_speak = ''.join(important_data) # Jam the list of strings into a long string for Polly

    polly_client = boto3.client('polly')
    
    # response['SynthesisTask']['CreationTime'] contains ex "2018-10-23 20:21:05.023000+02:00"
    # but that won't fly for Alexa! She wants a T between date and time

    time_as_string = "%s" % response['SynthesisTask']['CreationTime']
    pretty_time = time_as_string[:10] + "T" + time_as_string[11:]

    json_prep = {
        "uid": "urn:uuid:%s" % response['SynthesisTask']['TaskId'],
        "updateDate": pretty_time,
        "titleText": "Family News",
        "mainText": "",
        "streamUrl": response['SynthesisTask']['OutputUri']
    }

    feed_data = json.dumps(json_prep)
    
    s3 = boto3.client('s3')
    s3.put_object(ACL='public-read', Bucket='pollycal-family-news', Key='feed.json', Body=feed_data, Metadata={'Content-Type': 'application/json'})
    
    response = polly_client.start_speech_synthesis_task(VoiceId='Astrid',
                OutputFormat='mp3',
                OutputS3BucketName='pollycal-family-news',
                Text = a_string_to_speak)
    
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }

