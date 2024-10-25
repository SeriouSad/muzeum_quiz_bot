import pandas as pd
from django.core.management.base import BaseCommand
from museum_bot.models import TgUser, SuperGameUser


class Command(BaseCommand):
    help = 'Export users data to an Excel file'

    def handle(self, *args, **kwargs):
        # Получение всех пользователей
        users = TgUser.objects.all().values('tg_id', 'username', 'fio', 'phone_number', 'email', 'points')
        df_all_users = pd.DataFrame(list(users))
        # Замена пустых никнеймов на прочерк
        df_all_users['username'] = df_all_users['username'].fillna('-')

        # Получение пользователей из SuperGameUser
        super_game_users = SuperGameUser.objects.select_related('user').all()
        data = []
        for user in super_game_users:
            data.append({
                'tg_id': user.user.tg_id,
                'username': user.user.username or '-',
                'fio': user.user.fio,
                'phone_number': user.user.phone_number,
                'email': user.user.email,
                'points': user.user.points,
                'answer_1': 'Верный' if user.question1 else 'Нет',
                'answer_2': 'Верный' if user.question2 else 'Нет',
                'answer_3': 'Верный' if user.question3 else 'Нет',
                'winner': 'Да' if user.winner else 'Нет'
            })
        df_super_game_users = pd.DataFrame(data)

        # Создание файла Excel с двумя листами
        with pd.ExcelWriter('users_data.xlsx') as writer:
            df_all_users.to_excel(writer, sheet_name='All Users', index=False)
            df_super_game_users.to_excel(writer, sheet_name='Super Game Users', index=False)

        self.stdout.write(self.style.SUCCESS('Данные успешно экспортированы в users_data.xlsx'))
