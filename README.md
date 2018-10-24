# pollycal
Lambda to take all day calendar events, make polly audio, generate json

I wanted Alexa to speak Swedish, I had some dynamic-ish data to use and I wanted to learn how to make a lambda.

The local school has a public .ics format calendar that provides today's lunch as all-day events.
* Using ics python package to extract calendar events
* Uses Polly's Astrid voice to generate swedish audio
* Is configured as a Flash Briefing skill (private for now)

Assumes it is being run on the same day that the event is (ie, run between midnight and morning).
Assumes there is data to collect, otherwise it dies, there's no error handling.

TODO:
* Handle errors
* Demo video!
