#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors for :mod:`repoze.sendmail`, intended as a drop-in replacement
for the ``qp`` command line, using Amazon SES.

"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import gevent

import os

import time

from zope import interface

from email.message import Message

import boto3

from botocore.config import Config

from repoze.sendmail.encoding import encode_message

from repoze.sendmail.interfaces import IMailer

from repoze.sendmail.maildir import Maildir

from repoze.sendmail.queue import ConsoleApp as _ConsoleApp
from repoze.sendmail.queue import QueueProcessor

from zope.cachedescriptors.property import Lazy


@interface.implementer(IMailer)
class SESMailer(object):
    """
    This object does not handle throttling or quata actions;
    see also :mod:`nti.app.bulkemail.process`.
    """

    def __init__(self, region='us-east-1'):
        self.region=region

    @property
    def _ses_config(self):
        return Config(region_name=self.region)

    @Lazy
    def client(self):
        client = boto3.client('ses', config=self._ses_config)
        assert client
        return client

    def close(self):
        pass

    def send(self, fromaddr, toaddrs, message):
        if not isinstance(message, Message):  # pragma: no cover
            raise ValueError('Message must be instance of email.message.Message')

        message = encode_message(message)

        # Send the mail using SES, transforming SESError and known
        # subclasses into something the SMTP-based queue processor knows
        # how to deal with.
        # NOTE: now that we're here, we have the opportunity to de-VERP
        # the fromaddr found in the message, but still use the VERP form
        # in the fromaddr we pass to SES. In this way we can handle bounces
        # with the recipient none-the-wiser. See also :mod:`nti.app.bulkemail.process`
        # NOTE: Each recipient (To, CC, BCC) counts as a distinct message
        # for purposes of the quota limits. There are a maximum of
        # 50 dests per address. (http://docs.aws.amazon.com/ses/latest/APIReference/API_SendRawEmail.html)
        # NOTE: It is recommended to send an email to individuals:
        # http://docs.aws.amazon.com/ses/latest/DeveloperGuide/sending-email.html
        # "When you send an email to multiple recipients (recipients
        # are "To", "CC", and "BCC" addresses) and the call to Amazon
        # SES fails, the entire email is rejected and none of the
        # recipients will receive the intended email. We therefore
        # recommend that you send an email to one recipient at a time."

        # QQQ: The docs for SendRawEmail say that destinations is not required,
        # so how does that interact with what's in the message body?
        # Boto will accept either a string, a list of strings, or None
        self.client.send_raw_email(RawMessage={'Data': message},
                                   Source=fromaddr,
                                   Destinations=toaddrs)


import argparse
import sys
import logging

class ConsoleApp(_ConsoleApp):

    def __init__(self, argv=None):  # pylint: disable=unused-argument
        if argv is None:
            argv = sys.argv
        # Bypass the superclass, don't try to construct an SMTP mailer
        self.script_name = argv[0]
        self._process_args(argv[1:])
        self.mailer = SESMailer()
        getattr(self.mailer, 'client')


class MailerProcess(object):
    """
    A mailer processor that dumps the queue on a provided interval.
    """

    _exit = False

    def __init__(self, mailer_factory, queue_path, sleep_seconds=120):  # pylint: disable=unused-argument
        self.mailer_factory = mailer_factory
        self.sleep_seconds = sleep_seconds
        self.queue_path = queue_path
        self.mail_dir = Maildir(self.queue_path, create=True)

    def _maildir_factory(self, *args, **kwargs):
        return self.mail_dir

    def _do_process_queue(self):
        mailer = self.mailer_factory()
        assert mailer
        try:
            processor = QueueProcessor(mailer,
                                       self.queue_path, # Note this gets ignored by the Maildir factory we send
                                       Maildir=self._maildir_factory)
            logger.info('Processing messages %s' % (processor.maildir.path))
            processor.send_messages()
        finally:
            try:
                mailer.close()
            except AttributeError:
                pass
            mailer = None

    def run(self):
        while not self._exit:
            self._do_process_queue()
            logger.debug('Going to sleep for %i seconds' % (self.sleep_seconds))
            time.sleep(self.sleep_seconds)

def _stat_modified_time(attrs):
    """
    libev and libuv expose different attributes.
    Specifically modified time is st_mtime or st_mtim respectively.
    In libuv we need to look at st_mtim.tv_sec
    """
    try:
        return attrs.st_mtime
    except AttributeError:
        return attrs.st_mtim.tv_sec

def _stat_watcher_modified(watcher):
    """
    Inspects the stat watcher to see if the modified time
    has changed between the current attrs and the prev attrs
    """
    return _stat_modified_time(watcher.prev) != _stat_modified_time(watcher.attr)


_MINIMUM_DEBOUNCE_INTERVAL_SECONDS = 10


class MailerWatcher(MailerProcess):
    """
    A Mailer processor that watches for changes in the mail directory
    using gevent stat watchers.
    """
    watcher = None
    debouncer = None
    debouncer_count = 0

    max_process_frequency_seconds = _MINIMUM_DEBOUNCE_INTERVAL_SECONDS

    def __init__(self, *args, **kwargs):
        super(MailerWatcher, self).__init__(*args, **kwargs)
        hub = gevent.get_hub()
        to_watch = os.path.join(self.queue_path, str('new'))
        self.watcher = hub.loop.stat(to_watch)

    def _start_watching(self):
        assert self.watcher
        logger.debug('Starting watcher for MailDir %s', self.watcher.path)
        self.watcher.start(self._stat_change_observed)

    def _stop_watching(self):
        assert self.watcher
        logger.debug('Stopping watcher for MailDir %s', self.watcher.path)
        self.watcher.stop()

    def _do_process_queue(self):
        # The path we are watching has been modified
        #self._stop_watching()
        super(MailerWatcher, self)._do_process_queue()
        #self._start_watching()

    def _youve_got_mail(self):
        # We've detected we have mail. We want to debounce
        # this so we aren't going crazy. Process the queue at most ever
        # self.max_process_frequency_seconds
        # We use a gevent timer to accomplish this.

        hub = gevent.get_hub()
        if self.debouncer is None:
            self.debouncer = hub.loop.timer(self.max_process_frequency_seconds)

        def _timer_fired(self):
            self.debouncer.stop()
            self.debouncer = None
            if self.debouncer_count > 0:
                self.debouncer_count = 0
                self._youve_got_mail()

        if self.debouncer.active is False:
            self.debouncer_count = 0
            self.debouncer.start(_timer_fired, self)
            logger.info('Processing mail queue. Queue processing paused for %i seconds', self.max_process_frequency_seconds)
            self._do_process_queue()
        else:
            self.debouncer_count += 1
            logger.debug('Deferring queue processing because it was run recently')

    def _stat_change_observed(self):
        # On certain file systems we will see stat changes
        # for access times which we don't care about. We really
        # only care about modified times.`

        if _stat_watcher_modified(self.watcher):
            logger.debug('Maildir watcher detected MailDir modification')
            self._youve_got_mail()

    def run(self, seconds=None):
        # Process once initially in case we have things in the queue already
        self._do_process_queue()

        # Note we don't call start watching because _do_process_queue handles that
        self._start_watching()
        gevent.get_hub().join(seconds)

_LOG_LEVELS = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

def _log_level_for_verbosity(verbosity=0):
    return _LOG_LEVELS[min(max(verbosity, 0), len(_LOG_LEVELS) - 1)]


def run_process(): # pragma: no cover

    parser = argparse.ArgumentParser(
        description='Spawn a process that stays alive, periodically polling the mail queue '
        'and sending new mail using SES.')
    parser.add_argument('queue_path',
                        help='The path to the maildir',
                        action='store')
    parser.add_argument('-r', '--sesregion',
                        help='The SES region to connect to.')
    parser.add_argument('-v', '--verbose',
                        help='How verbose to log.',
                        action='count',
                        default=1)
    parser.add_argument('-w', '--debounce-interval',
                        dest='interval',
                        help=('The number of seconds to wait between dumping the queue '
                              '(default: %(default)s)'),
                        action='store',
                        default=MailerWatcher.max_process_frequency_seconds,
                        type=int)

    arguments = parser.parse_args()

    log_level = _log_level_for_verbosity(arguments.verbose)
    logging.basicConfig(stream=sys.stderr,
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=log_level)

    _mailer_factory = SESMailer if not arguments.sesregion else (lambda: SESMailer(arguments.sesregion))

    app = MailerWatcher(_mailer_factory, arguments.queue_path)

    if arguments.interval:
        app.max_process_frequency_seconds = max(_MINIMUM_DEBOUNCE_INTERVAL_SECONDS,
                                                arguments.interval)

    logger.info('Using debounce interval of %i', app.max_process_frequency_seconds)
    app.run()

def run_console(): # pragma: no cover
    if '--help' in sys.argv:
        # Override the help message we get from repoze.sendmail, we
        # ignore all the SMTP stuff it wants to do.
        parser = argparse.ArgumentParser(
            description='Process the mail queue one time and exit. '
            'Mail found in the mail queue will be sent using default SES settings.'
        )
        parser.add_argument('queue_path',
                        help='The path to the maildir',
                        action='store')
        parser.parse_args()
        return

    logging.basicConfig(stream=sys.stderr,
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.WARN)
    app = ConsoleApp()
    app.main()

if __name__ == "__main__":  # pragma NO COVERAGE
    run_console()
