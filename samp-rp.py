"""
    sender - ник
    Acc[sender][0] - Пароль
    Acc[sender][1] - Статус бана
    Acc[sender][2] - Админ-Уровень
    Acc[sender][3] - Админ-Пароль
    Acc[sender][4] - Бабло
    Acc[sender][5] - Варны
    Acc[sender][6] - Лвл
    Acc[sender][7] - Престиж

    Server[0] - Цена работы на ферме
    Server[1] - Множитель коэфицента Casino
"""
import json, time, random
# Десериализация

Acc = {}
Server = []

with open('accounts.json', 'r') as f:
    Acc = json.load(f)

with open('data.json', 'r') as f:
    Server = json.load(f)

# Глобальные переменные

nickname = ''
bannedStatus = False
alogined = False

# Сериализация

def save_data():
    with open('accounts.json', 'w') as f:
            json.dump(Acc, f, sort_keys=True)
    with open('data.json', 'w') as f:
            json.dump(Server, f, sort_keys=True)
# Команды

def cmd_alogin(sender):
    global alogined
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    key = input('Введите ваш админ-пароль: ')
    if key == Acc[sender][3] or Acc[sender][3] == '-1':
        print('Вы вошли как модератор', Acc[sender][2], 'уровня')
        alogined = True
        if Acc[sender][3] == '-1':
            Acc[sender][3] = key
            print('Ваш новый админ-пароль:',key)
            save_data()
    else:
        print('Неверный админ-пароль!')

def cmd_makeadmin(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 7:
        print('У вас слишком низкий уровень модератора! (Нужен 7)')
        return
    a,b = input('Введите Ник и Уровень админки через пробел: ').split(' ', 1)
    b = int(b)
    if b >= Acc[sender][2] and Acc[sender][2] < 10:
        print('Вы не можете выдать уровень больше вашего или равный вашему!')
        return
    if a in Acc:
        if Acc[a][2] == 10:
            print('Вы не можете установить ему уровень админки!')
            return
        Acc[a][2] = b
        print('Вы назначили',a,'модератором',b,'уровня')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_delete(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 10:
        print('У вас слишком низкий уровень модератора! (Нужен 10)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        if Acc[a][2] == 10:
            print('Вы не можете удалить ему аккаунт!')
            return
    Acc.pop(a, None)
    print('Файл-Аккаунт удалён!')
    save_data()

def cmd_unban(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        Acc[a][1] = False
        print('Вы разбанили аккаунт')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_ban(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 2:
        print('У вас слишком низкий уровень модератора! (Нужен 2)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        if Acc[a][2] >= 7 and Acc[sender][2] < 10:
            print('Вы не можете забанить его!')
            return
        Acc[a][1] = True
        print('Вы забанили аккаунт')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_ahelp(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    print('Команды модератора сервера Samp-Rp:')
    if Acc[sender][2] >= 1:
        print('<1> /getstats /unban /unwarn /ahelp /alogin /akey /alvlup')
    if Acc[sender][2] >= 2:
        print('<2> /ban /warn')
    if Acc[sender][2] >= 3:
        pass
    if Acc[sender][2] >= 4:
        pass
    if Acc[sender][2] >= 5:
        pass
    if Acc[sender][2] >= 6:
        print('<6> /setfarmcost')
    if Acc[sender][2] >= 7:
        print('<7> /makeadmin')
    if Acc[sender][2] >= 8:
        print('<8> /setstat')
    if Acc[sender][2] >= 9:
        print('<9> /givemoney /setcasinomultiplier /prestige')
    if Acc[sender][2] >= 10:
        print('<10> /delete, /agetstats, Защита от бана, Расширен /makeadmin')

def cmd_help(sender):
    print('/money - узнать средства на счету')
    print('/transfer - передать деньги другому игроку')
    print('/alogin - войти как модератор')
    print('/ahelp - команды модератора')
    print('/changepassword - сменить пароль')
    print('/stats - узнать свою статистику')
    print('/casino - сыграть в казино')
    print('/farm - работать на ферме')
    print('/lvlup - повысить лвл (Цена:',100000+Acc[sender][6]*100000,'вирт)')
    print('/buyadm - купить админку (Цена: 1.000.000.000 вирт, мин. 30 лвл)')
    print('/alvlup - повысить лвл админки (с 1 по 6: 100.000.000 вирт и 50 лвл, с 6 на 7: 500.000.000 вирт и 70 лвл, с 7 по 9: 1.000.000.000 вирт и 100 лвл, на 10: Престиж + 3.000.000.000 вирт и 150 лвл)')
    print('/prestige - получить престиж (Доступно на 9 лвле админки, сбрасываются все деньги и админка)')
def cmd_akey(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    key = input('Введите ваш админ-пароль: ')
    if key == Acc[sender][3]:
        key2 = input('Введите новый админ-пароль: ')
        Acc[sender][3] = key2
        print('Ваш новый админ-пароль:',key2)
        save_data()
    else:
        print('Неверный админ-пароль!')

def cmd_givemoney(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 9:
        print('У вас слишком низкий уровень модератора! (Нужен 9)')
        return
    a,b = input('Введите Ник и Сколько дать денег через пробел (пример: Nick_Sule 50000): ').split(' ', 1)
    b = int(b)
    if a in Acc:
        Acc[a][4] += b
        print('Вы выдали',b,'вирт игроку',a)
        print('Баланс игрока:',Acc[a][4],'вирт')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_money(sender):
    print('На вашем счету',Acc[sender][4],'вирт')

def cmd_transfer(sender):
    a,b = input('Введите Ник и Сколько денег перевести через пробел (пример: Nick_Sule 50000): ').split(' ', 1)
    b = int(b)
    if b > Acc[sender][4]:
        print('У вас слишком мало денег!')
        return
    if b < 1:
        print('Как минимум 1 вирт')
        return
    if a in Acc:
        Acc[sender][4] -= b
        Acc[a][4] += b
        print('Вы перевели',b,'вирт игроку',a)
        print('На вашем счету осталось',Acc[sender][4],'вирт')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_changepassword(sender):
    key = input('Введите ваш пароль: ')
    if key == Acc[sender][0]:
        newkey = input('Введите новый пароль: ')
        Acc[sender][0] = newkey
        save_data()
        print('Ваш новый пароль:',newkey)
    else:
        print('Неверный пароль!')

def cmd_warn(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 2:
        print('У вас слишком низкий уровень модератора! (Нужен 2)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        if Acc[a][2] >= 1 and Acc[sender][2] < 10:
            print('Вы не можете дать варн ему!')
            return
        Acc[a][5] += 1
        if Acc[a][5] >= 3:
            Acc[a][5] = 0
            Acc[a][1] = True
            print('Вы заблокировали аккаунт [3 Варна]')
        else:
            print('Вы выдали варн')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_unwarn(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        if Acc[a][5] <= 0:
            print('У игрока 0 Варнов')
            return
        Acc[a][5] -= 1
        print('Вы сняли варн')
        save_data()
    else:
        print('Файл-Аккаунт не найден')

def cmd_stats(sender):
    print('Ваш ник:',sender)
    print('Уровень:',Acc[sender][6])
    print('Админ-Уровень:',Acc[sender][2])
    print('Варны:',Acc[sender][5])
    print('Деньги:',Acc[sender][4])
    print('Есть престиж:',Acc[sender][7])

def cmd_setstat(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 8:
        print('У вас слишком низкий уровень модератора! (Нужен 8)')
        return
    print('Пункты: 0 - Уровень, 1 - Варны')
    a, b, c = input('Введите Имя Файл-Аккаунта, Пункт и Значение через пробел (Пример: Nick_Sule 0 1): ').split(' ', 2)
    b = int(b)
    c = int(c)
    if a in Acc:
        if Acc[a][2] >= 7 and Acc[sender][2] < 10:
            print('Вы не можете изменить ему статистику!')
            return
        if b == 0:
            Acc[a][6] = c
            print('Вы изменили Уровень игрока на',c)
            save_data()
        elif b == 1:
            Acc[a][5] = c
            print('Вы изменили Варны игрока на',c)
            if Acc[a][5] >= 3:
                Acc[a][5] = 0
                Acc[a][1] = True
                print('Вы заблокировали аккаунт [3 Варна]')
            save_data()
        else:
            print('Ошибка')
    else:
        print('Файл-Аккаунт не найден')

def cmd_getstats(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        print('Ник:',a)
        print('Статус бана:',Acc[a][1])
        print('Уровень:',Acc[a][6])
        print('Админ-Уровень:',Acc[a][2])
        print('Варны:',Acc[a][5])
        print('Деньги:',Acc[a][4])
        print('Есть престиж:',Acc[a][7])
    else:
        print('Файл-Аккаунт не найден')

def cmd_agetstats(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 10:
        print('У вас слишком низкий уровень модератора! (Нужен 10)')
        return
    a = input('Введите Имя Файл-Аккаунта: ')
    if a in Acc:
        print('Ник:',a)
        print('Пароль:',Acc[a][0])
        print('Статус бана:',Acc[a][1])
        print('Уровень:',Acc[a][6])
        print('Админ-Уровень:',Acc[a][2])
        print('Админ-Пароль:',Acc[a][3])
        print('Варны:',Acc[a][5])
        print('Деньги:',Acc[a][4])
        print('Есть престиж:',Acc[a][7])
    else:
        print('Файл-Аккаунт не найден')

def cmd_casino(sender):
    while True:
        print('-1 - Выйти, 0 - Ставки, 1 - Кости')
        a,b = input('Введите ID игры и ставку через пробел: ').split(' ', 1)
        a = int(a)
        b = int(b)
        if b < 0 or b > Acc[sender][4]:
            print('У вас недостаточно денег (Или ставка меньше 0)')
            continue
        if a == -1:
            break
        elif a == 0:
            coef = (round(random.uniform(1.3, 5.1)*Server[1], 2), round(random.uniform(1.3, 5.1)*Server[1], 2), round(random.uniform(1.3, 5.1)*Server[1], 2))
            print('Коэфиценты:')
            print('1 черепаха -', coef[0],', вторая -',coef[1],', третья -',coef[2])
            c = int(input('На какую черепаху вы хотите поставить? (от 1 до 3): '))
            if c > 3 or c < 1:
                print('Ошибка!')
                continue
            winner = random.randint(1, 3)
            print('На старт, Внимание, Марш...')
            Acc[sender][4] -= b
            save_data()
            time.sleep(5)
            if winner == c:
                print('Вы победили! Сумма выигрыша:',int(b*coef[winner-1]))
                Acc[sender][4] += int(b*coef[winner-1])
                save_data()
            else:
                print('Вы проиграли... Победила черепаха под номером',winner,'! Повезет в следующий раз!')
        elif a == 1:
            your = random.randint(1, 12)
            computers = random.randint(1, 12)
            print('Кости взмывают вверх...')
            time.sleep(3)
            if your > computers:
                print('Вы выиграли! Счёт: ',your,':',computers)
                Acc[sender][4] += int(b*Server[1])
            elif your == computers:
                print('Ничья! Счёт: ',your,':',computers)
            else:
                print('Вы проиграли... Счёт: ',your,':',computers)
                Acc[sender][4] -= b
            save_data()
        else:
            print('Ошибка!')
def cmd_farm(sender):
    print('Вы добываете колосок...')
    time.sleep(5)
    print('Вы добыли колосок и заработали',Server[0],'вирт')
    Acc[sender][4] += Server[0]
    save_data()

def cmd_setfarmcost(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 6:
        print('У вас слишком низкий уровень модератора! (Нужен 6)')
        return
    a = int(input('Введите цену за колосок (от 10 до 300): '))
    if a < 10 or a > 300 and Acc[sender][2] < 9:
        print('Минимум 10 вирт, а максимум 300!')
        return
    Server[0] = a
    save_data()
    print('Новая цена за колосок:',a,'вирт')

def cmd_setcasinomultiplier(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 9:
        print('У вас слишком низкий уровень модератора! (Нужен 9)')
        return
    a = float(input('Введите множитель выигрыша казино (от 1.0 до 3.0): '))
    if a < 1.0 or a > 3.0 and Acc[sender][2] < 10:
        print('Минимум 1.0, а максимум 3.0!')
        return
    Server[1] = a
    save_data()
    print('Новый множитель казино:',a)

def cmd_boostinfo(sender):
    print('Цена за колосок:',Server[0])
    print('Множитель выигрыша в казино:',Server[1])

def cmd_lvlup(sender):
    summa = 100000+Acc[sender][6]*100000
    if summa > Acc[sender][4]:
        print('У вас недостаточно средств для повышения уровня, нужно',summa,'вирт')
        return
    Acc[sender][4] -= summa
    Acc[sender][6] += 1
    save_data()
    print('Вы повысили свой уровень на 1. Новый уровень:',Acc[sender][6])

def cmd_buyadm(sender):
    if Acc[sender][2] > 0:
        print('Вы уже модератор!')
        return
    if 1000000000 > Acc[sender][4]:
        print('У вас недостаточно средств! Нужен 1 миллиард вирт.')
        return
    if Acc[sender][6] < 30:
        print('Для покупки нужен минимум 30 уровень.')
        return
    Acc[sender][4] -= 1000000000
    Acc[sender][2] = 1
    save_data()
    print('Вы приобрели права модерирования 1 уровня. Введите /alogin и придумайте пароль. Запомните его!')

def cmd_alvlup(sender):
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 1:
        print('У вас слишком низкий уровень модератора! (Нужен 1)')
        return
    if Acc[sender][2] < 6:
        if 100000000 > Acc[sender][4]:
            print('У вас недостаточно средств! Нужно 100 миллионов вирт.')
            return
        if Acc[sender][6] < 50:
            print('Для повышения нужен минимум 50 уровень.')
            return
        Acc[sender][4] -= 100000000
        Acc[sender][2] += 1
        save_data()
        print('Вы повысили свой уровень модерирования на 1. Новый уровень:',Acc[sender][2])
    elif Acc[sender][2] == 6:
        if 500000000 > Acc[sender][4]:
            print('У вас недостаточно средств! Нужно 500 миллионов вирт.')
            return
        if Acc[sender][6] < 70:
            print('Для повышения нужен минимум 70 уровень.')
            return
        Acc[sender][4] -= 500000000
        Acc[sender][2] += 1
        save_data()
        print('Вы повысили свой уровень модерирования на 1. Новый уровень:',Acc[sender][2])
    elif Acc[sender][2] > 6 and Acc[sender][2] < 9:
        if 1000000000 > Acc[sender][4]:
            print('У вас недостаточно средств! Нужно 1 миллиард вирт.')
            return
        if Acc[sender][6] < 100:
            print('Для повышения нужен минимум 100 уровень.')
            return
        Acc[sender][4] -= 1000000000
        Acc[sender][2] += 1
        save_data()
        print('Вы повысили свой уровень модерирования на 1. Новый уровень:',Acc[sender][2])
    elif Acc[sender][2] == 9:
        if 3000000000 > Acc[sender][4]:
            print('У вас недостаточно средств! Нужно 3 миллиарда вирт.')
            return
        if Acc[sender][7] == False:
            print('У вас нету престижа! Получите его командой /prestige.')
            return
        if Acc[sender][6] < 150:
            print('Для повышения нужен минимум 150 уровень.')
            return
        Acc[sender][4] -= 3000000000
        Acc[sender][2] += 1
        save_data()
        print('Вы повысили свой уровень модерирования до максимального.')
    else:
        print('У вас максимальный уровень!')

def cmd_prestige(sender):
    if Acc[sender][7] == True:
        print('У вас и так есть престиж!')
        return
    if alogined == False:
        print('Авторизуйтесь как модератор (/alogin)')
        return
    if Acc[sender][2] < 9:
        print('У вас слишком низкий уровень модератора! (Нужен 9)')
        return
    print('Вы получили престиж.')
    print('Все значения были сброшены, деньги и админ-уровень были обнулены.')
    print('Теперь когда вы получите 9 уровень модерирования, вы сможете стать модератором 10 уровня.')
    Acc[sender][2] = 0
    Acc[sender][3] = '-1'
    Acc[sender][4] = 0
    Server[0] = 100
    Server[1] = 1.0
    Acc[sender][7] = True
    save_data()
# Словарь команд

cmds = {
    '/makeadmin' : cmd_makeadmin,
    '/delete' : cmd_delete,
    '/ban' : cmd_ban,
    '/unban' : cmd_unban,
    '/ahelp' : cmd_ahelp,
    '/help' : cmd_help,
    '/alogin' : cmd_alogin,
    '/akey' : cmd_akey,
    '/givemoney' : cmd_givemoney,
    '/money' : cmd_money,
    '/transfer' : cmd_transfer,
    '/changepassword' : cmd_changepassword,
    '/warn' : cmd_warn,
    '/unwarn' : cmd_unwarn,
    '/stats' : cmd_stats,
    '/setstat' : cmd_setstat,
    '/getstats' : cmd_getstats,
    '/agetstats' : cmd_agetstats,
    '/casino' : cmd_casino,
    '/farm' : cmd_farm,
    '/setfarmcost' : cmd_setfarmcost,
    '/setcasinomultiplier' : cmd_setcasinomultiplier,
    '/boostinfo' : cmd_boostinfo,
    '/lvlup' : cmd_lvlup,
    '/buyadm' : cmd_buyadm,
    '/alvlup' : cmd_alvlup,
    '/prestige' : cmd_prestige
}
# Основной цикл

while True:
    nickname = input('SA-MP: Type your nickname (type q to exit): ')
    if nickname == 'q':
        break
    if nickname in Acc:
        parol = input('~~~~~~~~~~~~~~~~\nДобро пожаловать на Samp-Rp\n\nВаш аккаунт зарегистрирован\n\nВведите пароль:\n~~~~~~~~~~~~~~~~\n')
        if parol != Acc[nickname][0]:
            print('Неверный пароль!')
        else:
            print('Добро пожаловать на Samp-Rp')
            print('Введите /help чтобы узнать основные команды сервера')
            if Acc[nickname][1] == True:
                print('Ваш аккаунт заблокирован.')
            else:
                while True:
                    comanda = input('Введите команду: ')
                    if comanda == '/q' or comanda == '/quit':
                        alogined = False
                        break
                    if comanda in cmds:
                        cmds[comanda](nickname)
                    else:
                        print('Команда не найдена!')
    else:
        if nickname.find('Pavlov') != -1:
            bannedStatus = True
        parol = input('~~~~~~~~~~~~~~~~\nДобро пожаловать на Samp-Rp\n\nВаш аккаунт не зарегистрирован\n\nВведите пароль:\n~~~~~~~~~~~~~~~~\n')
        print('Добро пожаловать на Samp-Rp')
        print('Ваш Файл-Аккаунт зарегистрирован')
        print('Перезайдите!')
        if bannedStatus == True:
            print('Ваш аккаунт заблокирован.')
        Acc[nickname] = [parol, bannedStatus, 0, '-1', 0, 0, 0, False]
        save_data()
        bannedStatus = False