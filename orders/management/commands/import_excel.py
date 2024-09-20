import os

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand

from orders.models import DeliveryRequest, DeliveryStatusCurrent, DeliveryRequestStatusHistory


class Command(BaseCommand):
    help = 'Импорт данных из DeliveryData.xlsx в базу данных'

    def handle(self, *args, **kwargs):
        excel_file = os.path.join(settings.BASE_DIR, 'DeliveryData.xlsx')

        # импорт данных из листа DeliveryRequest
        df_requests = pd.read_excel(excel_file, sheet_name='DeliveryRequests')
        delivery_requests = []
        for _, row in df_requests.iterrows():
            delivery_request = DeliveryRequest(
                internal_id=row['InternalId'],
                city=row['DeliveryCity'],
                address=row['DeliveryAddress'],
                delivery_date=row['DeliveryDate'],
                delivery_time=row['DeliveryTime'],
                customer=row['CustomerName'],
                comment=row['Comment'],
                package_type=row['PackageType'],
                load_date=row['LoadDate'],
            )
            delivery_requests.append(delivery_request)

        DeliveryRequest.objects.bulk_create(delivery_requests)
        self.stdout.write(self.style.SUCCESS('DeliveryRequests успешно импортированы'))

        # создадим словарь для быстрого доступа к DeliveryRequest по id
        delivery_requests_dict = {dr.internal_id: dr for dr in DeliveryRequest.objects.all()}

        # импорт данных из листа DeliveryStatusCurrent
        df_statuses = pd.read_excel(excel_file, sheet_name='DeliveryStatusCurrent')
        delivery_statuses = []
        for _, row in df_statuses.iterrows():
            delivery_status = DeliveryStatusCurrent(
                internal_id=delivery_requests_dict[row['InternalId']],
                status_name=row['StatusName'],
                load_date=row['LoadDate'],
            )
            delivery_statuses.append(delivery_status)

        DeliveryStatusCurrent.objects.bulk_create(delivery_statuses)
        self.stdout.write(self.style.SUCCESS('DeliveryStatusCurrent успешно импортированы'))

        # импорт данных из листа DeliveryRequestStatusHistory
        df_history = pd.read_excel(excel_file, sheet_name='DeliveryStatusHistory')
        delivery_histories = []
        for _, row in df_history.iterrows():
            delivery_history = DeliveryRequestStatusHistory(
                internal_id=delivery_requests_dict[row['InternalId']],
                status_name=row['StatusName'],
                load_date=row['LoadDate'],
            )
            delivery_histories.append(delivery_history)

        DeliveryRequestStatusHistory.objects.bulk_create(delivery_histories)
        self.stdout.write(self.style.SUCCESS('DeliveryRequestStatusHistory успешно импортированы'))
