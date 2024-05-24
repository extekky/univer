import json
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Задаем значения
# ------------------------------------------
clist_values = [
    "eth2", "eth5", "eth6"
]

chash_values = {
    "eth0": "100",
    "eth2": "20",
    "eth5": "30",
    "eth10": "4",
}

r.delete('clist', 'chash')
r.lpush('clist', *clist_values)

for key, value in chash_values.items():
    r.hset('chash', key, value)
# ------------------------------------------

# Получаем значения
clist = r.lrange('clist', 0, -1)
chash = r.hgetall('chash')

slist = [value.decode('utf-8') for value in clist if value in chash]
print(slist)

# Вычисление значений для хэш-таблицы shash
shash = {}
for key, value in chash.items():
    key_str = key.decode('utf-8')
    if key_str in slist:
        shash[key_str] = int(value) * 2
    else:
        shash[key_str] = 0

# Запись данных в Redis
r.delete('slist', 'shash')
r.lpush('slist', *slist)
print(shash)
for key, value in shash.items():
    r.hset('shash', key, value)

print(json.dumps(shash, indent=4))
