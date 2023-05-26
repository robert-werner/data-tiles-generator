# Первая версия утилиты

Общая информация

На нашем сервере есть т.н. Источники

Для простоты будем считать их метеостанциями с указанными координатами.

По запросу POST /api/v2/sources/list можно получить список источников.

Пример запроса:

```bash
curl --location 'https://dcc5.modext.ru:8088/dataserver/api/v2/sources/list' \
--header 'X-Ticket: ST-test' \
--header 'Content-Type: application/json' \
--data '{
    "urn": [
        "RHM-IS-CLIWARE.synop_all"
    ]
}'
```

Ответ будет примерно такой:
```json
{
    "meta": {
        "code": 200,
        "rid": "7661a236-fb1e-11ed-9926-02420a000094",
        "time": "42.679"
    },
    "response": {
        "sources": {
            "count": 78,
            "info": {
                "page": 1,
                "pagecount": 1,
                "pagesize": 100,
                "total": 78
            },
            "items": [
                {
                    "meteoRange": 900,
                    "mid": "9d8a93f9-8f6f-11ed-a785-02420a0000d1",
                    "name": "Симферополь",
                    "objs": [],
                    "ownerOrg": 1,
                    "src": {
                        "group": "RU35",
                        "index": "33946"
                    },
                    "srctid": "SRC_TYP_METPLACE",
                    "last_insert": 1684988975,
                    "link": {},
                    "loc": {
                        "lat": 45.040278,
                        "lon": 33.967222
                    },
                    "metadata": {
                        "binding": [
                            {
                                "index": "33946",
                                "urn": "RHM-DATA-HMC-FORECAST"
                            },
                            {
                                "index": "33946",
                                "urn": "RHM-IS-CLIWARE.synop_all"
                            }
                        ]
                    },
                    "rec": {
                        "created": 1673194506,
                        "updateUser": "00000000-0000-0000-0000-000000000000",
                        "updated": 1678830353
                    },
                    "shape": {
                        "type": "Point",
                        "crs": {
                            "type": "name",
                            "properties": {
                                "name": "EPSG:4326"
                            }
                        },
                        "coordinates": [
                            33.967222,
                            45.040278
                        ]
                    },
                    "sid": "RU35-033946-0000",
                    "ter": {
                        "country": "RU",
                        "region": "RU-ROS"
                    }
                },
                {
                    "meteoRange": 900,
                    "mid": "785c598a-8fa6-11ed-a785-02420a0000d1",
                    "name": "Иркутск",
                    "objs": [],
                    "ownerOrg": 1,
                    "src": {
                        "group": "RU25",
                        "index": "30710"
                    },
                    "srctid": "SRC_TYP_METPLACE",
                    "last_insert": 1685028582,
                    "link": {},
                    "loc": {
                        "lat": 52.266667,
                        "lon": 104.316667
                    },
                    "metadata": {
                        "binding": [
                            {
                                "index": "30710",
                                "urn": "RHM-DATA-HMC-FORECAST"
                            },
                            {
                                "index": "30710",
                                "urn": "RHM-IS-CLIWARE.synop_all"
                            }
                        ]
                    },
                    "rec": {
                        "created": 1673218066,
                        "updateUser": "00000000-0000-0000-0000-000000000000",
                        "updated": 1682194220
                    },
                    "shape": {
                        "type": "Point",
                        "crs": {
                            "type": "name",
                            "properties": {
                                "name": "EPSG:4326"
                            }
                        },
                        "coordinates": [
                            104.316667,
                            52.266667
                        ]
                    },
                    "sid": "RU25-030710-0000",
                    "ter": {
                        "country": "RU",
                        "region": "RU-ROS"
                    }
                }
```

В ответе в массиве <kbd>items</kbd> перечислены Источники (станции)

Для каждой станции указываются координаты
```json
  "loc": {
    "lat": 52.266667,
    "lon": 104.316667
  }
```

Первая версия утилиты должна генерировать JSON тайлы (data tiles) из Источников для двух проекций: Меркатора и Полярной проекции.

Data Tiles представляют собой такие файлы:

```json
{
    "items": 3,
    "data": [
        "wmo-34162",
        90,
        141,
        "wmo-34161",
        106,
        114,
        "wmo-34163",
        40,
        125,
    ]
}
```
где,</br>
- <kbd>items</kbd> - количество элементов для каждой станции</br>
- <kbd>data</kbd> - массив данных по каждой станции</br>
    - 1 - идентификатор станции
    - 2,3 - позиция станции на тайле в пикселах (X/Y)

Таким образом утилита должна получать на вход идентификатор метаданных, для которых необходимо сгенерировать тайлы (urn) - в примере выше это "RHM-IS-CLIWARE.synop_all"
</br>

---

## Утилита должна генерировать набор тайлов для всех Источников этого urn

---

Алгоритм такой:

- При запуске утилита получает Источники с бэка по указанному urn
- Утилита генерирует полный набор тайлов для всех Источников этого urn для каждой проекции:
  - для каждого тайла определяется какие Источники входят в него
  - для каждого Источника определяется позиция X/Y в пикселах для этого тайла
  - повторяется для всех Источников этого тайла
  - результат записывается в JSON
