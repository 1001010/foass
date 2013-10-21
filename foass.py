#!/usr/bin/python
# for linux

# This implementation of FOASS is (c) 2013 Jason De Arte, All Rights Reserved.
# Someone more awesome than me came up with the idea for FOASS, I just implemented my 
# server version using their published API as a personal learning experience to 
# stretch my skills in Python as a software engineer.

import os
import json
import random
import cgitb

# Enable mostly readable web page errors
cgitb.enable()


class SETTINGS():
    RANDOM_NAMES = ['Monte', 'Craig', 'Nico', 'Kurtis', 'Oliver', 'Dawson', 'Jason']
    MAX_URI_ELEMENTS = 3

    COMMAND_TABLE = {
        #quick index : URI                    Human Readable Replacement Text
        'off'        : ('off/:name/:from',    ('Fuck off, :name.', ':from')),
        'you'        : ('you/:name/:from',    ('Fuck you, :name.', ':from')),
        'this'       : ('this/:from',         ('Fuck this', ':from')),
        'that'       : ('that/:from',         ('Fuck that.', ':from')),
        'everything' : ('everything/:from',   ('Fuck everything.', ':from')),
        'everyone'   : ('everyone/:from',     ('Everyone can go and fuck off.', ':from')),
        'donut'      : ('donut/:name/:from',  (':name, go and take a flying fuck at a rolling donut.', ':from')),
        'shakespeare': ('shakespeare/:name/:from', (':name, Thou clay-brained guts, thou knotty-pated fool, thou whoreson obscene greasy tallow-catch!',':from')),
        'linus'      : ('linus/:name/:from',  (':name, there aren\'t enough swear-words in the English language, so now I\'ll have to call you perkeleen vittup&auml;&auml; just to express my disgust and frustration with this crap.',':from')),
        'pink'       : ('pink/:from',         ('Well, Fuck me pink.', ':from')),
        'king'       : ('king/:name/:from',   ('Oh fuck off, just really fuck off you total dickface. Christ :name, you are fucking thick.',':from')),
        'life'       : ('life/:from',         ('Fuck my life.', ':from')),
        'chainsaw'   : ('chainsaw/:name/:from', ('Fuck me gently with a chainsaw, :name. Do I look like Mother Teresa?', ':from')),
        'thanks'     : ('thanks/:from',       ('Fuck you very much.', ':from')),

        # Non-standard additions
        'given'      : ('given/:from',        ('0 fucks given.', ':from')),
        'eat'        : ('eat/:name/:from',    ('Eat a bowl of dicks, :name.',':from')),
        'bowl'       : ('bowl/:name/:from',   ('Eat a bowl of dicks, :name.',':from')),
        'bag'        : ('bag/:name/:from',    ('Eat a bag of dicks, :name.',':from')),
        'essex'      : ('essex/:name/:from',  ('Bollocks to that, yooooou stooooopid wanker, you, :name!',':from')),
        'london'     : ('london/:name/:from', ('That\'s bollocks, innit, :name.',':from')),
        'ity'        : ('ity/:name/:from',    ('What the fuckity fuck-fuck were you fucking doing, :name?', ':from')),
        'lawn'       : ('lawn/:name/:from',   ('Get off my Fucking lawn, :name.', ':from')),
    }

    DEFAULT_RESULT = {'message': 'What the fuck sort of call was that?  Next time, check your fucking typing', 'subtitle': 'The Server'}


def GetRequest():
    request = None
    try:
        request = [x for x in os.environ['REQUEST_URI'].split('/') if x is not '']
        if request is None or len(request) == 0:
            # empty request or user is requesting the home page
            request = []
    except:
        request = None
    return request


def GetTransformedResponse(request, want_examples):
    """ returns a single item simple dict suitable for plaintext or json or html conversion
        unless you want extended data for the API page
    """
    result = None
    try:
        while len(request) < SETTINGS.MAX_URI_ELEMENTS:
            request.append(SETTINGS.RANDOM_NAMES[random.randint(0,len(SETTINGS.RANDOM_NAMES)-1)])

        cmd_values = SETTINGS.COMMAND_TABLE[request[0]]
        cmd_uri = cmd_values[0]
        cmd_result = cmd_values[1]
        replacements = dict(zip(cmd_uri.split('/')[1:], request[1:]))

        result = {
            'message': cmd_result[0],
            'subtitle': cmd_result[1]
        }

        if want_examples:
            result.update({
                'uri'        : '/' + cmd_uri,
                'uri_example': '/' + cmd_uri,
                'cmd'        : ' - '.join(cmd_result),
                'cmd_example': ' - '.join(cmd_result)})

        for key in replacements:
            result['message' ] = result['message' ].replace(key, replacements[key])
            result['subtitle'] = result['subtitle'].replace(key, replacements[key])
            if want_examples:
                result['uri_example'] = result['uri_example'].replace(key, replacements[key])
                result['cmd_example'] = result['cmd_example'].replace(key, replacements[key])
    except Exception:
        result = None
    return result


def do_html():
    def render_homepage():
        print '<body style="">'
        print '<div class="container">'
        print ' <div class="hero-unit">'
        print '  <h1><strike>FOAAS</strike> FOASS<h1>'
        print '  <h2><strike>Fuck Off As A Service</strike> Don\'t care about the backronym, it\'s funnier as FO<i>ASS</i></h2>'
        print '  <p>Please see the README for use.</p>'
        print '  <p><em>local variation of v0.0.1.2</em></p>'
        print '  <p>This python re-implementation (and direct lift of the layout) of the awesome groundbreaking work found at <a href="http://foaas.herokuapp.com/">http://foaas.herokuapp.com/</a> is done solely as a python cgi coding exersise to test my skills (or lack there of).<br/>'
        print ' OK, maybe that\'s a little lie. My inner child is definitely doing a fist pump in the air and screaming "Fuck Yea! I\'m so proud of grown up me".<br/>'
        print ' IT IS NOT INTENDED TO BE FEATURE COMPLETE OR USED BY ANYONE BY ANY STRETCH OF THE IMAGINATION<br/>'
        print '- <a href="http://JasonDeArte.com/wp/tag/foass/">Jason De Arte</a>'
        print '  </p>'
        print ' </div>'
        print '</div>'
        print '<div class="container">'
        print ' <div class="content" style="margin-left:50px;">'
        print '  <h2 id="introduction">Introduction</h2>'
        print '  <p>FOAAS (Fuck Off As A Service) provides a modern, RESTful, scalable solution to the common problem of telling people to fuck off.</p>'
        print '  <h2 id="contentnegotiation">Content Negotiation</h2>'
        print '  <p>FOAAS will respond to the following \'<code>Accept:</code>\' request header values with appropriate content</p>'
        print '  <ul>'
        print '   <li><code>text/plain</code> - Content will be returned as a plain string.</li>'
        print "   <li><code>application/json</code> - Content will be returned as a JSON object <code>{ message: 'message', subtitle: 'subtitle' }</code></li>"
        print '   <li><code>text/html</code> - <b>default</b> - Content will be returned as an HTML page with a twitter bootstrap hero unit, containing the message and the subtitle.</li>'
        print '  </ul>'
        print '  <p />'

        print "  <div id='api_commands'>"
        print '   <h2>API</h2><hr/>'
        for key in SETTINGS.COMMAND_TABLE:
            sample_response = GetTransformedResponse([key], want_examples=True)
            print "<h3>" + sample_response['uri'] + "</h3>"
            print "<p>Will return content of the form '" + sample_response['cmd'] + "', e.g. "
            print "<a href='" + sample_response['uri_example'] + "'>" + sample_response['uri_example'] + "</a>"
            print " will return '<em>" + sample_response['cmd_example'] + "</em>'</p>"
            print '<hr/>'
        print "  </div>"

        print '<div class="container">'
        print ' <div class="hero-unit">'
        print '  <h2>EOFF == End Of Fucking File</h2>'
        print '  <p><em> - The Server</em></p>'
        print '</div></div>'

        print ' </div>'
        print '</div>'
        print '</body>'

    def render_html_quote():
        print '<body style="margin-top:40px;">'
        print '<div class="container">'
        print ' <div id="view-10" view="">'
        print '  <div class="hero-unit">'
        print '   <h1>' + response['message'] + '</h1>'
        print '   <p><em> - ' + response['subtitle'] + '</em></p>'
        print '  </div>'
        print '  <a href="/">How to fuck yourself</a>'
        print ' </div>'
        print '</div>'
        print '</body>'

    print "Content-type: text/html\n"
    print "<html>"
    print "<head>"
    print '<title>FOAAS</title>'
    print '<meta charset="utf-8"/>'
    print '<link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet" />'
    print '</head>'

    request = GetRequest()
    if not request:
        render_homepage()
    else:
        response = GetTransformedResponse(request, want_examples=False)
        if not response:
            response = SETTINGS.DEFAULT_RESULT
        render_html_quote()

    print '</html>'


def do_json():
    print "Content-type: application/json\n"
    result = SETTINGS.DEFAULT_RESULT
    request = GetRequest()
    if request:
        response = GetTransformedResponse(request, want_examples=False)
        if response:
            result = response
    print json.dumps(result, indent=2)


def do_plaintext():
    print "Content-type: text/plain\n"
    result = SETTINGS.DEFAULT_RESULT
    request = GetRequest()
    if request:
        response = GetTransformedResponse(request, want_examples=False)
        if response:
            result = response
    print result['message'] + ' - ' + result['subtitle']


def main():
    accept_types = []
    try:
        accept_types = os.environ['HTTP_ACCEPT'].split(',')
    except Exception:
        pass

    if 'application/json' in accept_types:
        do_json()
    elif 'text/plain' in accept_types:
        do_plaintext()
    else:
        do_html()

if __name__ == "__main__":
    main()
