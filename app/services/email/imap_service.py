import email
from email import policy
import aioimaplib
from config.config import EMAIL_SETTINGS


# ПОДРЕФАКТОРИТЬ И ЛУЧШЕ РАЗОБРАТЬСЯ
class EmailImapService:
    def __init__(self):
        self.imap_server = EMAIL_SETTINGS.IMAP_SERVER
        self.imap_port = EMAIL_SETTINGS.IMAP_PORT
        self.imap_username = EMAIL_SETTINGS.IMAP_USERNAME
        self.imap_password = EMAIL_SETTINGS.IMAP_PASSWORD
        self.client = aioimaplib.IMAP4_SSL(host=self.imap_server, port=self.imap_port)

    async def load_emails(self, mailbox="INBOX", criteria="UNSEEN", mark_seen=True):
        """Загружает письма с сервера"""
        try:
            await self.client.wait_hello_from_server()
            await self.client.login(self.imap_username, self.imap_password)
            await self.client.select(mailbox)

            # Поиск писем по критерию
            result, data = await self.client.search(criteria)

            if result != "OK" or not data or not data[0]:
                print("Писем не найдено")
                return []

            email_ids = data[0].split()
            results = []

            for email_id in email_ids:
                try:
                    # Декодируем ID и используем в команде FETCH
                    email_id_str = email_id.decode("utf-8")

                    # Формируем команду FETCH - ВАЖНО: без лишних скобок
                    if mark_seen:
                        result, fetch_data = await self.client.fetch(
                            email_id_str, "BODY[]"
                        )
                    else:
                        result, fetch_data = await self.client.fetch(
                            email_id_str, "BODY.PEEK[]"
                        )

                    if result != "OK":
                        print(f"Ошибка получения письма {email_id_str}: {result}")
                        continue

                    # Извлекаем данные письма
                    raw_email = await self.extract_email_data(fetch_data)

                    if raw_email:
                        # Парсим письмо
                        email_message = email.message_from_bytes(
                            raw_email, policy=policy.default
                        )
                        parsed_email = self.process_email(email_message)
                        results.append(parsed_email)

                        print(f"Обработано письмо: {parsed_email['subject'][:50]}...")
                    else:
                        print(f"Не удалось извлечь данные письма для ID {email_id_str}")

                except Exception as e:
                    print(f"Ошибка при обработке письма {email_id}: {e}")
                    continue

            return results

        except Exception as e:
            print(f"Ошибка при загрузке писем: {e}")
            import traceback

            traceback.print_exc()
            return []
        finally:
            await self.client.logout()

    async def extract_email_data(self, fetch_data):
        """Извлекает сырые данные письма из ответа IMAP"""
        try:
            # Более надежный способ извлечения данных
            for i, item in enumerate(fetch_data):
                if isinstance(item, (bytearray, bytes)):
                    data = bytes(item) if isinstance(item, bytearray) else item
                    # Ищем начало email данных (обычно начинается с Delivered-To или Return-Path)
                    if len(data) > 100 and (
                        b"Delivered-To" in data
                        or b"Return-Path" in data
                        or b"Received:" in data
                    ):
                        return data

            # Альтернативный поиск - берем самый большой bytearray/bytes
            large_items = [
                item
                for item in fetch_data
                if isinstance(item, (bytearray, bytes)) and len(item) > 1000
            ]
            if large_items:
                largest = max(large_items, key=len)
                return bytes(largest) if isinstance(largest, bytearray) else largest

            return None

        except Exception as e:
            print(f"Ошибка при извлечении данных письма: {e}")
            return None

    def process_email(self, email_message):
        """Обрабатывает письмо и извлекает содержимое"""
        email_text = ""
        email_html = ""
        attachments = []

        try:
            if email_message.is_multipart():
                # Обрабатываем все части письма
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))

                    # Пропускаем служебные части
                    if content_type.startswith("multipart/"):
                        continue

                    # Извлекаем plain text
                    if (
                        content_type in ("text/plain", "text/html")
                        and "attachment" not in content_disposition
                    ):
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                charset = part.get_content_charset("utf-8")
                                email_text = payload.decode(
                                    charset or "utf-8", errors="ignore"
                                )
                        except Exception as e:
                            print(f"Ошибка декодирования: {e}")

                    # Извлекаем вложения
                    elif "attachment" in content_disposition or part.get_filename():
                        filename = part.get_filename()
                        if filename:
                            try:
                                file_data = part.get_payload(decode=True)
                                attachments.append(
                                    {
                                        "filename": filename,
                                        "data": file_data,
                                        "content_type": content_type,
                                    }
                                )
                            except Exception as e:
                                print(f"Ошибка извлечения вложения: {e}")
            else:
                # Письмо не multipart - просто извлекаем текст
                try:
                    payload = email_message.get_payload(decode=True)
                    if payload:
                        charset = email_message.get_content_charset("utf-8")
                        email_text = payload.decode(charset or "utf-8", errors="ignore")
                except Exception as e:
                    print(f"Ошибка декодирования простого письма: {e}")

            # Если нет plain text, но есть HTML, используем HTML
            if not email_text and email_html:
                email_text = self._html_to_text(email_html)

        except Exception as e:
            print(f"Ошибка в process_email: {e}")

        return {
            "subject": email_message.get("subject", ""),
            "from": email_message.get("from", ""),
            "date": email_message.get("date", ""),
            "text": email_text,
            "html": email_html,
            "attachments": attachments,
        }

    def _html_to_text(self, html_content):
        """Простая конвертация HTML в текст"""
        if not html_content:
            return ""

        import re

        # Удаляем HTML теги
        clean_text = re.sub(r"<[^>]+>", " ", html_content)
        # Заменяем множественные пробелы на один
        clean_text = re.sub(r"\s+", " ", clean_text)
        return clean_text.strip()
