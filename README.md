# Termer
Простое приложение для преподавателей, позволяющее на основе заранее заданных разделов и терминов в них строить случайные выборки (по названию, описанию или изображению).
Полученная выборка может быть передана учащемуся для проверки его знаний терминов.
Учащемуся предлагает дописать недостающую часть термина на основе увиденной:
* К названию - описание (и картинка)
* К описанию - название (и картинка)
* К картинке - название и описание

# Установка
## Windows
### Простой способ
1. Скачать установщик (.exe) или сброку (.zip) со страницы релизов, выбрав последнюю версию
2. Запустить установщик

### Запуск из исходного кода
1. Установить Python в соответствии с инструкцией для вашей платформы
2. Клонировать репозиторий:
  ```bash
  git clone git@github.com:goodm2ice/termer.git
  ```
3. В папке репозитория открыть терминал и вписать команду:
    ```bash
    python src/main.py
    ```

### Сброка установщика из исходного кода
1. Установить Python в соответствии с инструкцией для вашей платформы
2. Установить NSIS в соответствии с инструкцией для вашей платформы
3. Клонировать репозиторий:
  ```bash
  git clone git@github.com:goodm2ice/termer.git
  ```
Запустить сброку в зависимости от системы:

**Для Windows**
```powershell
.\build.ps1
```

**Для Linux/MAC**
```bash
chmod +x build.sh
./build.sh
```