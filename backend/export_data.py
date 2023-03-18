import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',  'crypto_project.settings')
django.setup()

from coindesk.models import Coindesk

def export_coindesk_data_to_csv(filename):
    fields = ['category', 'title', 'author', 'date', 'content', 'url']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        
        for article in Coindesk.objects.all():
            writer.writerow({
                'category': article.category,
                'title': article.title,
                'author': article.author,
                'date': article.date,
                'content': article.content,
                'url': article.url
            })

if __name__ == '__main__':
    filename = 'coindesk_data.csv'
    export_coindesk_data_to_csv(filename)
    print(f'Data exported to {filename}')