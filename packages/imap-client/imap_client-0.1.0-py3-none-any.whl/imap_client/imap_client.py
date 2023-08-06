from __future__ import annotations
import imaplib
import email, email.message


def check_res(response):
    if response != "OK":
        raise ValueError("Bad response from connection")


class Msg:
    def __init__(self, id, inbox: Inbox):
        self.id = id
        self.conn = inbox.conn
        self.inbox = inbox
        self.preview_headers = {header: self.get_header(header).strip()
            for header in ["From", "Subject"]
        }
        self.raw_message = None
        self.message = None
        self.text_body = None
        self.html_body = None
        self.attachments = None

    def fetch_data(self):
        self.conn.select(f'"{self.inbox.name}"')
        self.message = self.get_message()
        body_parts = self.get_body(self.message)
        print(body_parts)
        self.text_body = self.parse_parts(body_parts, "text/plain")
        self.text_html = self.parse_parts(body_parts, "text/html")
        self.attachments = self.parse_attachments(body_parts)

    def get_data(self, data_type) -> bytes:
        res, data = self.conn.fetch(str(self.id), data_type)
        check_res(res)
        print(data)
        return data[0][1]

    def get_header(self, header) -> str:
        return self.get_data(f"BODY[HEADER.FIELDS ({header.upper()})]") \
               .decode().replace(header + ": ", "")

    def get_message(self) -> email.message.Message:
        contents = self.get_data("RFC822")
        self.raw_message = contents.decode()
        return email.message_from_bytes(contents) 
    
    def get_body(self, message: email.message.Message) \
        -> list(tuple(str, str) | tuple(str, str, str, email.message.Message)) \
         | tuple(str, str) | tuple(str, str, str, email.message.Message):
        """
        Returns a list of message parts, each a tuple consisting of the MIMEtype
        and the payload contents in decoded from, or, in the case of an
        attachment, a tuple with a string signalising "attachment", the
        MIMEtype, the attachment filename, and a reference to that message part
        for future attachment downloading using Message.get_payload().
        In case there is only 1 message part, it returns just that part in a
        tuple.
        """
        parts = []
                                                                                
        if message.is_multipart():
            for payload in message.get_payload():
                # recursively fetch payload of parts
                parts.append(self.get_body(payload))
            return parts

        if message.get_content_maintype() != "text"\
        and message.get_content_disposition() == "attachment":
            return (message.get_content_disposition(), message.get_content_type(),
                    message.get_filename(), message)

        return  (message.get_content_type(),
                 message.get_payload(decode=True).decode())

    def parse_parts(self, body_parts, type):
        print(body_parts)
        if isinstance(body_parts, tuple):
            if body_parts[0] == type:
                return body_parts[1]
            return None
        
        parsed_parts = []
        for part in body_parts:
            parsed_part = self.parse_parts(part, type)
            if parsed_part is not None:
                parsed_parts.append(parsed_part)

        return "\n".join(parsed_parts)


    def parse_attachments(self, body_parts):
        if isinstance(body_parts, tuple):
            if body_parts[0] == "attachment":
                return [body_parts]
            return None

        parsed_attachments = []
        for part in body_parts:
            parsed_attachment = self.parse_attachments(part)
            if parsed_attachment is not None:
                parsed_attachments += parsed_attachment

        return parsed_attachments

class Inbox:
    def __init__(self, flags, delimiter, name, size, **kwargs):
        self.flags = flags
        self.delimiter = delimiter
        self.name = name
        self.size = size
        self.conn = kwargs.get("conn")
        self.msg_display_amount = kwargs.get("msg_display_amount")
        self.msg_generator = self._get_messages()
        self.messages = self.msg_generator.__next__()

    def get_messages(self):
        self.conn.select(f'"{self.name}"')
        try:
            new_messages = self.msg_generator.__next__()
        except StopIteration:
            raise StopIteration("No more messages to fetch")
        else:
            self.messages += new_messages

    def _get_messages(self) -> list[Msg]:
        self.conn.select(f'"{self.name}"')

        if self.size == 0:
            yield []

        for i in range(self.size, 0, -self.msg_display_amount):

            msgs = []
            end = i - self.msg_display_amount
            end = end if end > 0 else 0
            for j in range(i, end, -1):
                msgs.append(Msg(j, self))

            yield msgs


class IMAPClient:
    def __init__(self, conn: imaplib.IMAP4 | imaplib.IMAP4_SSL,
                 msg_display_amount: int = 10):
        self.conn = conn
        self.msg_display_amount = msg_display_amount
        self.inbox_data = {
            "conn": conn, 
            "msg_display_amount": msg_display_amount
        }
        self.inboxes: list[Inbox] = self._get_inboxes()
    
    def get_display_inboxes(self):
        display = []

        for inbox in self.inboxes:
            display.append(inbox.name.ljust(40) + str(inbox.size).rjust(6))

        return display

    def _get_inboxes(self) -> list[Inbox]:
        res, inboxes = self.conn.list()
        check_res(res)

        parsed_inboxes: list[Inbox] = []

        for inbox in inboxes:
            flags, delimiter, name = (item.strip() for item
                in inbox.decode().split('"') if item.strip())

            flags = [flag.strip(" ()") for flag in flags.split("\\")
                if flag.strip(" ()")]
            if "Noselect" in flags:
                continue

            res, size = self.conn.select(f'"{name}"')
            check_res(res)
            size = int(size[0].decode())
            parsed_inboxes.append(Inbox(flags, delimiter, name, size,
                                        **self.inbox_data))

        # make "inbox" appear on top
        parsed_inboxes.sort(
            key=lambda inbox : 0 if "inbox" in inbox.name.lower() else 1
        )

        return parsed_inboxes
