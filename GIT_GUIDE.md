# GIT Rehberi – Xiaomi Calculation Web App

Bu belge, projede Git kullanımıyla ilgili tüm temel ve ileri seviye komutları, günlük pratik adımları ve senaryoları içerir.  

---

## Geliştirmeye Devam Ederken – Günlük Akış

### 1. Proje klasörüne gir
```bash
cd C:/.../Xiaomi_Calculation_Web_App
```

### 2. Durumu kontrol et (isteğe bağlı)
```bash
git status
```

### 3. GitHub’daki güncellemeleri al (gerekirse)
```bash
git pull
```

### 4. Yeni değişiklikleri ekle ve gönder
```bash
git add .
git commit -m "Açıklayıcı commit mesajı"
git push
```

---

## Günlük Komutlar

| Komut | Açıklama |
|-------|----------|
| `git status` | Durumu ve değişiklikleri gösterir |
| `git add .` | Tüm dosyaları commit’e hazırlar |
| `git commit -m "..."` | Değişiklikleri kaydeder |
| `git push` | Değişiklikleri GitHub’a yollar |
| `git pull` | Güncellemeleri indirir |
| `git log` | Commit geçmişini listeler |

---

## Branch (Dal) İşlemleri

### Mevcut branch’leri listele:
```bash
git branch
```

### Yeni branch oluştur ve geç:
```bash
git checkout -b yeni_branch
```

### Branch değiştirme:
```bash
git checkout branch_adi
```

### Branch’i ana dal ile birleştirme:
```bash
git checkout main
git merge branch_adi
```

### Branch silme:
```bash
git branch -d branch_adi
```

---

## Geri Dönüş Senaryoları

### Son commit’i geri al (push etmediysen):
```bash
git reset --soft HEAD~1
```

### Push edilen commit’i geri al (geçmiş korunur):
```bash
git revert <commit_kodu>
```

### Eski commit’e dön ve zorla gönder (dikkatli):
```bash
git reset --hard <commit_kodu>
git push -f origin main
```

---

## Temiz Başlangıç Komutları

```bash
Remove-Item -Recurse -Force .git   # PowerShell için
git init
git remote add origin <repo_link>
git checkout -b main
git add .
git commit -m "Initial setup: ..."
git push -u origin main
```

---

## Uzak Bağlantılar

### Remote bağlantıyı görmek:
```bash
git remote -v
```

### Remote silmek:
```bash
git remote remove origin
```

### Remote eklemek:
```bash
git remote add origin <repo_link>
```

---

## Güvenlik Notları

- `.env` gibi şifre içeren dosyalar `.gitignore` içinde olmalı  
- Git geçmişinde `.env` varsa `git rm --cached .env` ile çıkarılmalı  
- Commit mesajları kısa ama açıklayıcı olmalı

---

## Önerilen Commit Mesajları

```bash
git commit -m "Initial setup: Base project with Python, NiceGUI, and DB config"
git commit -m "Fix: DB connection error resolved with text()"
git commit -m "Feature: Added sidebar navigation layout"
```

---

# Git Durum Harfleri (VS Code'da Görünen Simgeler)

| Harf | Anlamı    | Açıklama                                                               |
|------|-----------|------------------------------------------------------------------------|
| M    | Modified  | Dosya değiştirildi, ama henüz commit edilmedi.                         |
| U    | Untracked | Git tarafından takip edilmeyen yeni bir dosya.                         |
| A    | Added     | `git add` ile eklendi, commit edilmeyi bekliyor.                       |
| D    | Deleted   | Takip edilen dosya silindi.                                            |
| R    | Renamed   | Takip edilen dosyanın adı değiştirildi.                                |
| C    | Copied    | Başka bir dosyadan kopyalanarak oluşturuldu.                           |