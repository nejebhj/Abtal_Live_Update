import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    # 1. سحب التوكن من الخزنة
    token = os.environ.get('MY_TOKEN')
    
    # 2. رابط بيانات الروستر (Live 3PL)
    url = "https://eg.me.logisticsbackoffice.com/api/dashboard/rooster/live-3pl/riders?sorting=id:desc&limit=100"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            riders = data.get('data', [])
            
            # 3. الربط بجوجل شيت (الأبطال)
            # ملحوظة: لازم ترفع ملف الـ JSON بتاع جوجل هنا برضه
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
            client = gspread.authorize(creds)
            sheet = client.open("ELABTAL").sheet1 # تأكد إن اسم الشيت صح
            
            # 4. تنظيف الشيت وكتابة البيانات الجديدة
            output = [["ID", "Name", "Status", "UTR"]] # العناوين
            for r in riders:
                output.append([r.get('id'), r.get('name'), r.get('status'), r.get('utr')])
            
            sheet.clear()
            sheet.update('A1', output)
            print("✅ تم تحديث شيت الأبطال بنجاح!")
        else:
            print(f"❌ خطأ في التوكن: {response.status_code}")
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    update_sheet()
