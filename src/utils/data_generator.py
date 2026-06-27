from faker import Faker
import random
import json
import os

random.seed(42)
fake = Faker("ru_RU")

templates = [
    "Меня зовут {name}, мой email {email}. ",
    "Позвоните мне по номеру {phone}, я живу по адресу {address}.",
    "Клиент {name} оплатил заказ на сумму 5000 руб. Реквизиты: {email}, {phone}",
    "Заявка оформлена на {name}, контакт: {email}.",
    "Контактная информация: ФИО — {name}, телефон — {phone}, почта — {email}. Адрес регистрации: {address}.",
    "Пользователь {name} оставил заявку. Для связи: {email} или {phone}.",
    "Доставка будет по адресу: {address}. Получатель: {name}, контактный телефон {phone}.",
    "Здравствуйте, {name}! Подтвердите, пожалуйста, ваш email: {email} и номер телефона {phone}.",
    "Сотрудник {name} принят на работу. Контакты: {email}, {phone}. Адрес проживания: {address}.",
    "Запрос от клиента {name}: {email}, {phone}. Тема: возврат товара.",
    "Новая регистрация: {name}, {email}, {phone}. Адрес: {address}.",
    "Письмо от {name} ({email}): «Могу ли я уточнить детали по телефону {phone}? Живу по адресу {address}.»",
    "Заявка №12345 от {name}, email: {email}, телефон: {phone}. Адрес доставки: {address}.",
    "Клиент {name} сообщил, что не получил письмо на {email}. Позвоните ему по {phone}.",
    "Обратная связь: {name}, {phone}. Почта для ответа — {email}.",
    "Запрос на поддержку от {name} ({email}). Телефон для связи: {phone}.",
    "Данные для учёта: ФИО — {name}, email — {email}, телефон — {phone}, адрес — {address}.",
    "Пользователь {name} указал контакт: {phone}. Альтернативная почта: {email}.",
    "Согласие на обработку данных предоставлено {name} ({email}, {phone}, {address}).",
    "Клиент {name} отменил заказ. Контакты: {email}, {phone}.",
    "Офис по адресу {address} посетил клиент {name}. Контакт: {email}, {phone}.",
    "Запрос на выписку отправлен от {name}, {email}, {phone}.",
    "Подтвердите личность: ФИО — {name}, email — {email}, телефон — {phone}.",
    "Поступила жалоба от {name} ({email}, {phone}) по поводу доставки на {address}.",
    "Номер телефона {phone} принадлежит {name}, email: {email}.",
    "Адрес {address} зарегистрирован на {name}. Контакт: {email}, {phone}.",
    "Информация о пользователе: {name}, {email}, {phone}, {address}.",
    "Запрос на смену пароля от {name} ({email}). Телефон: {phone}.",
    "Клиент {name} подтвердил доставку по адресу {address}. Контакт: {phone}, {email}.",
    "Заявка создана автоматически: пользователь {name}, email {email}, телефон {phone}.",
    "Для связи с {name} используйте {email} или звоните по {phone}.",
    "Клиент {name} оставил отзыв. Контактные данные: {email}, {phone}, {address}.",
    "Сотрудник {name} временно недоступен. Эл. почта: {email}, резервный телефон: {phone}.",
    "Запрос на открытие доступа: {name}, {email}, {phone}, адрес — {address}.",
    "Пользователь {name} внес изменения в профиль: email ({email}), телефон ({phone}), адрес ({address}).",
    "Уведомление отправлено на {email} и {phone} пользователю {name}.",
    "Клиент {name} запросил звонок. Контакты: {email}, {phone}. Адрес: {address}.",
    "Данные для инвойса: {name}, {email}, {address}. Телефон: {phone}.",
    "Запрос от партнёра: контактное лицо — {name}, email: {email}, телефон: {phone}.",
    "Поддержка, здравствуйте. Я {name}, мой email {email}, телефон {phone}. У меня вопрос по адресу {address}.",
    "Клиент {name} подтвердил личность через email {email} и телефон {phone}.",
    "Доставка отменена. Клиент {name}, {phone}, {email}, адрес: {address}.",
    "Запрос на возврат средств от {name} ({email}, {phone}).",
    "Клиент {name} сообщил об ошибке в данных: email {email}, телефон {phone}, адрес {address}.",
    "Автоматическое уведомление: пользователь {name} ({email}) подключился с телефона {phone}.",
    "Заявка на тур оформлена на {name}. Контакты: {email}, {phone}. Адрес: {address}.",
    "Пользователь {name} подписался на рассылку. Контакт: {email}, {phone}.",
    "Клиент {name} изменил email на {email} и телефон на {phone}. Адрес остался: {address}.",
    "Запрос на сертификат: {name}, {email}, {phone}, {address}. {email} {phone} {email}",
    "Клиент {name} оставил сообщение: «Мой email {email}, звоните по {phone} по поводу {address}.»",
    "Подтверждение регистрации: {name}, {email}, {phone}, {address}.",
    "Клиент {name} запросил копию договора. Контакты: {email}, {phone}, {address}.",
    "Заявка на кредит подана {name}. Контакты: {email}, {phone}, адрес регистрации: {address}.",
    "Пользователь {name} обновил профиль: email — {email}, телефон — {phone}, адрес — {address}.",
    "Клиент {name} сообщил, что не получает письма на {email}. Позвоните по {phone}.",
    "Запрос на смену тарифа от {name} ({email}, {phone}). Адрес: {address}.",
    "Клиент {name} отказался от подписки. Контакты: {email}, {phone}, {address}.",
    "Запрос на восстановление аккаунта: {name}, {email}, {phone}.",
    "Клиент {name} подтвердил адрес {address} через звонок на {phone} и письмо на {email}.",
    "Заявка на ремонт принята от {name}. Контакты: {email}, {phone}. Адрес: {address}.",
    "Пользователь {name} оставил отзыв: «Спасибо! Связались по {phone}, ответили на {email}.»",
    "Клиент {name} запросил выписку по счёту. Контакты: {email}, {phone}, {address}.",
    "Заявка на визу: {name}, {email}, {phone}, {address}.",
    "Клиент {name} сообщил об утере карты. Контакты: {email}, {phone}, {address}.",
    "Поддержка, помогите! Я {name}, мой email {email}, телефон {phone}, адрес {address}.",
    "Клиент {name} подтвердил получение посылки. Контакты: {email}, {phone}.",
    "Запрос на открытие счёта: {name}, {email}, {phone}, {address}.",
    "Клиент {name} отменил визит. Контакты: {email}, {phone}, {address}.",
    "Пользователь {name} сменил номер. Старый: {phone}, новый: {phone}. Email: {email}."
]

def generate_sample_with_entities():
    template = random.choice(templates)

    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    address = fake.address()

    text = template.format(name=name, email=email, phone=phone, address=address)
    text = text.strip()

    entities = []

    start = text.find(name)
    if start != -1:
        entities.append({
            "start": start,
            "end": start + len(name),
            "label": "PERSON"
        })

    start = text.find(email)
    if start != -1:
        entities.append({
            "start": start,
            "end": start + len(email),
            "label": "EMAIL"
        })

    start = text.find(phone)
    if start != -1:
        entities.append({
            "start": start,
            "end": start + len(phone),
            "label": "PHONE_NUMBER"
        })

    start = text.find(address)
    if start != -1:
        end_pos = start + len(address)
        if start >= 0 and end_pos <= len(text):
            entities.append({
                "start": start,
                "end": end_pos,
                "label": "ADDRESS"
            })

    entities.sort(key=lambda x: x["start"])

    return {"text": text, "entities": entities}

def save_dataset(n_samples=1000, output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)

    data = []
    for i in range(n_samples):
        Faker.seed(i)
        data.append(generate_sample_with_entities())

    split = int(0.8 * len(data))
    train_data = data[:split]
    val_data = data[split:]

    with open(os.path.join(output_dir, "train.jsonl"), "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(os.path.join(output_dir, "val.jsonl"), "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Сохранено: {len(train_data)} в train, {len(val_data)} в val")
