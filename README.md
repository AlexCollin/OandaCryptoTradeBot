https://github.com/oanda/oandapy
3370950
2b18a96d7af1f8d98191eca470b67858-04fb6f5ecdac7ffd1fc06112f0166da5

live
5634109
19b678b9251c5f098c5b933234bb8f94-3c9e98a8e7a5b0875b27f53a42a46465

**Migrations**

Сбросить базу
```
python3 migrate.py reset
```
Запустить сборку котировок с проверкой истории
```
python3 main.py -c config.json -l collector_and_checker
```
Запустить проверку со сбросом паттернов сигналов и прогнозов
```
python3 main.py -c config.json -l checker -f true
```
Запустить проверку без записи паттернов и прогнозов

```
python3 main.py -c config.json -l checker -nw true
```