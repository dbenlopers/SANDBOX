# -*- coding: utf-8 -*-

import telnetlib


def check_broker_state(broker):
    conn = broker.connection()
    telnetlib.Telnet(conn.hostname, conn.port)
    conn.close()
