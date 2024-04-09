import sys, ssl, time
from imap_tools import MailBox
from config_data.config import ConfigMail, load_config_mail


config: ConfigMail = load_config_mail()
email: str = config.config_mail.email
password: str = config.config_mail.password
imap: str = config.config_mail.imap


def get_mail(number_test):

    try:
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT')

        with MailBox(imap, ssl_context=ctx).login(email, password) as mailbox:
            for msg in mailbox.fetch(reverse=True, limit=55):
                if number_test in msg.text:
                    result = msg.date
                    time.sleep(2)
                    mailbox.move([msg.uid], 'Trash')
                    time.sleep(2)
                    return result.strftime('%x %X')
            return (0, 'письмо не получено дольше допустимого')
    except Exception:
        return ('0', str(sys.exc_info()[1]))

if __name__ == '__main__':
    print(get_mail('number_test'))