workspace {
    name "Магазин"
    description "Лабораторная работа 01"

    model {

        # Настраиваем возможность создания вложенных груп
        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь интернет-магазина" {
            description "Пользователь интернет магазина, обладающий личным аккаунтом"
        }

        shop_owner = person "Владелец интернет-магазина" {
            description "Владелец интернет магазина, добавляющий товары в базу"
        }

        online_shop = softwareSystem "Интернет-магазин" {
            description "Интернет-магазин, где пользователь может купить товар, а владелец - добавить его в базу"

            api_app = container "API Application" {
                description "Предоставляет функционал интернет-магазина"
                technology "Python, FastAPI"
            }

            group "Слой данных" {
                user_db = container "User Database" {
                    description "Реляционная БД, содержащая информацию о пользователях"
                    technology "PostgreSQL 15"
                    tags "database"
                }

                user_cache = container "User Cache" {
                    description "Кеш пользовательских данных, хранимый для ускорения поиска информации о них"
                    technology "Redis"
                    tags "database"
                }

                shop_db = container "Shop Database" {
                    description "Документоориентированная БД, содержащая информацию о товарах магазина"
                    technology "MongoDB"
                    tags "database"
                }

                shopping_cart_db = container "Shopping Cart Database" {
                    description "Документоориентированная БД, содержащая информацию о содержимом корзин пользователей"
                    technology "MongoDB"
                    tags "database"
                }
            }

            api_app -> user_db "Получение/обновление данных о пользователе" "TCP:5432"
            api_app -> user_cache "Получение/обновление данных о пользователе" "TCP:6379"
            api_app -> shop_db "Получение/обвноление данных о товаре" "TCP:27017"
            api_app -> shopping_cart_db "Получение/обвноление данных о корзине пользователя" "TCP:27018"

            user -> api_app "Просмотр товаров и добавление их в корзину" "REST HTTP:8000"
            shop_owner -> api_app "Добавление товара в магазин" "REST HTTP:8000"
        }

        user -> online_shop "Покупки в магазине" "REST HTTP:8000"
        shop_owner -> online_shop "Администрирование магазина" "REST HTTP:8000"
    }
views {
    themes default
    styles {
            element "database" {
                shape cylinder
            }
        }
    }   
}