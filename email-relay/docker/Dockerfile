FROM amazonlinux:2

# Specify an argument. This defaults to cdl-general-dev.
ARG aws_profile

RUN echo "aws profile is set to ${aws_profile}"

# Update system packages
RUN yum update -y

# Install logging package for postfix to log out
RUN yum install rsyslog diffutils cyrus-sasl-plain -y

# Debug tools...
#RUN yum install vim less -y
#ADD test.email /test.email

# Install ghettoforge yum repo file for Postfix3
RUN curl http://mirror.ghettoforge.org/distributions/gf/RPM-GPG-KEY-gf.el7 -o /etc/pki/rpm-gpg/RPM-GPG-KEY-gf.el7
RUN curl  http://mirror.ghettoforge.org/distributions/gf/gf-release-latest.gf.el7.noarch.rpm -o gf-release-latest.gf.el7.noarch.rpm
RUN rpm -i gf-release-latest.gf.el7.noarch.rpm

# Clean Yum cache
RUN yum clean all
RUN yum makecache fast

# Install postfix3 from ghettoforge. the referenced 3.3.1 is only in the gf-testing repo atm. Will need to change it to come from gf-plus once it's released properly.
RUN yum --enablerepo=gf-plus,gf-testing,gf install postfix3-3.3.1-1.gf.el7 -y

# Remove sendmail after installing postfix to keep dependencies needed by postfix.
RUN yum remove sendmail

# Configure the mail transmit agent to be postfix.
RUN alternatives --set mta /usr/sbin/sendmail.postfix

# Do a global replace to comment out any other hosts left in config
RUN sed -i 's/relayhost =/#relayhost =/g' /etc/postfix/main.cf

# Configure postfix using postconf tool.
RUN postconf -e "inet_protocols=ipv4"
RUN postconf -e "relayhost=[email-smtp.eu-west-1.amazonaws.com]:587"
RUN postconf -e "smtp_sasl_auth_enable=yes"
RUN postconf -e "smtp_sasl_security_options=noanonymous"
RUN postconf -e "smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd"
RUN postconf -e "smtp_use_tls=yes"
RUN postconf -e "smtp_tls_security_level=encrypt"
RUN postconf -e "smtp_tls_note_starttls_offer=yes"
RUN postconf -e "inet_interfaces=all"
RUN postconf -e "mynetworks=127.0.0.0/8 10.0.0.0/8"

# hash out setting
RUN sed -i 's/-o smtp_fallback_relay=/#-o smtp_fallback_relay=/g' /etc/postfix/master.cf

# Configure Postfix credentials for SES
RUN touch /etc/postfix/sasl_passwd

ADD ses_creds/$aws_profile.txt /etc/postfix/sasl_passwd

RUN postmap hash:/etc/postfix/sasl_passwd
RUN chmod 0600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db

RUN postconf -e 'smtp_tls_CAfile = /etc/ssl/certs/ca-bundle.crt'

# Required for postfix service files as not present in container
RUN echo NETWORKING=yes > /etc/sysconfig/network

ENTRYPOINT ["/sbin/postfix", "start-fg"]
