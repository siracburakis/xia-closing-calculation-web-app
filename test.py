import json
import pandas as pd

# 1. JSON dosyasını yükle
with open("C:\Users\burak.kayapinar\Downloads\vX3zgGFC - gfc-feb-march.json" 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Kartları çek (cards)
cards = data['cards']

# 3. Kullanmak istediğin alanları seç
card_list = []
for card in cards:
    card_list.append({
        'id': card.get('id'),
        'name': card.get('name'),
        'desc': card.get('desc'),
        'date_created': card.get('dateLastActivity'),
        'list_id': card.get('idList'),
        'member_ids': card.get('idMembers'),
        'labels': [label['name'] for label in card.get('labels', [])],
        'closed': card.get('closed')
    })

# 4. DataFrame'e çevir
df = pd.DataFrame(card_list)

# 5. CSV olarak kaydet
df.to_csv('C:\Users\burak.kayapinar\Downloads\trello_cards.csv', index=False, encoding='utf-8')

print("CSV dosyası başarıyla oluşturuldu.")
