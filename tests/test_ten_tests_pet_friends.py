from api import PetFriends
from settings import valid_email, valid_password
import os
import string
import random

pf = PetFriends()


def test_get_api_key_for_invalid_user(email='invalid@invalid', password='invalid'):
    """ Проверяем, что запрос api ключа с некорректными email и password возвращает статус ошибки: 4хх или 5хх"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status >= 400


def test_get_pets_with_invalid_filter(filter='my_cats'):
    """ Проверяем, что запрос питомцев существующим пользователем c некорректным значением filter возвращает
    статус ошибки: 4хх или 5хх.
    Для этого, сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этого ключ,
    запрашиваем список питомцев c невалидным значением filter и проверяем статус.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status >= 400


def test_get_pets_with_invalid_auth_key(filter=''):
    """ Проверяем что запрос питомцев c некорректным api ключом возвращает статус ошибки: 4хх или 5хх.
    Для этого формируем случайный api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список питомцев и проверяем статус.
    Доступное значение параметра filter - 'my_pets' либо '' """

    auth_key = {'key': ''.join(random.choices(string.ascii_lowercase + string.digits, k=56))}
    status, _ = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status >= 400


def test_add_new_pet_without_photo(name='Кошка', animal_type='Просто кошка', age='1'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_pet_photo(pet_photo='images/photo.jpg'):
    """Проверяем возможность добавить/заменить фотографию существующему питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем/заменяем фотографию существующему питомцу
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем что статус ответа = 200, и что у питомца есть фотография
    assert status == 200
    assert len(result['pet_photo']) > 0


def test_unsuccessful_update_pet_invalid_photo(pet_photo='images/cat.tiff'):
    """Проверяем, что попытка добавить/заменить существующему питомцу фотографию в некорректном формате
    возвращает статус ошибки: 4хх или 5хх.
    Корректные форматы фотографий JPG, JPEG или PNG """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Пытаемся добавить/заменить существующему питомцу фотографию в некорректном формате
    status, _ = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status > 400


def test_unsuccessful_add_pet_with_negative_age(name='Собака', animal_type='Собака какая-то', age='- 99'):
    """Проверяем, что попытка добавить питомца без фото с некорректным отрицательным возрастом возвращает
     статус ошибки: 4хх или 5хх."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, _ = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status >= 400


def test_unsuccessful_add_pet_with_invalid_data():
    """Проверяем, что попытка добавить питомца без фото с некорректными данными возвращает
     статус ошибки: 4хх или 5хх."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Некорректные имя, тип и возраст генерируем случайно
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=255))
    animal_type = ''.join(random.choices(string.ascii_letters + string.digits, k=500))
    age = ''.join(random.choices(string.ascii_letters + string.digits, k=30))

    # Добавляем питомца
    status, _ = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
    assert status >= 400


def test_unsuccessful_update_stranger_pet_info():
    """Проверяем, что попытка обновить информацию о чужом питомце возвращает статус ошибки: 4хх или 5хх."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то удаляем всех своих питомцев
    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем список чужих питомцев
    _, stranger_pets = pf.get_list_of_pets(auth_key, "")

    # Если список чужих питомцев не пустой, то пробуем обновить информацию последнего питомца в списке,
    # чтобы не мешать другим пользователям. Имя, тип и возраст генерируем случайно, для неоднократного тестирования
    # последнего питомца в списке.
    if len(stranger_pets['pets']) > 0:
        pet_id = stranger_pets['pets'][len(stranger_pets['pets']) - 1]['id']
        name = ''.join(random.choices(string.ascii_uppercase, k=3))
        animal_type = ''.join(random.choices(string.ascii_lowercase, k=5))
        age = random.randint(100, 999)

        status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем, что статус ответа сообщает об ошибке: 4хх или 5хх
        assert status > 400
    else:
        # Если список чужих питомцев пустой, то выкидываем исключение с текстом об отсутствии чужих питомцев
        raise Exception("The list of other people's pets is empty")


def test_unsuccessful_delete_stranger_pet():
    """Проверяем, что попытка удалить чужого питомца возвращает статус ошибки: 4хх или 5хх."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то удаляем всех своих питомцев
    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем список чужих питомцев
    _, stranger_pets = pf.get_list_of_pets(auth_key, "")

    # Если список чужих питомцев не пустой, пробуем удалить чужого последнего в списке питомца,
    # чтобы не мешать другим пользователям
    if len(stranger_pets['pets']) > 0:
        pet_id = stranger_pets['pets'][len(stranger_pets['pets'])-1]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Получаем список чужих питомцев после попытки удаления
        _, stranger_pets = pf.get_list_of_pets(auth_key, "")

        # Проверяем что статус ответа сообщает об ошибке: 4хх или 5хх и чужой питомец не удалился
        assert status > 400
        assert pet_id in stranger_pets.values()
    else:
        # Если список чужих питомцев пустой, то выкидываем исключение с текстом об отсутствии чужих питомцев
        raise Exception("The list of other people's pets is empty")
