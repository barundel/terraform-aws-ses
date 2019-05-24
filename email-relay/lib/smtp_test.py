import email.utils
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer


def send_mail():
    start_time = time.time()
    # Replace sender@example.com with your "From" address.
    # This address must be verified.
    # SENDER = 'josh.sinfield@cdl.co.uk'
    # SENDERNAME = 'Josh Sinfield'
    SENDER = 'josh.sinfield@cdl.co.uk'
    SENDERNAME = 'Josh Sinfield'

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    # RECIPIENT = 'ben.arundel@cdl.co.uk'
    # RECIPIENTNAME = 'Ben Arundel'

    # RECIPIENT = 'ashley.fairclough@cdl.co.uk'
    # RECIPIENTNAME = 'Ashley Fairclough'

    # recipients_addr = ['ben.arundel@cdl.co.uk', 'rob.houghton@cdl.co.uk', 'josh.sinfield@cdl.co.uk']
    # recipients_names = ['Ben Arundel', 'Rob Houghton', 'Josh Sinfield']
    # formatted_recipients = [email.utils.formataddr((recipients_names[i],recipients_addr[i])) for i in range(0,len(recipients_names))]

    recipients = [
        # ('Ben Arundel', 'ben.arundel@cdl.co.uk'),
        # ('Ashley Fairclough', 'ashley.fairclough@cdl.co.uk'),
        # ('Rob Houghton', 'rob.houghton@cdl.co.uk'),
        ('Josh Sinfield', 'josh.sinfield@cdl.co.uk')
    ]

    formatted_recipients = [email.utils.formataddr(i) for i in recipients]

    print(formatted_recipients)
    all_recipients = ', '.join(formatted_recipients)
    # all_recipients_addrs = ','.join(recipients_addr)
    # print('all_rec_addrs', all_recipients_addrs)

    # # Replace smtp_username with your Amazon SES SMTP user name.
    # USERNAME_SMTP = "smtp_username"
    #
    # # Replace smtp_password with your Amazon SES SMTP password.
    # PASSWORD_SMTP = "smtp_password"
    #
    # # (Optional) the name of a configuration set to use for this message.
    # # If you comment out this line, you also need to remove or comment out
    # # the "X-SES-CONFIGURATION-SET:" header below.
    # CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
    # endpoint in the appropriate region.
    HOST = "ses-relay.dev.cdlcloud.co.uk"
    PORT = 443

    # The subject line of the email.
    SUBJECT = 'Josh SES Test via postfix using (Python smtplib)'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test\r\n"
                 "This email was sent through postfix ")

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES SMTP Email Test</h1>
      <p>This email was sent with Amazon SES using the
        <a href='https://www.python.org/'>Python</a>
        <a href='https://docs.python.org/3/library/smtplib.html'>
        smtplib</a> library.</p>
    </body>
    </html>
                """

    main_msg = MIMEMultipart()
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    main_msg['Subject'] = SUBJECT
    main_msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    # main_msg['To'] = email.utils.formataddr((RECIPIENTNAME,RECIPIENT))
    main_msg['To'] = all_recipients
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
    main_msg.add_header('X-SES-CONFIGURATION-SET', 'track-the-email')

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')
    part3 = MIMEApplication(open('test_attachment.txt', 'rb').read())
    part3.add_header('Content-Disposition', 'attachment; filename="test_attachment.txt"')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    main_msg.attach(msg)
    main_msg.attach(part3)

    range_max = 10
    for i in range(1, range_max):
        # Try to send the message.
        try:
            print('i: ', i, 'Connecting to server...')
            server = smtplib.SMTP(HOST, PORT)
            print('After connection. calling ehlo')
            # server.ehlo()
            # server.starttls()
            # stmplib docs recommend calling ehlo() before & after starttls()
            # server.ehlo()
            # server.login(USERNAME_SMTP, PASSWORD_SMTP)
            # server.sendmail(SENDER, RECIPIENT, main_msg.as_string())
            server.sendmail(SENDER, formatted_recipients, main_msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")

    end_time = time.time()
    diff = end_time - start_time
    print('Took {0}s to send {1} emails'.format(diff, len(range(1, range_max))))
    invokeTimer()


def invokeTimer():
    Timer(1, send_mail).start()


if __name__ == '__main__':
    invokeTimer()

    # send_mail()
